"""
Workflow Context System
Provides shared context across all agents for better collaboration and consistency
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


class WorkflowContext:
    """
    Centralized context shared across all agents in a workflow.
    Enables agents to access outputs from all previous agents and maintain consistency.
    """
    
    def __init__(self, project_name: str, transcript: str):
        """
        Initialize workflow context
        
        Args:
            project_name: Name of the project
            transcript: Original meeting transcript
        """
        self.project_name = project_name
        self.safe_project_name = self._sanitize_project_name(project_name)
        self.transcript = transcript
        self.agent_outputs: Dict[str, Any] = {}
        self.shared_insights: Dict[str, Any] = {}
        self.metadata: Dict[str, Any] = {
            "created_at": datetime.utcnow().isoformat(),
            "workflow_version": "2.0",
            "agents_completed": []
        }
        
        # Design system and HTML generation guidelines
        self.design_guidelines = self._load_design_system()
        self.html_generation_prompt = self._create_html_generation_prompt()
        
        logger.info(f"WorkflowContext initialized for project: {project_name} (safe: {self.safe_project_name})")
    
    def _sanitize_project_name(self, name: str) -> str:
        """
        Convert project name to filesystem-safe format
        
        Args:
            name: Original project name
            
        Returns:
            Sanitized project name safe for filesystem
        """
        # Replace spaces with underscores
        safe_name = name.replace(" ", "_")
        # Remove any other problematic characters
        safe_name = "".join(c for c in safe_name if c.isalnum() or c in "_-")
        return safe_name
    
    def _load_design_system(self) -> str:
        """Load AICOE design system guidelines"""
        try:
            from .design_system import get_design_system_prompt
            return get_design_system_prompt()
        except Exception as e:
            logger.warning(f"Could not load design system: {e}")
            return self._get_default_design_system()
    
    def _get_default_design_system(self) -> str:
        """Fallback design system if design_system.py not available"""
        return """
# AICOE Design System

## Colors
- Primary Navy: #1a1a2e
- Accent Pink: #ff69b4
- Accent Cyan: #00ffcc
- Accent Turquoise: #00e5b3

## Typography
- Font Family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif
- Fluid Typography: Use clamp() for responsive sizing

## Spacing
- Use 8px grid system
- Consistent padding and margins

## Components
- Card-based layouts
- Smooth transitions and animations
- Apple-inspired design principles
"""
    
    def _create_html_generation_prompt(self) -> str:
        """Create unified HTML generation prompt for all agents"""
        return """
**CRITICAL: HTML GENERATION CONSISTENCY REQUIREMENTS**

You MUST generate HTML that is visually consistent with all other agents' outputs.

**DESIGN SYSTEM (MANDATORY):**
{design_guidelines}

