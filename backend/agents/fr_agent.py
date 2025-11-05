"""
FR Agent - Functional Requirements Document Generator
Follows Rule 06: Functional Requirements Document Guidelines
Enhanced with comprehensive design system context integration (like PRD agent)
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .design_system import get_design_system_prompt
from .context_loader import ContextLoader
import logging
import json

logger = logging.getLogger(__name__)


class FRAgent(BaseAgent):
    """
    FR Agent creates comprehensive Functional Requirements Documents
    following AICoE rule 06 guidelines for functional requirements documentation.
    Enhanced with two-stage process (XML → HTML) like PRD agent.
    """

    def __init__(self, llm_client):
        config = AgentConfig(
            name="FRAgent",
            description="Creates comprehensive Functional Requirements Documents with comprehensive AICOE design system integration",
            model="x-ai/grok-code-fast-1",
            temperature=0.4,
            max_tokens=12000  # Increased to handle complex HTML generation
        )
        super().__init__(config, llm_client)
        # Initialize context loader for design system integration
        self.context_loader = ContextLoader()
        self.logger = logging.getLogger("fr_agent")
        
        # Rule 06: Functional Requirements Document Guidelines
        self.rule_guidelines = {
            "document_structure": [
                "Functional Overview",
                "User Stories and Use Cases",
                "Functional Specifications",
                "System Behavior Requirements",
                "Data Processing Requirements",
                "Interface Requirements",
                "Performance Requirements",
                "Security Requirements",
                "Error Handling Requirements"
            ],
            "content_requirements": {
                "user_stories": "Detailed user stories with acceptance criteria",
                "functional_specs": "Comprehensive functional specifications",
                "system_behavior": "Detailed system behavior descriptions",
                "data_processing": "Data processing and transformation requirements",
                "interface_specs": "User interface and API specifications",
                "performance_criteria": "Performance and scalability requirements",
                "security_measures": "Security and access control requirements",
                "error_handling": "Error handling and recovery procedures"
            },
            "formatting": {
                "structure": "Professional technical document format",
                "user_stories": "Format user stories with Given-When-Then structure",
                "tables": "Use tables for functional specifications",
                "diagrams": "Include system behavior diagrams",
                "aicoe_branding": "Apply AICoE design system branding"
            }
        }

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Generate comprehensive FR document as HTML

        This is a TWO-STAGE process (like PRD agent):
        Stage 1: Generate structured XML (for data storage and IP)
        Stage 2: Transform XML to beautiful HTML using LLM

        Input:
            - structured_notes: From TranscriptAgent
            - use_cases: From BlueprintAgent
            - business_requirements: From BRDAgent
            - research_insights: From ResearchAgent
            - project_name: Name of the project

        Output:
            - fr_xml: Structured XML document
            - fr_html: Beautiful HTML document
        """
        try:
            # NEW: Merge workflow context for agent collaboration
            input_data = self._merge_workflow_context(input_data)

            # NEW: Load comprehensive design system context
            design_context = self.context_loader.get_agent_context("fr_agent")
            
            self.log_execution("start", "Generating FR document with comprehensive design system integration")
            self.validate_input(input_data, ["project_name"])

            project_name = input_data["project_name"]
            structured_notes = input_data.get("structured_notes", {})
            use_cases = input_data.get("use_cases", [])
            business_requirements = input_data.get("business_requirements", {})
            research_insights = input_data.get("research_insights", {})

            # Prepare context for FR generation
            research_text = json.dumps(research_insights, indent=2) if research_insights else "No research insights available"

            self.log_execution(
                "info",
                f"Using comprehensive design system context: {len(design_context.get('design_system', ''))} chars",
            )

            context_text = f"""
Project Name: {project_name}

Structured Meeting Notes:
{json.dumps(structured_notes, indent=2)}

Use Cases:
{json.dumps(use_cases, indent=2)}

Business Requirements:
{json.dumps(business_requirements, indent=2)}

Research Insights (CRITICAL - Use this extensively):
{research_text}

**ADDITIONAL CONTEXT FOR ENHANCED FR:**
- Include detailed user stories with acceptance criteria
- Add comprehensive functional specifications
- Document system behavior requirements
- Specify data processing and transformation requirements
- Define interface requirements (UI and API)
- Set performance and scalability requirements
- Detail security and access control requirements
- Address error handling and recovery procedures
"""

            # STAGE 1: Generate XML for data storage
            xml_system_message = """## ROLE AND GOAL
You are an expert Functional Analyst creating comprehensive Functional Requirements Documents (FRDs). Your goal is to create an enterprise-grade FRD that combines functional vision, requirements, use cases, and technical specifications into a professional document.

## CONTEXT
You will receive structured data from previous agents including meeting notes, use cases, business requirements, and research insights. Use this data to create a comprehensive, professional FRD.

## STEP-BY-STEP PROCESS
1. Extract functional requirements and system behaviors from the structured meeting notes.
2. Incorporate all use cases with detailed functional flows and specifications.
3. Synthesize research insights to include technical best practices and industry standards.
4. Define comprehensive functional specifications with detailed requirements.
5. Create detailed user stories with acceptance criteria in Given-When-Then format.
6. Document system behavior requirements and workflows.
7. Specify data processing and transformation requirements.
8. Define interface requirements (both UI and API specifications).
9. Set performance and scalability requirements.
10. Detail security and access control requirements.
11. Address error handling and recovery procedures.
12. Assemble all sections into the strict XML format defined below.

## CRITICAL QUALITY REQUIREMENTS
- Include comprehensive user stories with detailed acceptance criteria
- Provide detailed functional specifications with clear requirements
- Document all system behavior requirements and workflows
- Specify data processing and transformation requirements
- Define interface requirements (UI mockups and API specifications)
- Set performance and scalability requirements
- Detail security and access control requirements
- Address error handling and recovery procedures

## OUTPUT FORMAT (CRITICAL)
Your entire response MUST be ONLY valid XML in this exact format. No explanations, no markdown, just the XML.

<functionalRequirementsDocument>
    <title>FRD for [Project Name]</title>
    <functionalOverview>A comprehensive overview of the system's functional capabilities, user interactions, and core features. Include key functional objectives and user value propositions.</functionalOverview>

    <userStories>
        <userStory id="US-001" name="User Story Name" priority="High/Medium/Low">
            <asA>As a [user type]</asA>
            <iWant>I want [functionality]</iWant>
            <soThat>So that [benefit/value]</soThat>
            <acceptanceCriteria>
                <criteria>Given [initial context] When [action] Then [expected outcome]</criteria>
                <criteria>Given [initial context] When [action] Then [expected outcome]</criteria>
            </acceptanceCriteria>
            <businessValue>Business value and importance of this story</businessValue>
            <estimation>Story points or time estimate</estimation>
        </userStory>
        <!-- Additional user stories -->
    </userStories>

    <functionalSpecifications>
        <specification id="FS-001" name="Functional Specification Name" priority="High/Medium/Low">
            <description>Detailed description of the functional requirement</description>
            <inputs>Input parameters and data required</inputs>
            <processing>Processing logic and business rules</processing>
            <outputs>Output data and deliverables produced</outputs>
            <preconditions>Conditions that must be true before execution</preconditions>
            <postconditions>State of system after successful completion</postconditions>
            <exceptions>Exception handling and error scenarios</exceptions>
        </specification>
        <!-- Additional functional specifications -->
    </functionalSpecifications>

    <systemBehavior>
        <behavior id="SB-001" name="System Behavior Name" priority="High/Medium/Low">
            <description>Description of the system behavior</description>
            <trigger>What triggers this behavior</trigger>
            <sequence>Step-by-step sequence of actions</sequence>
            <conditions>Conditions and business rules</conditions>
            <outcomes>Possible outcomes and results</outcomes>
        </behavior>
        <!-- Additional system behaviors -->
    </systemBehavior>

    <dataProcessing>
        <process id="DP-001" name="Data Processing Requirement">
            <description>Description of data processing requirement</description>
            <inputData>Input data sources and formats</inputData>
            <transformation>Data transformation and processing logic</transformation>
            <outputData>Output data formats and destinations</outputData>
            <validation>Data validation and quality checks</validation>
            <errorHandling>Error handling for data processing failures</errorHandling>
        </process>
        <!-- Additional data processing requirements -->
    </dataProcessing>

    <interfaceRequirements>
        <interface id="IF-001" name="Interface Requirement" type="UI/API">
            <description>Description of the interface requirement</description>
            <purpose>Purpose and function of the interface</purpose>
            <specifications>Detailed interface specifications</specifications>
            <interactions>User interactions and workflows</interactions>
            <accessibility>Accessibility requirements and standards</accessibility>
        </interface>
        <!-- Additional interface requirements -->
    </interfaceRequirements>

    <performanceRequirements>
        <requirement id="PR-001" name="Performance Requirement" priority="High/Medium/Low">
            <description>Description of the performance requirement</description>
            <metric>Performance metric (response time, throughput, etc.)</metric>
            <target>Target value or threshold</target>
            <measurement>How to measure and monitor</measurement>
            <conditions>Conditions under which this applies</conditions>
        </requirement>
        <!-- Additional performance requirements -->
    </performanceRequirements>

    <securityRequirements>
        <requirement id="SR-001" name="Security Requirement" priority="High/Medium/Low">
            <description>Description of the security requirement</description>
            <type>Type of security (authentication, authorization, encryption, etc.)</type>
            <specifications>Detailed security specifications</specifications>
            <compliance>Compliance standards and regulations</compliance>
        </requirement>
        <!-- Additional security requirements -->
    </securityRequirements>

    <errorHandling>
        <scenario id="EH-001" name="Error Scenario">
            <description>Description of the error scenario</description>
            <trigger>What triggers this error</trigger>
            <detection>How the error is detected</detection>
            <response>System response and user feedback</response>
            <recovery>Recovery procedures and next steps</recovery>
            <logging>Error logging and monitoring requirements</logging>
        </scenario>
        <!-- Additional error handling scenarios -->
    </errorHandling>
</functionalRequirementsDocument>
"""

            self.log_execution("llm_call", "Generating FR XML")

            xml_response = await self._call_llm(
                xml_system_message,
                f"""Generate a FRD XML document for project: {project_name}

Input Data:
{context_text}""",
                max_tokens=8000
            )

            # Clean XML response
            fr_xml = xml_response.strip()
            if fr_xml.startswith("```xml"):
                fr_xml = fr_xml.split("```xml")[1].split("```")[0].strip()
            elif fr_xml.startswith("```"):
                fr_xml = fr_xml.split("```")[1].split("```")[0].strip()

            self.log_execution("success", f"Generated FR XML ({len(fr_xml)} characters)")

            # STAGE 2: Transform XML to HTML using LLM
            # NEW: Use comprehensive design system context
            design_system = design_context.get("design_system", get_design_system_prompt())
            html_prompt_template = design_context.get("html_prompt_template", "")
            design_requirements = design_context.get("design_requirements", "")

            html_system_message = f"""## ROLE AND GOAL
You are an expert Functional Analyst and Information Designer. Your goal is to transform a raw FRD in XML format into a professional, client-ready, and interactive HTML document.

{design_system}

{design_requirements}

{html_prompt_template}

## CONTEXT
You will be given a single input: an XML string containing a `<functionalRequirementsDocument>`.

## STEP-BY-STEP PROCESS
1. Parse the input XML to identify all sections (Functional Overview, User Stories, Functional Specifications, etc.).
2. Generate a clean HTML structure that represents this document.
3. Create an interactive, smooth-scrolling Table of Contents at the top of the document that links to each major section.
4. Style the entire document with absolute precision according to the comprehensive AICOE design system above.
5. Return the final, single HTML file as a string.

## CRITICAL DESIGN SYSTEM REQUIREMENTS:
1. Use the COMPLETE AICOE design system CSS variables (copy the entire :root block)
2. Light theme colors: #FFFFFF background, #F9FAFB secondary
3. Text colors: #111827 primary, #4B5563 secondary, #6B7280 tertiary
4. Primary brand color: #2563EB for interactive elements
5. Inter font family with proper fallbacks
6. Responsive design (mobile, tablet, desktop)
7. WCAG 2.1 AA accessibility standards
8. Lucide icons exclusively
9. Minimalistic design principles

## OUTPUT FORMAT (CRITICAL)
You MUST produce a single, complete HTML string as your response. DO NOT include any other text, explanation, or formatting like markdown code fences. Your response should start with `<!DOCTYPE html>` and end with `</html>`.

## ADDITIONAL REQUIREMENTS
- Use CSS variables from the design system
- Include Lucide icons for visual enhancement
- Add smooth transitions and micro-interactions
- Ensure responsive design for all devices
- Include AICOE logo in footer with gradient effect
- Make the document visually stunning and professional
- **Interactivity:** The Table of Contents links MUST be functional and scroll smoothly to the corresponding sections.
- **Responsive:** The design must work perfectly on desktop, tablet, and mobile.
- **Print-friendly:** Include print styles for professional PDF generation.
- Follow all design system requirements exactly"""

            self.log_execution("llm_call", "Transforming XML to HTML")

            # OPTIMIZATION: Reduced max_tokens to prevent timeout during HTML generation
            html_response = await self._call_llm(
                html_system_message,
                f"""Transform this FRD XML into a beautiful, professional HTML document:

{fr_xml}""",
                max_tokens=8000  # Reduced from 12000 to prevent timeout
            )

            # Clean HTML response
            fr_html = html_response.strip()
            if fr_html.startswith("```html"):
                fr_html = fr_html.split("```html")[1].split("```")[0].strip()
            elif fr_html.startswith("```"):
                fr_html = fr_html.split("```")[1].split("```")[0].strip()

            # Validate HTML starts correctly
            if not fr_html.startswith("<!DOCTYPE"):
                self.logger.warning("Generated HTML doesn't start with DOCTYPE, prepending it")
                fr_html = "<!DOCTYPE html>\n" + fr_html

            self.log_execution("success", f"Generated FR HTML ({len(fr_html)} characters)")

            return AgentResult(
                success=True,
                data={
                    "fr_xml": fr_xml,
                    "fr_html": fr_html,
                    "project_name": project_name
                },
                metadata={
                    "agent": self.config.name,
                    "format": "xml+html"
                }
            )

        except Exception as e:
            self.logger.error(f"Error in FRAgent: {str(e)}")
            return AgentResult(
                success=False,
                data=None,
                error=str(e),
                metadata={"agent": self.config.name}
            )

    # Remove old methods - using two-stage process like PRD agent now
    pass