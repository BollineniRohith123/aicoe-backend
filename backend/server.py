from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
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

# Import multi-agent system
from agents.llm_client import LLMClient
from agents.orchestrator import OrchestratorAgent

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize LLM Client and Orchestrator
llm_client = LLMClient(
    api_key=os.getenv("EMERGENT_LLM_KEY"),
    provider="openai",
    model="gpt-4o"
)
orchestrator = OrchestratorAgent(llm_client, db)

# Storage directory for project artifacts
STORAGE_DIR = ROOT_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

# Create the main app without a prefix
app = FastAPI(title="AICOE Automation Platform API")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


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

@api_router.post("/process-transcript")
async def process_transcript(request: ProcessTranscriptRequest):
    """
    Process a meeting transcript through the multi-agent workflow
    """
    try:
        logger.info(f"Processing transcript for project: {request.project_name}")
        
        # Generate project ID
        project_id = str(uuid.uuid4())
        
        # Execute the multi-agent workflow
        workflow_result = await orchestrator.execute_workflow(
            project_name=request.project_name,
            transcript=request.transcript,
            workflow_type="full"
        )
        
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
        
        # Save Mockup if available
        if "mockup" in workflow_result.get("results", {}):
            mockup_data = workflow_result["results"]["mockup"]
            mockup_content = mockup_data.get("mockup_html", "")
            mockup_file = project_dir / "Mockup.html"
            async with aiofiles.open(mockup_file, 'w') as f:
                await f.write(mockup_content)
            artifacts["mockup"] = str(mockup_file)
        
        # Save complete workflow results
        results_file = project_dir / "workflow_results.json"
        async with aiofiles.open(results_file, 'w') as f:
            await f.write(json.dumps(workflow_result, indent=2, default=str))
        
        # Store project metadata in database
        project_doc = {
            "id": project_id,
            "project_name": request.project_name,
            "workflow_id": workflow_result["workflow_id"],
            "status": workflow_result["status"],
            "created_at": datetime.utcnow().isoformat(),
            "artifacts": artifacts,
            "results": workflow_result["results"],
            "context": workflow_result["context"]
        }
        
        await db.projects.insert_one(project_doc)
        
        logger.info(f"Successfully processed project {project_id}")
        
        return {
            "project_id": project_id,
            "project_name": request.project_name,
            "status": workflow_result["status"],
            "message": "Project processed successfully",
            "workflow_id": workflow_result["workflow_id"],
            "results": workflow_result["results"]
        }
        
    except Exception as e:
        logger.error(f"Error processing transcript: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

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
        elif artifact_type == "mockup":
            filename = f"{project['project_name']}-Mockup.html"
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