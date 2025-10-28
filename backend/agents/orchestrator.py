"""
Orchestrator Agent - Coordinates multi-agent workflow
Inspired by Google ADK architecture for agent orchestration
"""
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .transcript_agent import TranscriptAgent
from .requirements_agent import RequirementsAgent
from .prd_agent import PRDAgent
from .mockup_agent import MockupAgent
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)


class WorkflowStage:
    """Represents a stage in the workflow"""
    def __init__(self, name: str, agent: BaseAgent, depends_on: List[str] = None):
        self.name = name
        self.agent = agent
        self.depends_on = depends_on or []
        self.status = "pending"  # pending, running, completed, failed
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None


class OrchestratorAgent:
    """
    Orchestrator Agent coordinates the execution of multiple specialized agents
    Implements Google ADK-style multi-agent orchestration:
    - Sequential and parallel execution
    - Dependency management
    - Error handling and recovery
    - State management
    - Progress tracking
    """
    
    def __init__(self, llm_client, db=None):
        self.llm_client = llm_client
        self.db = db
        self.logger = logging.getLogger("orchestrator")
        
        # Initialize all agents
        self.agents = {
            "transcript": TranscriptAgent(llm_client),
            "requirements": RequirementsAgent(llm_client),
            "prd": PRDAgent(llm_client),
            "mockup": MockupAgent(llm_client)
        }
    
    async def execute_workflow(
        self,
        project_name: str,
        transcript: str,
        workflow_type: str = "full",
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Execute the complete multi-agent workflow
        
        Args:
            project_name: Name of the project
            transcript: Raw meeting transcript
            workflow_type: "full" for all agents, or custom workflow
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dict with all agent results and workflow metadata
        """
        workflow_id = f"workflow_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        self.logger.info(f"Starting workflow {workflow_id} for project: {project_name}")
        
        # Define workflow stages with dependencies
        stages = self._define_workflow_stages(workflow_type)
        
        # Shared context across agents
        context = {
            "project_name": project_name,
            "workflow_id": workflow_id,
            "workflow_type": workflow_type,
            "start_time": datetime.utcnow().isoformat()
        }
        
        # Results storage
        results = {}
        
        try:
            # Execute stages in order (respecting dependencies)
            for stage in stages:
                try:
                    await self._report_progress(
                        progress_callback,
                        stage.name,
                        "running",
                        f"Executing {stage.name}..."
                    )
                    
                    stage.status = "running"
                    stage.start_time = datetime.utcnow()
                    
                    # Prepare input for this stage
                    stage_input = self._prepare_stage_input(
                        stage.name,
                        project_name,
                        transcript,
                        results
                    )
                    
                    # Execute the agent
                    self.logger.info(f"Executing stage: {stage.name}")
                    result = await stage.agent.execute(stage_input, context)
                    
                    stage.end_time = datetime.utcnow()
                    
                    if result.success:
                        stage.status = "completed"
                        stage.result = result
                        results[stage.name] = result.data
                        
                        await self._report_progress(
                            progress_callback,
                            stage.name,
                            "completed",
                            f"{stage.name} completed successfully"
                        )
                    else:
                        stage.status = "failed"
                        stage.error = result.error
                        self.logger.error(f"Stage {stage.name} failed: {result.error}")
                        
                        await self._report_progress(
                            progress_callback,
                            stage.name,
                            "failed",
                            f"{stage.name} failed: {result.error}"
                        )
                        
                        # Decide whether to continue or stop
                        if stage.name in ["transcript", "requirements"]:
                            # Critical stages - stop workflow
                            raise Exception(f"Critical stage {stage.name} failed: {result.error}")
                        # Non-critical stages - continue with partial results
                        
                except Exception as e:
                    stage.status = "failed"
                    stage.error = str(e)
                    self.logger.error(f"Error executing stage {stage.name}: {str(e)}")
                    
                    await self._report_progress(
                        progress_callback,
                        stage.name,
                        "failed",
                        f"Error: {str(e)}"
                    )
                    
                    # Stop workflow on critical errors
                    if stage.name in ["transcript", "requirements"]:
                        raise
            
            # Workflow completed
            context["end_time"] = datetime.utcnow().isoformat()
            context["status"] = "completed"
            
            await self._report_progress(
                progress_callback,
                "workflow",
                "completed",
                "All stages completed successfully"
            )
            
            # Compile final results
            final_results = {
                "project_name": project_name,
                "workflow_id": workflow_id,
                "status": "success",
                "context": context,
                "results": results,
                "stages": [
                    {
                        "name": s.name,
                        "status": s.status,
                        "duration": (
                            (s.end_time - s.start_time).total_seconds()
                            if s.start_time and s.end_time else None
                        )
                    }
                    for s in stages
                ]
            }
            
            # Store in database if available
            if self.db:
                await self._store_workflow_results(final_results)
            
            return final_results
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {str(e)}")
            context["end_time"] = datetime.utcnow().isoformat()
            context["status"] = "failed"
            context["error"] = str(e)
            
            await self._report_progress(
                progress_callback,
                "workflow",
                "failed",
                f"Workflow failed: {str(e)}"
            )
            
            return {
                "project_name": project_name,
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e),
                "context": context,
                "results": results
            }
    
    def _define_workflow_stages(self, workflow_type: str) -> List[WorkflowStage]:
        """Define workflow stages based on type"""
        if workflow_type == "full":
            return [
                WorkflowStage("transcript", self.agents["transcript"]),
                WorkflowStage("requirements", self.agents["requirements"], ["transcript"]),
                WorkflowStage("prd", self.agents["prd"], ["transcript", "requirements"]),
                WorkflowStage("mockup", self.agents["mockup"], ["requirements"])
            ]
        else:
            # Default to full workflow
            return self._define_workflow_stages("full")
    
    def _prepare_stage_input(
        self,
        stage_name: str,
        project_name: str,
        transcript: str,
        previous_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare input data for a specific stage"""
        base_input = {"project_name": project_name}
        
        if stage_name == "transcript":
            base_input["transcript"] = transcript
            
        elif stage_name == "requirements":
            base_input["structured_notes"] = previous_results.get("transcript", {}).get("structured_notes", {})
            
        elif stage_name == "prd":
            base_input["structured_notes"] = previous_results.get("transcript", {}).get("structured_notes", {})
            base_input["use_cases"] = previous_results.get("requirements", {}).get("use_cases", [])
            base_input["business_requirements"] = previous_results.get("requirements", {}).get("business_requirements", {})
            
        elif stage_name == "mockup":
            base_input["use_cases"] = previous_results.get("requirements", {}).get("use_cases", [])
            base_input["structured_notes"] = previous_results.get("transcript", {}).get("structured_notes", {})
        
        return base_input
    
    async def _report_progress(
        self,
        callback: Optional[callable],
        stage: str,
        status: str,
        message: str
    ):
        """Report progress to callback if provided"""
        if callback:
            try:
                await callback({
                    "stage": stage,
                    "status": status,
                    "message": message,
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                self.logger.warning(f"Progress callback failed: {str(e)}")
    
    async def _store_workflow_results(self, results: Dict[str, Any]):
        """Store workflow results in database"""
        try:
            if self.db:
                await self.db.workflows.insert_one({
                    "_id": results["workflow_id"],
                    **results,
                    "created_at": datetime.utcnow()
                })
        except Exception as e:
            self.logger.error(f"Failed to store workflow results: {str(e)}")
