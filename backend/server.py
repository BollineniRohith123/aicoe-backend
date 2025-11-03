from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import uvicorn
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import agents
from agents.orchestrator import OrchestratorAgent
from agents.agent_communication import AgentCommunicationHub
from agents.storage_agent import StorageAgent
from agents.researcher_agent import ResearcherAgent
from agents.prd_agent import PRDAgent
from agents.architecture_agent import ArchitectureAgent
from agents.mockup_agent import MockupAgent
from agents.proposal_agent import ProposalAgent
from agents.reviewer_agent import ReviewerAgent
from agents.knowledge_base_agent import KnowledgeBaseAgent
from agents.bom_agent import BOMAgent
from agents.data_agent import DataAgent
from agents.blueprint_agent import BlueprintAgent
from agents.gallery_agent import CaseStudyGalleryAgent
from agents.intake_agent import IntakeAgent
from agents.llm_client import LLMClient

app = FastAPI(
    title="AICOE Automation Platform",
    description="AI Center of Excellence - Intelligent Project Automation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM client
llm_client = LLMClient()

# Initialize agents
orchestrator = OrchestratorAgent(llm_client)

# Initialize individual agents (for direct access if needed)
agent_comm = AgentCommunicationHub()
storage_agent = StorageAgent(llm_client, base_storage_path="storage")
researcher_agent = ResearcherAgent(llm_client)
prd_agent = PRDAgent(llm_client)
architecture_agent = ArchitectureAgent(llm_client)
mockup_agent = MockupAgent(llm_client)
proposal_agent = ProposalAgent(llm_client)
reviewer_agent = ReviewerAgent(llm_client)
knowledge_base_agent = KnowledgeBaseAgent(llm_client)
bom_agent = BOMAgent(llm_client)
data_agent = DataAgent(llm_client)
blueprint_agent = BlueprintAgent(llm_client)
gallery_agent = CaseStudyGalleryAgent(llm_client)
intake_agent = IntakeAgent(llm_client)

# Pydantic models
class ProjectRequest(BaseModel):
    project_name: str
    description: str
    requirements: Optional[str] = None
    industry: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None

class TranscriptRequest(BaseModel):
    transcript: str
    project_id: Optional[str] = None

class AgentStatus(BaseModel):
    agent_name: str
    status: str
    progress: float
    message: Optional[str] = None

class ProjectStatus(BaseModel):
    project_id: str
    status: str
    progress: float
    current_agent: Optional[str] = None
    agents_status: List[AgentStatus]
    created_at: datetime
    updated_at: datetime

# Routes
@app.get("/")
async def root():
    return {
        "message": "AICOE Automation Platform API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/api/projects/create")
async def create_project(request: ProjectRequest, background_tasks: BackgroundTasks):
    try:
        # Create project using orchestrator
        project_id = await orchestrator.create_project(
            name=request.project_name,
            description=request.description,
            requirements=request.requirements,
            industry=request.industry,
            budget=request.budget,
            timeline=request.timeline
        )

        # Start background processing
        background_tasks.add_task(process_project, project_id)

        return {
            "project_id": project_id,
            "status": "created",
            "message": "Project created successfully. Processing started."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects/{project_id}/status")
async def get_project_status(project_id: str):
    try:
        status = await orchestrator.get_project_status(project_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Project not found: {str(e)}")

@app.get("/api/projects")
async def list_projects():
    try:
        projects = await storage_agent.list_projects()
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transcript/process")
async def process_transcript(request: TranscriptRequest, background_tasks: BackgroundTasks):
    try:
        # Process transcript using intake agent
        result = await intake_agent.process_transcript(
            transcript=request.transcript,
            project_id=request.project_id
        )

        if request.project_id:
            # Start background processing for existing project
            background_tasks.add_task(process_project, request.project_id)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/status")
async def get_agents_status():
    try:
        # Get status of all agents
        agents_status = agent_comm.get_all_agents_status()
        return {"agents": agents_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Background task function
async def process_project(project_id: str):
    try:
        await orchestrator.process_project(project_id)
    except Exception as e:
        print(f"Error processing project {project_id}: {str(e)}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": True,
        "message": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "error": True,
        "message": "Internal server error",
        "details": str(exc)
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
