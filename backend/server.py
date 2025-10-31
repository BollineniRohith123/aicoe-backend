from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone
import json
import aiofiles
import asyncio

# Import multi-agent system
from agents.llm_client import LLMClient
from agents.orchestrator import OrchestratorAgent

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize LLM Client and Orchestrator
# Using OpenRouter API with GLM-4.6 model (NO GPT models)
llm_client = LLMClient(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    provider="openrouter",
    model="z-ai/glm-4.6"
)
orchestrator = OrchestratorAgent(llm_client, db)

# Storage directory for project artifacts
STORAGE_DIR = ROOT_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

# Workflow state tracking to prevent duplicate executions
active_workflows = {}  # {workflow_id: {"status": "running"|"completed"|"failed", "task": asyncio.Task}}

# Create the main app without a prefix
app = FastAPI(title="AICOE Automation Platform API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.workflow_status: Dict[str, Dict[str, Any]] = {}

    async def connect(self, workflow_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[workflow_id] = websocket
        logging.info(f"WebSocket connected for workflow: {workflow_id}")

    def disconnect(self, workflow_id: str):
        if workflow_id in self.active_connections:
            del self.active_connections[workflow_id]
            logging.info(f"WebSocket disconnected for workflow: {workflow_id}")

    async def send_progress(self, workflow_id: str, data: Dict[str, Any]):
        """Send progress update to connected client"""
        if workflow_id in self.active_connections:
            try:
                await self.active_connections[workflow_id].send_json(data)
                logging.debug(f"Sent progress update for {workflow_id}: {data.get('stage', 'unknown')}")
            except Exception as e:
                logging.error(f"Error sending progress update: {str(e)}")
                self.disconnect(workflow_id)

    def update_status(self, workflow_id: str, status: Dict[str, Any]):
        """Update workflow status"""
        self.workflow_status[workflow_id] = status

    def get_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get workflow status"""
        return self.workflow_status.get(workflow_id)

manager = ConnectionManager()


# ===== MODELS =====

class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

class ProcessTranscriptRequest(BaseModel):
    project_name: str = Field(..., min_length=1, description="Name of the project")
    transcript: str = Field(..., min_length=10, description="Meeting transcript text")

class ProcessTranscriptResponse(BaseModel):
    project_id: str
    project_name: str
    status: str
    message: str
    workflow_id: str

class ProjectResponse(BaseModel):
    project_id: str
    project_name: str
    status: str
    created_at: str
    workflow_id: str
    results: Optional[Dict[str, Any]] = None


# ===== ROUTES =====

@api_router.get("/")
async def root():
    return {
        "message": "AICOE Automation Platform API",
        "version": "1.0.0",
        "status": "running"
    }

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)
    
    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()
    
    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)
    
    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])
    
    return status_checks

@api_router.get("/workflow/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """
    Get the current status of a workflow
    Returns workflow state, completed agents, and results
    """
    try:
        # Check if workflow exists in active workflows
        if workflow_id in active_workflows:
            workflow_state = active_workflows[workflow_id]

            # Get workflow status from manager
            workflow_status = manager.workflow_status.get(workflow_id, {})

            return {
                "workflow_id": workflow_id,
                "status": workflow_state["status"],
                "project_name": workflow_state.get("project_name"),
                "start_time": workflow_state.get("start_time").isoformat() if workflow_state.get("start_time") else None,
                "end_time": workflow_state.get("end_time").isoformat() if workflow_state.get("end_time") else None,
                "completed_agents": workflow_status.get("completed_agents", []),
                "current_agent": workflow_status.get("current_agent"),
                "agent_statuses": workflow_status.get("agent_statuses", {}),
                "results": workflow_status.get("results"),
                "error": workflow_state.get("error")
            }
        else:
            # Workflow not found in active workflows
            return {
                "workflow_id": workflow_id,
                "status": "not_found",
                "message": "Workflow not found. It may have been cleaned up or never existed."
            }

    except Exception as e:
        logger.error(f"Error retrieving workflow status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve workflow status: {str(e)}")

@api_router.post("/process-transcript")
async def process_transcript(request: ProcessTranscriptRequest):
    """
    Process a meeting transcript through the multi-agent workflow
    Returns workflow_id immediately, client should connect to WebSocket for progress
    """
    try:
        logger.info(f"Processing transcript for project: {request.project_name}")

        # Generate project ID and workflow ID
        project_id = str(uuid.uuid4())
        workflow_id = f"workflow_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{project_id[:8]}"

        # Return immediately with workflow_id
        # Client will connect to WebSocket for progress updates
        return {
            "project_id": project_id,
            "project_name": request.project_name,
            "status": "started",
            "message": "Workflow started. Connect to WebSocket for progress updates.",
            "workflow_id": workflow_id
        }

    except Exception as e:
        logger.error(f"Error starting workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to start workflow: {str(e)}")

@api_router.websocket("/ws/{workflow_id}")
async def websocket_endpoint(websocket: WebSocket, workflow_id: str):
    """
    WebSocket endpoint for real-time workflow progress updates
    """
    logger.info(f"WebSocket connected for workflow: {workflow_id}")
    await manager.connect(workflow_id, websocket)

    try:
        # Wait for start message from client
        logger.info(f"Waiting for start message from client for workflow: {workflow_id}")
        data = await websocket.receive_json()
        logger.info(f"Received message from client: {data}")

        action = data.get("action")

        # Handle reconnection - don't restart workflow
        if action == "reconnect":
            logger.info(f"Client reconnecting to workflow: {workflow_id}")

            # Check if workflow is still running
            if workflow_id in active_workflows:
                workflow_state = active_workflows[workflow_id]
                await websocket.send_json({
                    "type": "reconnect_ack",
                    "status": workflow_state["status"],
                    "message": f"Reconnected to workflow. Status: {workflow_state['status']}"
                })
            else:
                await websocket.send_json({
                    "type": "reconnect_ack",
                    "status": "unknown",
                    "message": "Workflow not found in active workflows. It may have completed."
                })

            # Continue to keep connection alive section below
            # The workflow will continue sending progress updates through the manager

        elif action == "start":
            # Check if workflow is already running
            if workflow_id in active_workflows:
                workflow_state = active_workflows[workflow_id]
                if workflow_state["status"] == "running":
                    logger.warning(f"Workflow {workflow_id} is already running. Ignoring duplicate start request.")
                    await websocket.send_json({
                        "type": "error",
                        "message": "Workflow is already running. Please wait for it to complete."
                    })
                    return

            project_name = data.get("project_name")
            transcript = data.get("transcript")

            if not project_name or not transcript:
                logger.error(f"Missing project_name or transcript for workflow: {workflow_id}")
                await websocket.send_json({
                    "type": "error",
                    "message": "Missing project_name or transcript"
                })
                return

            logger.info(f"Starting workflow for project: {project_name}")

            # Mark workflow as running
            active_workflows[workflow_id] = {
                "status": "running",
                "project_name": project_name,
                "start_time": datetime.utcnow()
            }

            # Initialize workflow status tracking
            manager.workflow_status[workflow_id] = {
                "completed_agents": [],
                "current_agent": None,
                "agent_statuses": {},
                "results": {}
            }

            # Create progress callback
            async def progress_callback(progress_data):
                # Update workflow status in manager
                stage = progress_data.get("stage")
                status = progress_data.get("status")

                if stage and stage != "workflow":
                    # Update current agent
                    if status == "running":
                        manager.workflow_status[workflow_id]["current_agent"] = stage

                    # Update agent status
                    manager.workflow_status[workflow_id]["agent_statuses"][stage] = status

                    # Add to completed agents if completed
                    if status == "completed" and stage not in manager.workflow_status[workflow_id]["completed_agents"]:
                        manager.workflow_status[workflow_id]["completed_agents"].append(stage)

                # Send progress update to client
                await manager.send_progress(workflow_id, {
                    "type": "progress",
                    **progress_data
                })

            # Execute workflow with progress callback
            try:
                workflow_result = await orchestrator.execute_workflow(
                    project_name=project_name,
                    transcript=transcript,
                    workflow_type="full",
                    progress_callback=progress_callback
                )

                # Update workflow state to completed
                if workflow_id in active_workflows:
                    active_workflows[workflow_id]["status"] = "completed"
                    active_workflows[workflow_id]["end_time"] = datetime.utcnow()

                # Generate project ID
                project_id = workflow_id.split("_")[-1]

                # Create project directory
                project_dir = STORAGE_DIR / project_id
                project_dir.mkdir(exist_ok=True)

                # Save artifacts
                artifacts = {}

                # Save PRD if available
                if "prd" in workflow_result.get("results", {}):
                    prd_data = workflow_result["results"]["prd"]
                    prd_content = prd_data.get("prd_markdown", "")
                    prd_file = project_dir / "PRD.md"
                    async with aiofiles.open(prd_file, 'w') as f:
                        await f.write(prd_content)
                    artifacts["prd"] = str(prd_file)

                    # Save PDF if available
                    if "prd_pdf" in prd_data:
                        prd_pdf_content = prd_data.get("prd_pdf", b"")
                        prd_pdf_file = project_dir / "PRD.pdf"
                        async with aiofiles.open(prd_pdf_file, 'wb') as f:
                            await f.write(prd_pdf_content)
                        artifacts["prd_pdf"] = str(prd_pdf_file)

                # Save Mockup if available (multi-page support)
                if "mockup" in workflow_result.get("results", {}):
                    mockup_data = workflow_result["results"]["mockup"]

                    # Save main index.html
                    mockup_content = mockup_data.get("mockup_html", "")
                    mockup_file = project_dir / "index.html"
                    async with aiofiles.open(mockup_file, 'w') as f:
                        await f.write(mockup_content)
                    artifacts["mockup"] = str(mockup_file)

                    # Save additional pages if available
                    mockup_pages = mockup_data.get("mockup_pages", {})
                    if isinstance(mockup_pages, dict):
                        for page_name, page_content in mockup_pages.items():
                            if page_name != "index.html":  # index.html already saved
                                page_file = project_dir / page_name
                                async with aiofiles.open(page_file, 'w') as f:
                                    await f.write(page_content)
                                artifacts[f"mockup_{page_name}"] = str(page_file)

                # Save Commercial Proposal if available
                if "commercial_proposal" in workflow_result.get("results", {}):
                    proposal_data = workflow_result["results"]["commercial_proposal"]
                    proposal_content = proposal_data.get("proposal_markdown", "")
                    proposal_file = project_dir / "Proposal.md"
                    async with aiofiles.open(proposal_file, 'w') as f:
                        await f.write(proposal_content)
                    artifacts["commercial_proposal"] = str(proposal_file)

                    # Save Proposal PDF if available
                    if "proposal_pdf" in proposal_data:
                        proposal_pdf_content = proposal_data.get("proposal_pdf", b"")
                        proposal_pdf_file = project_dir / "Proposal.pdf"
                        async with aiofiles.open(proposal_pdf_file, 'wb') as f:
                            await f.write(proposal_pdf_content)
                        artifacts["commercial_proposal_pdf"] = str(proposal_pdf_file)

                # Save BOM if available
                if "bom" in workflow_result.get("results", {}):
                    bom_data = workflow_result["results"]["bom"]
                    bom_json = bom_data.get("bom_json", {})
                    bom_json_file = project_dir / "BOM.json"
                    async with aiofiles.open(bom_json_file, 'w') as f:
                        await f.write(json.dumps(bom_json, indent=2))
                    artifacts["bom_json"] = str(bom_json_file)

                    # Save BOM PDF if available
                    if "bom_pdf" in bom_data:
                        bom_pdf_content = bom_data.get("bom_pdf", b"")
                        bom_pdf_file = project_dir / "BOM.pdf"
                        async with aiofiles.open(bom_pdf_file, 'wb') as f:
                            await f.write(bom_pdf_content)
                        artifacts["bom_pdf"] = str(bom_pdf_file)

                # Save Architecture Diagram if available
                if "architecture_diagram" in workflow_result.get("results", {}):
                    arch_data = workflow_result["results"]["architecture_diagram"]
                    arch_content = arch_data.get("architecture_html", "")
                    arch_file = project_dir / "Architecture.html"
                    async with aiofiles.open(arch_file, 'w') as f:
                        await f.write(arch_content)
                    artifacts["architecture_diagram"] = str(arch_file)

                # Save complete workflow results
                results_file = project_dir / "workflow_results.json"
                async with aiofiles.open(results_file, 'w') as f:
                    await f.write(json.dumps(workflow_result, indent=2, default=str))

                # Store project metadata in database
                project_doc = {
                    "id": project_id,
                    "project_name": project_name,
                    "workflow_id": workflow_id,
                    "status": workflow_result["status"],
                    "created_at": datetime.utcnow().isoformat(),
                    "artifacts": artifacts,
                    "results": workflow_result["results"],
                    "context": workflow_result["context"]
                }

                await db.projects.insert_one(project_doc)

                # Store final results in manager for state persistence
                manager.workflow_status[workflow_id]["results"] = workflow_result["results"]

                # Send completion message
                await websocket.send_json({
                    "type": "complete",
                    "project_id": project_id,
                    "workflow_id": workflow_id,
                    "status": workflow_result["status"],
                    "results": workflow_result["results"]
                })

            except Exception as e:
                logger.error(f"Workflow execution error: {str(e)}")

                # Update workflow state to failed
                if workflow_id in active_workflows:
                    active_workflows[workflow_id]["status"] = "failed"
                    active_workflows[workflow_id]["error"] = str(e)
                    active_workflows[workflow_id]["end_time"] = datetime.utcnow()

                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })

        # Keep connection alive
        while True:
            try:
                message = await websocket.receive_text()
                if message == "ping":
                    await websocket.send_text("pong")
            except WebSocketDisconnect:
                break

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for workflow: {workflow_id}")
        manager.disconnect(workflow_id)
    except Exception as e:
        logger.error(f"WebSocket error for workflow {workflow_id}: {str(e)}")

        # Update workflow state to failed if it was running
        if workflow_id in active_workflows and active_workflows[workflow_id]["status"] == "running":
            active_workflows[workflow_id]["status"] = "failed"
            active_workflows[workflow_id]["error"] = str(e)
            active_workflows[workflow_id]["end_time"] = datetime.utcnow()

        manager.disconnect(workflow_id)
    finally:
        # Clean up completed/failed workflows after some time (optional)
        # For now, we keep them in memory for status checking
        pass

@api_router.get("/workflow/{workflow_id}/status")
async def get_workflow_status(workflow_id: str):
    """
    Get the current status of a workflow
    """
    try:
        if workflow_id in active_workflows:
            workflow_state = active_workflows[workflow_id]
            return {
                "workflow_id": workflow_id,
                "status": workflow_state["status"],
                "project_name": workflow_state.get("project_name"),
                "start_time": workflow_state.get("start_time").isoformat() if workflow_state.get("start_time") else None,
                "end_time": workflow_state.get("end_time").isoformat() if workflow_state.get("end_time") else None,
                "error": workflow_state.get("error")
            }
        else:
            # Check database for completed workflows
            workflow = await db.workflows.find_one({"_id": workflow_id}, {"_id": 0})
            if workflow:
                return {
                    "workflow_id": workflow_id,
                    "status": workflow.get("status", "unknown"),
                    "project_name": workflow.get("project_name"),
                    "message": "Workflow found in database"
                }
            else:
                raise HTTPException(status_code=404, detail="Workflow not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching workflow status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/projects/{project_id}")
async def get_project(project_id: str):
    """
    Get project details and results
    """
    try:
        # Find project in database
        project = await db.projects.find_one({"id": project_id}, {"_id": 0})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return project
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/projects")
async def list_projects():
    """
    List all projects
    """
    try:
        projects = await db.projects.find({}, {"_id": 0}).sort("created_at", -1).to_list(100)
        return {"projects": projects, "count": len(projects)}
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/download/{project_id}/{artifact_type}")
async def download_artifact(project_id: str, artifact_type: str):
    """
    Download a specific artifact (prd or mockup)
    """
    try:
        # Get project from database
        project = await db.projects.find_one({"id": project_id}, {"_id": 0})
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get artifact path
        artifacts = project.get("artifacts", {})
        
        if artifact_type not in artifacts:
            raise HTTPException(status_code=404, detail=f"Artifact '{artifact_type}' not found")
        
        file_path = Path(artifacts[artifact_type])
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found on disk")
        
        # Determine filename and media type
        if artifact_type == "prd":
            filename = f"{project['project_name']}-PRD.md"
            media_type = "text/markdown"
        elif artifact_type == "prd_pdf":
            filename = f"{project['project_name']}-PRD.pdf"
            media_type = "application/pdf"
        elif artifact_type == "mockup":
            filename = f"{project['project_name']}-Mockup.html"
            media_type = "text/html"
        elif artifact_type == "commercial_proposal":
            filename = f"{project['project_name']}-Proposal.md"
            media_type = "text/markdown"
        elif artifact_type == "commercial_proposal_pdf":
            filename = f"{project['project_name']}-Proposal.pdf"
            media_type = "application/pdf"
        elif artifact_type == "bom_json":
            filename = f"{project['project_name']}-BOM.json"
            media_type = "application/json"
        elif artifact_type == "bom_pdf":
            filename = f"{project['project_name']}-BOM.pdf"
            media_type = "application/pdf"
        elif artifact_type == "architecture_diagram":
            filename = f"{project['project_name']}-Architecture.html"
            media_type = "text/html"
        else:
            filename = file_path.name
            media_type = "application/octet-stream"
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type=media_type
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading artifact: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()