**CONSISTENCY CHECKLIST:**
✅ Use EXACT same AICOE color palette (#1a1a2e, #ff69b4, #00ffcc, #00e5b3)
✅ Use EXACT same font family (-apple-system, BlinkMacSystemFont, "SF Pro Display")
✅ Use EXACT same spacing system (8px grid)
✅ Use EXACT same card component styles
✅ Use EXACT same header/footer structure
✅ Use EXACT same animation styles
✅ Include Lucide icons for visual consistency
✅ Follow Apple-inspired design principles

**PREVIOUS AGENT OUTPUTS (FOR REFERENCE):**
{previous_outputs_summary}

**YOUR HTML MUST:**
1. Match the visual style of previous outputs
2. Use the same CSS classes and structure
3. Maintain the same level of polish and detail
4. Follow the same layout patterns
5. Use consistent component styling

Generate HTML that looks like it was created by the same designer as all other pages.
"""
    
    def add_agent_output(self, agent_name: str, output: Dict[str, Any]):
        """
        Store agent output for other agents to access
        
        Args:
            agent_name: Name of the agent
            output: Agent's output data
        """
        self.agent_outputs[agent_name] = {
            "data": output,
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent_name
        }
        self.metadata["agents_completed"].append(agent_name)
        
        logger.info(f"Added output from {agent_name} to workflow context")
        
        # Extract and store key insights for cross-agent use
        self._extract_insights(agent_name, output)
    
    def _extract_insights(self, agent_name: str, output: Dict[str, Any]):
        """Extract key insights from agent output for sharing"""
        insights = {}
        
        # Extract based on agent type
        if agent_name == "transcript":
            insights["key_requirements"] = output.get("structured_notes", {}).get("requirements", [])
            insights["technical_constraints"] = output.get("structured_notes", {}).get("technical_constraints", [])
            
        elif agent_name == "researcher":
            insights["industry_trends"] = output.get("research_insights", {}).get("industry_trends", [])
            insights["competitor_insights"] = output.get("research_insights", {}).get("competitor_insights", [])
            
        elif agent_name == "requirements":
            insights["use_cases"] = output.get("use_cases", [])
            insights["business_requirements"] = output.get("business_requirements", {})
            
        elif agent_name == "prd":
            insights["product_vision"] = output.get("prd_content", "")
            insights["technical_stack"] = output.get("technical_stack", {})
        
        if insights:
            self.shared_insights[agent_name] = insights
            logger.info(f"Extracted {len(insights)} insights from {agent_name}")
    
    def get_agent_output(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """
        Get output from a specific agent
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Agent output data or None if not found
        """
        agent_data = self.agent_outputs.get(agent_name)
        return agent_data["data"] if agent_data else None
    
    def get_all_outputs(self) -> Dict[str, Any]:
        """Get all agent outputs"""
        return {name: data["data"] for name, data in self.agent_outputs.items()}
    
    def get_full_context(self, current_agent: str = None) -> Dict[str, Any]:
        """
        Get complete context for an agent
        
        Args:
            current_agent: Name of the current agent (optional)
            
        Returns:
            Full workflow context
        """
        context = {
            "project_name": self.project_name,
            "safe_project_name": self.safe_project_name,
            "transcript": self.transcript,
            "all_agent_outputs": self.get_all_outputs(),
            "shared_insights": self.shared_insights,
            "design_guidelines": self.design_guidelines,
            "html_generation_prompt": self._format_html_prompt(),
            "metadata": self.metadata
        }
        
        if current_agent:
            context["current_agent"] = current_agent
            context["previous_agents"] = self.metadata["agents_completed"]
        
        return context
    
    def _format_html_prompt(self) -> str:
        """Format HTML generation prompt with current context"""
        # Create summary of previous outputs for consistency
        previous_summary = self._create_previous_outputs_summary()
        
        return self.html_generation_prompt.format(
            design_guidelines=self.design_guidelines,
            previous_outputs_summary=previous_summary
        )
    
    def _create_previous_outputs_summary(self) -> str:
        """Create a summary of previous agent outputs for consistency reference"""
        summary_parts = []
        
        for agent_name in self.metadata["agents_completed"]:
            output = self.get_agent_output(agent_name)
            if output:
                # Summarize what this agent generated
                summary_parts.append(f"- {agent_name}: Generated {self._summarize_output(output)}")
        
        return "\n".join(summary_parts) if summary_parts else "No previous outputs yet"
    
    def _summarize_output(self, output: Dict[str, Any]) -> str:
        """Create a brief summary of agent output"""
        summaries = []
        
        if "structured_notes" in output:
            summaries.append("structured notes")
        if "research_insights" in output:
            summaries.append("research insights")
        if "use_cases" in output:
            summaries.append(f"{len(output['use_cases'])} use cases")
        if "prd_content" in output:
            summaries.append("PRD document")
        if "mockup_html" in output:
            summaries.append("mockup pages")
        if "bom_xml" in output:
            summaries.append("BOM")
        if "architecture_xml" in output:
            summaries.append("architecture diagram")
        
        return ", ".join(summaries) if summaries else "output data"
    
    def get_shared_insight(self, insight_key: str) -> Optional[Any]:
        """
        Get a specific shared insight
        
        Args:
            insight_key: Key for the insight (e.g., "use_cases", "industry_trends")
            
        Returns:
            Insight data or None
        """
        for agent_insights in self.shared_insights.values():
            if insight_key in agent_insights:
                return agent_insights[insight_key]
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert workflow context to dictionary for serialization"""
        return {
            "project_name": self.project_name,
            "safe_project_name": self.safe_project_name,
            "agent_outputs": self.agent_outputs,
            "shared_insights": self.shared_insights,
            "metadata": self.metadata
        }
    
    def __repr__(self) -> str:
        return f"WorkflowContext(project={self.project_name}, agents_completed={len(self.metadata['agents_completed'])})"

