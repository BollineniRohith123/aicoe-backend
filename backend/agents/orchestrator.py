"""
Orchestrator Agent - Coordinates multi-agent workflow
Inspired by Google ADK architecture for agent orchestration
"""
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .transcript_agent import TranscriptAgent
from .researcher_agent import ResearcherAgent
from .requirements_agent import RequirementsAgent
from .prd_agent import PRDAgent
from .mockup_agent import MockupAgent
from .synthetic_data_agent import SyntheticDataAgent
from .knowledge_base_agent import KnowledgeBaseAgent
from .reviewer_agent import ReviewerAgent
from .storage_agent import StorageAgent
from .commercial_proposal_agent import CommercialProposalAgent
from .bom_agent import BOMAgent
from .architecture_diagram_agent import ArchitectureDiagramAgent
from .agent_communication import AgentCommunicationHub, Message
import logging
import asyncio
import os
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

        # Track active workflow executions to prevent duplicates
        self.active_executions = set()  # Set of workflow_ids currently executing

        # Initialize communication hub for inter-agent communication
        self.comm_hub = AgentCommunicationHub()

        # Initialize all 12 agents (including 3 new specialized agents)
        self.agents = {
            "transcript": TranscriptAgent(llm_client),
            "researcher": ResearcherAgent(llm_client),
            "requirements": RequirementsAgent(llm_client),
            "prd": PRDAgent(llm_client),
            "mockup": MockupAgent(llm_client),
            "synthetic_data": SyntheticDataAgent(llm_client),
            "knowledge_base": KnowledgeBaseAgent(llm_client),
            "reviewer": ReviewerAgent(llm_client),
            "storage": StorageAgent(llm_client),
            "commercial_proposal": CommercialProposalAgent(llm_client),
            "bom": BOMAgent(llm_client),
            "architecture_diagram": ArchitectureDiagramAgent(llm_client)
        }

        # Register all agents in the communication hub
        for agent_name, agent in self.agents.items():
            self.comm_hub.register_agent(agent_name, agent)
    
    async def execute_workflow(
        self,
        project_name: str,
        transcript: str,
        workflow_type: str = "full",
        progress_callback: Optional[callable] = None,
        max_workflow_time: int = 3600  # Maximum workflow execution time in seconds (default: 1 hour)
    ) -> Dict[str, Any]:
        """
        Execute the complete multi-agent workflow

        Args:
            project_name: Name of the project
            transcript: Raw meeting transcript
            workflow_type: "full" for all agents, or custom workflow
            progress_callback: Optional callback for progress updates
            max_workflow_time: Maximum time in seconds for workflow execution (default: 3600s = 1 hour)

        Returns:
            Dict with all agent results and workflow metadata
        """
        workflow_id = f"workflow_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        # Check if this workflow is already executing (prevent duplicate execution)
        if workflow_id in self.active_executions:
            error_msg = f"Workflow {workflow_id} is already executing. Duplicate execution prevented."
            self.logger.error(error_msg)
            return {
                "project_name": project_name,
                "workflow_id": workflow_id,
                "status": "failed",
                "error": error_msg,
                "results": {}
            }

        # Mark workflow as executing
        self.active_executions.add(workflow_id)
        self.logger.info(f"Starting workflow {workflow_id} for project: {project_name}")
        self.logger.info(f"Maximum workflow execution time: {max_workflow_time} seconds")
        self.logger.info(f"Active executions: {len(self.active_executions)}")

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

        # Track workflow start time for timeout
        workflow_start_time = datetime.utcnow()

        try:
            # Execute stages in order (respecting dependencies)
            for stage in stages:
                # Check if workflow has exceeded maximum execution time
                elapsed_time = (datetime.utcnow() - workflow_start_time).total_seconds()
                if elapsed_time > max_workflow_time:
                    error_msg = f"Workflow exceeded maximum execution time of {max_workflow_time} seconds (elapsed: {elapsed_time:.0f}s)"
                    self.logger.error(error_msg)
                    raise TimeoutError(error_msg)
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
                    
                    # Execute the agent with timeout (max 10 minutes per agent)
                    self.logger.info(f"Executing stage: {stage.name}")
                    try:
                        result = await asyncio.wait_for(
                            stage.agent.execute(stage_input, context),
                            timeout=600  # 10 minutes per agent
                        )
                    except asyncio.TimeoutError:
                        error_msg = f"Agent {stage.name} exceeded maximum execution time of 600 seconds"
                        self.logger.error(error_msg)
                        result = AgentResult(
                            success=False,
                            data={},
                            error=error_msg
                        )

                    stage.end_time = datetime.utcnow()
                    
                    if result.success:
                        stage.status = "completed"
                        stage.result = result
                        results[stage.name] = result.data

                        # Save agent output to project folder via StorageAgent
                        if stage.name != "storage":
                            await self._save_agent_output(project_name, stage.name, result.data)

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
            if self.db is not None:
                await self._store_workflow_results(final_results)

            # Remove from active executions
            self.active_executions.discard(workflow_id)
            self.logger.info(f"Workflow {workflow_id} completed. Active executions: {len(self.active_executions)}")

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

            # Remove from active executions
            self.active_executions.discard(workflow_id)
            self.logger.info(f"Workflow {workflow_id} failed. Active executions: {len(self.active_executions)}")

            return {
                "project_name": project_name,
                "workflow_id": workflow_id,
                "status": "failed",
                "error": str(e),
                "context": context,
                "results": results
            }
    
    def _define_workflow_stages(self, workflow_type: str) -> List[WorkflowStage]:
        """
        Define workflow stages based on type

        Full workflow (with 12 agents):
        1. Storage - Create project structure
        2. Transcript - Process raw transcript
        3. Researcher - Perform web research
        4. Requirements - Generate use cases (enriched with research)
        5. Knowledge Base - Enrich with domain knowledge
        6. PRD - Create comprehensive PRD
        7. Mockup - Generate Apple-style mockups
        8. Synthetic Data - Generate demo data
        9. Commercial Proposal - Generate business proposal (NEW)
        10. BOM - Generate Bill of Materials (NEW)
        11. Architecture Diagram - Generate system architecture diagrams (NEW)
        12. Reviewer - Create initial review cycle
        """
        if workflow_type == "full":
            return [
                # Stage 1: Create project structure first
                WorkflowStage("storage", self.agents["storage"]),

                # Stage 2: Process transcript
                WorkflowStage("transcript", self.agents["transcript"], ["storage"]),

                # Stage 3: Perform web research (AFTER transcript, BEFORE requirements)
                WorkflowStage("researcher", self.agents["researcher"], ["transcript"]),

                # Stage 4: Generate requirements (enriched with research insights)
                WorkflowStage("requirements", self.agents["requirements"], ["transcript", "researcher"]),

                # Stage 5: Enrich with knowledge base
                WorkflowStage("knowledge_base", self.agents["knowledge_base"], ["requirements", "researcher"]),

                # Stage 6: Create PRD (with research insights)
                WorkflowStage("prd", self.agents["prd"], ["transcript", "requirements", "knowledge_base", "researcher"]),

                # Stage 7 & 8: Generate mockups and synthetic data (can run in parallel)
                WorkflowStage("mockup", self.agents["mockup"], ["requirements", "knowledge_base"]),
                WorkflowStage("synthetic_data", self.agents["synthetic_data"], ["requirements"]),

                # Stage 9: Generate commercial proposal (depends on PRD)
                WorkflowStage("commercial_proposal", self.agents["commercial_proposal"], ["prd", "requirements", "researcher"]),

                # Stage 10: Generate Bill of Materials (depends on requirements and knowledge base)
                WorkflowStage("bom", self.agents["bom"], ["requirements", "knowledge_base", "researcher"]),

                # Stage 11: Generate architecture diagrams (depends on knowledge base)
                WorkflowStage("architecture_diagram", self.agents["architecture_diagram"], ["knowledge_base", "requirements", "researcher"]),

                # Stage 12: Create review cycle (depends on all deliverables)
                WorkflowStage("reviewer", self.agents["reviewer"], ["prd", "mockup", "synthetic_data", "commercial_proposal", "bom", "architecture_diagram"])
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
        """Prepare input data for a specific stage with inter-agent communication"""
        base_input = {"project_name": project_name}

        if stage_name == "storage":
            # Storage agent creates project structure
            base_input["action"] = "create_project"

        elif stage_name == "transcript":
            base_input["transcript"] = transcript
            # Communicate with storage agent
            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="transcript",
                message_type="request",
                content="Process transcript and share structured notes"
            ))

        elif stage_name == "researcher":
            # Researcher agent performs web research
            base_input["structured_notes"] = previous_results.get("transcript", {}).get("structured_notes", {})
            # Communicate with transcript agent
            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="researcher",
                message_type="request",
                content="Perform web research to gather industry insights"
            ))

        elif stage_name == "requirements":
            base_input["structured_notes"] = previous_results.get("transcript", {}).get("structured_notes", {})
            # Include research insights to enrich use case generation
            research_insights = previous_results.get("researcher", {}).get("research_insights", {})
            base_input["research_insights"] = research_insights

            # Validate research insights are not empty
            if not research_insights or not isinstance(research_insights, dict):
                self.logger.warning("Research insights are empty or invalid for requirements stage")
            else:
                self.logger.info(f"Passing research insights to requirements agent: {len(research_insights)} categories")

            # Communicate with transcript and researcher agents
            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="requirements",
                message_type="request",
                content=f"Generate use cases from structured notes and research insights ({len(research_insights)} research categories available)",
                metadata={"research_categories": list(research_insights.keys()) if isinstance(research_insights, dict) else []}
            ))

        elif stage_name == "knowledge_base":
            # Knowledge base enriches the requirements
            base_input["document_type"] = "requirements"
            base_input["content"] = previous_results.get("requirements", {})
            # Include research insights for additional context
            research_insights = previous_results.get("researcher", {}).get("research_insights", {})
            base_input["research_insights"] = research_insights

            # Validate research insights
            if not research_insights or not isinstance(research_insights, dict):
                self.logger.warning("Research insights are empty or invalid for knowledge_base stage")
            else:
                self.logger.info(f"Passing research insights to knowledge_base agent: {len(research_insights)} categories")

            # Communicate with requirements agent
            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="knowledge_base",
                message_type="request",
                content=f"Enrich requirements with domain knowledge and validate against research insights ({len(research_insights)} categories)",
                metadata={"research_categories": list(research_insights.keys()) if isinstance(research_insights, dict) else []}
            ))

        elif stage_name == "prd":
            base_input["structured_notes"] = previous_results.get("transcript", {}).get("structured_notes", {})
            base_input["use_cases"] = previous_results.get("requirements", {}).get("use_cases", [])
            base_input["business_requirements"] = previous_results.get("requirements", {}).get("business_requirements", {})
            base_input["enrichment"] = previous_results.get("knowledge_base", {}).get("enrichment", {})
            # Include research insights to enrich PRD with industry context
            research_insights = previous_results.get("researcher", {}).get("research_insights", {})
            base_input["research_insights"] = research_insights

            # Validate research insights
            if not research_insights or not isinstance(research_insights, dict):
                self.logger.warning("Research insights are empty or invalid for PRD stage")
            else:
                self.logger.info(f"Passing research insights to PRD agent: {len(research_insights)} categories")
                # Log specific research data being passed
                if "industry_trends" in research_insights:
                    self.logger.info(f"  - Industry trends: {len(research_insights.get('industry_trends', []))} items")
                if "competitor_insights" in research_insights:
                    self.logger.info(f"  - Competitor insights: {len(research_insights.get('competitor_insights', []))} items")

            # Communicate with multiple agents
            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="prd",
                message_type="request",
                content=f"Create comprehensive PRD with knowledge base enrichment and research insights ({len(research_insights)} categories including market analysis)",
                metadata={
                    "research_categories": list(research_insights.keys()) if isinstance(research_insights, dict) else [],
                    "has_industry_trends": "industry_trends" in research_insights,
                    "has_competitor_insights": "competitor_insights" in research_insights
                }
            ))

        elif stage_name == "mockup":
            base_input["use_cases"] = previous_results.get("requirements", {}).get("use_cases", [])
            base_input["structured_notes"] = previous_results.get("transcript", {}).get("structured_notes", {})
            base_input["enrichment"] = previous_results.get("knowledge_base", {}).get("enrichment", {})
            # Include research insights for UI/UX best practices
            research_insights = previous_results.get("researcher", {}).get("research_insights", {})
            base_input["research_insights"] = research_insights

            if research_insights and isinstance(research_insights, dict):
                self.logger.info(f"Passing research insights to mockup agent for UI/UX best practices")

            # Communicate with knowledge base
            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="mockup",
                message_type="request",
                content="Generate Apple-style mockups with AICOE branding and industry best practices",
                metadata={"has_research_insights": bool(research_insights)}
            ))

        elif stage_name == "synthetic_data":
            base_input["use_cases"] = previous_results.get("requirements", {}).get("use_cases", [])
            base_input["requirements"] = previous_results.get("requirements", {}).get("business_requirements", {})
            # Communicate with requirements agent
            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="synthetic_data",
                message_type="request",
                content="Generate realistic demo data for use cases"
            ))

        elif stage_name == "commercial_proposal":
            # Generate commercial proposal based on PRD and requirements
            base_input["prd_markdown"] = previous_results.get("prd", {}).get("prd_markdown", "")
            base_input["use_cases"] = previous_results.get("requirements", {}).get("use_cases", [])
            research_insights = previous_results.get("researcher", {}).get("research_insights", {})
            base_input["research_insights"] = research_insights

            if research_insights and isinstance(research_insights, dict):
                self.logger.info(f"Passing research insights to commercial proposal agent for pricing context")

            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="commercial_proposal",
                message_type="request",
                content="Generate professional commercial proposal with pricing and timelines",
                metadata={"has_research_insights": bool(research_insights)}
            ))

        elif stage_name == "bom":
            # Generate Bill of Materials based on requirements and architecture
            base_input["use_cases"] = previous_results.get("requirements", {}).get("use_cases", [])
            base_input["enrichment"] = previous_results.get("knowledge_base", {}).get("enrichment", {})
            research_insights = previous_results.get("researcher", {}).get("research_insights", {})
            base_input["research_insights"] = research_insights

            if research_insights and isinstance(research_insights, dict):
                self.logger.info(f"Passing research insights to BOM agent for technical standards")

            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="bom",
                message_type="request",
                content="Generate detailed Bill of Materials with cost estimates",
                metadata={"has_research_insights": bool(research_insights)}
            ))

        elif stage_name == "architecture_diagram":
            # Generate architecture diagrams based on knowledge base and requirements
            base_input["enrichment"] = previous_results.get("knowledge_base", {}).get("enrichment", {})
            base_input["use_cases"] = previous_results.get("requirements", {}).get("use_cases", [])
            research_insights = previous_results.get("researcher", {}).get("research_insights", {})
            base_input["research_insights"] = research_insights

            if research_insights and isinstance(research_insights, dict):
                self.logger.info(f"Passing research insights to architecture diagram agent for design patterns")

            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="architecture_diagram",
                message_type="request",
                content="Generate interactive system architecture diagrams",
                metadata={"has_research_insights": bool(research_insights)}
            ))

        elif stage_name == "reviewer":
            # Validate all generated HTML files for UC001 styling compliance
            base_input["action"] = "validate_all_files"
            base_input["project_name"] = project_name
            base_input["project_path"] = os.path.join("backend", "projects", project_name)

            # Communicate with all agents
            self.comm_hub.send_message(Message(
                from_agent="orchestrator",
                to_agent="reviewer",
                message_type="request",
                content="Validate all generated HTML files for UC001 styling compliance and completeness"
            ))

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
            if self.db is not None:
                await self.db.workflows.insert_one({
                    "_id": results["workflow_id"],
                    **results,
                    "created_at": datetime.utcnow()
                })
        except Exception as e:
            self.logger.error(f"Failed to store workflow results: {str(e)}")

    async def _save_agent_output(self, project_name: str, agent_name: str, data: Dict[str, Any]):
        """Save agent output to appropriate project folder via StorageAgent"""
        try:
            storage_agent = self.agents["storage"]

            # Map agent outputs to folders and filenames
            # Folder names must match the keys in ProjectStructure.folders
            file_mappings = {
                "transcript": {
                    "folder": "notes",  # Maps to MeetingNotes
                    "filename": "structured_notes.json",
                    "content": data
                },
                "researcher": {
                    "folder": "research",  # Maps to ResearchFindings
                    "filename": "research_insights.json",
                    "content": data.get("research_insights", data)
                },
                "requirements": {
                    "folder": "use_cases",  # Maps to UseCases
                    "filename": "use_cases.json",
                    "content": data
                },
                "knowledge_base": {
                    "folder": "architecture",  # Maps to SystemArchitecture
                    "filename": "knowledge_enrichment.json",
                    "content": data
                },
                "prd": {
                    "folder": "prd",  # Maps to PRDDocuments
                    "filename": "PRD_v1.md",
                    "content": data.get("prd_markdown", str(data))
                },
                "prd_html": {
                    "folder": "prd",  # Maps to PRDDocuments
                    "filename": "PRD_v1.html",
                    "content": data.get("prd_html", "")
                },
                "mockup": {
                    "folder": "mockups",  # Maps to HTML/Version1/Mockups
                    "filename": "index.html",  # Changed from mockup_v1.html to index.html
                    "content": data.get("mockup_html", str(data))
                },
                "synthetic_data": {
                    "folder": "synthetic_data",  # Maps to SyntheticData
                    "filename": "demo_data.json",
                    "content": data
                },
                "commercial_proposal": {
                    "folder": "commercial_proposals",  # Maps to CommercialProposals
                    "filename": "proposal_v1.md",
                    "content": data.get("proposal_markdown", str(data))
                },
                "commercial_proposal_html": {
                    "folder": "commercial_proposals",  # Maps to CommercialProposals
                    "filename": "proposal_v1.html",
                    "content": data.get("proposal_html", "")
                },
                "bom": {
                    "folder": "bom",  # Maps to BillOfMaterials
                    "filename": "bom_v1.json",
                    "content": data.get("bom_json", data)
                },
                "bom_html": {
                    "folder": "bom",  # Maps to BillOfMaterials
                    "filename": "bom_v1.html",
                    "content": data.get("bom_html", "")
                },
                "architecture_diagram": {
                    "folder": "architecture",  # Maps to SystemArchitecture
                    "filename": "architecture_diagram_v1.html",
                    "content": data.get("architecture_html", str(data))
                },
                "reviewer": {
                    "folder": "feedback",  # Maps to ReviewerFeedback
                    "filename": "review_cycle_v1.json",
                    "content": data
                }
            }

            if agent_name in file_mappings:
                mapping = file_mappings[agent_name]

                # Save file via StorageAgent
                save_input = {
                    "action": "save_file",
                    "project_name": project_name,
                    "folder": mapping["folder"],
                    "filename": mapping["filename"],
                    "content": mapping["content"]
                }

                result = await storage_agent.execute(save_input, {})

                if result.success:
                    self.logger.info(f"Saved {agent_name} output to {mapping['folder']}/{mapping['filename']}")
                else:
                    self.logger.warning(f"Failed to save {agent_name} output: {result.error}")

            # Special handling for agents that generate both MD/JSON and HTML versions
            if agent_name == "prd" and "prd_html" in data:
                html_mapping = file_mappings.get("prd_html")
                if html_mapping:
                    html_save_input = {
                        "action": "save_file",
                        "project_name": project_name,
                        "folder": html_mapping["folder"],
                        "filename": html_mapping["filename"],
                        "content": data["prd_html"]
                    }
                    html_result = await storage_agent.execute(html_save_input, {})
                    if html_result.success:
                        self.logger.info(f"Saved PRD HTML to {html_mapping['folder']}/{html_mapping['filename']}")
                    else:
                        self.logger.warning(f"Failed to save PRD HTML: {html_result.error}")

            # Save commercial proposal HTML
            if agent_name == "commercial_proposal" and "proposal_html" in data:
                html_mapping = file_mappings.get("commercial_proposal_html")
                if html_mapping:
                    html_save_input = {
                        "action": "save_file",
                        "project_name": project_name,
                        "folder": html_mapping["folder"],
                        "filename": html_mapping["filename"],
                        "content": data["proposal_html"]
                    }
                    html_result = await storage_agent.execute(html_save_input, {})
                    if html_result.success:
                        self.logger.info(f"Saved Proposal HTML to {html_mapping['folder']}/{html_mapping['filename']}")
                    else:
                        self.logger.warning(f"Failed to save Proposal HTML: {html_result.error}")

            # Save BOM HTML
            if agent_name == "bom" and "bom_html" in data:
                html_mapping = file_mappings.get("bom_html")
                if html_mapping:
                    html_save_input = {
                        "action": "save_file",
                        "project_name": project_name,
                        "folder": html_mapping["folder"],
                        "filename": html_mapping["filename"],
                        "content": data["bom_html"]
                    }
                    html_result = await storage_agent.execute(html_save_input, {})
                    if html_result.success:
                        self.logger.info(f"Saved BOM HTML to {html_mapping['folder']}/{html_mapping['filename']}")
                    else:
                        self.logger.warning(f"Failed to save BOM HTML: {html_result.error}")

            # Save additional mockup pages (multi-page prototypes)
            if agent_name == "mockup" and "mockup_pages" in data:
                mockup_pages = data.get("mockup_pages", {})
                if isinstance(mockup_pages, dict):
                    for page_name, page_content in mockup_pages.items():
                        if page_name != "index.html":  # index.html already saved
                            page_save_input = {
                                "action": "save_file",
                                "project_name": project_name,
                                "folder": "mockups",
                                "filename": page_name,
                                "content": page_content
                            }
                            page_result = await storage_agent.execute(page_save_input, {})
                            if page_result.success:
                                self.logger.info(f"Saved mockup page: mockups/{page_name}")
                            else:
                                self.logger.warning(f"Failed to save mockup page {page_name}: {page_result.error}")

        except Exception as e:
            self.logger.error(f"Error saving {agent_name} output: {str(e)}")
