"""
BRD Agent - Business Requirements Document Generator
Follows Rule 05: Business Requirements Document Guidelines
Enhanced with comprehensive design system context integration (like PRD agent)
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .design_system import get_design_system_prompt
from .context_loader import ContextLoader
import logging
import json

logger = logging.getLogger(__name__)


class BRDAgent(BaseAgent):
    """
    BRD Agent creates comprehensive Business Requirements Documents
    following AICoE rule 05 guidelines for business requirements documentation.
    Enhanced with two-stage process (XML → HTML) like PRD agent.
    """

    def __init__(self, llm_client):
        config = AgentConfig(
            name="BRDAgent",
            description="Creates comprehensive Business Requirements Documents with comprehensive AICOE design system integration",
            model="x-ai/grok-code-fast-1",
            temperature=0.4,
            max_tokens=12000  # Increased to handle complex HTML generation
        )
        super().__init__(config, llm_client)
        # Initialize context loader for design system integration
        self.context_loader = ContextLoader()
        self.logger = logging.getLogger("brd_agent")
        
        # Rule 05: Business Requirements Document Guidelines
        self.rule_guidelines = {
            "document_structure": [
                "Executive Summary",
                "Business Objectives",
                "Stakeholder Analysis",
                "Business Rules",
                "Process Requirements",
                "Data Requirements",
                "Integration Requirements",
                "Compliance Requirements",
                "Success Metrics"
            ],
            "content_requirements": {
                "business_context": "Clear explanation of business problem and opportunity",
                "stakeholder_mapping": "Detailed stakeholder analysis with roles and responsibilities",
                "business_rules": "Comprehensive list of business rules and constraints",
                "process_flows": "Business process descriptions and workflows",
                "data_requirements": "Business data needs and data flow requirements",
                "integration_points": "External system integration requirements",
                "compliance_needs": "Regulatory and compliance requirements",
                "success_criteria": "Measurable business success criteria"
            },
            "formatting": {
                "structure": "Professional business document format",
                "sections": "Clear section headers and numbering",
                "tables": "Use tables for stakeholder analysis and requirements",
                "diagrams": "Include business process diagrams where applicable",
                "aicoe_branding": "Apply AICoE design system branding"
            }
        }

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Generate comprehensive BRD document as HTML

        This is a TWO-STAGE process (like PRD agent):
        Stage 1: Generate structured XML (for data storage and IP)
        Stage 2: Transform XML to beautiful HTML using LLM

        Input:
            - structured_notes: From TranscriptAgent
            - use_cases: From RequirementsAgent
            - research_insights: From ResearchAgent
            - project_name: Name of the project

        Output:
            - brd_xml: Structured XML document
            - brd_html: Beautiful HTML document
        """
        try:
            # NEW: Merge workflow context for agent collaboration
            input_data = self._merge_workflow_context(input_data)

            # NEW: Load comprehensive design system context
            design_context = self.context_loader.get_agent_context("brd_agent")
            
            self.log_execution("start", "Generating BRD document with comprehensive design system integration")
            self.validate_input(input_data, ["project_name"])

            project_name = input_data["project_name"]
            structured_notes = input_data.get("structured_notes", {})
            use_cases = input_data.get("use_cases", [])
            research_insights = input_data.get("research_insights", {})

            # Prepare context for BRD generation
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

Research Insights (CRITICAL - Use this extensively):
{research_text}

**ADDITIONAL CONTEXT FOR ENHANCED BRD:**
- Include comprehensive stakeholder analysis with roles and responsibilities
- Add detailed business rules and constraints
- Document process requirements and workflows
- Specify data requirements and business data flows
- Define integration requirements with external systems
- Address compliance and regulatory requirements
- Set measurable success criteria and KPIs
"""

            # STAGE 1: Generate XML for data storage
            xml_system_message = """## ROLE AND GOAL
You are an expert Business Analyst creating comprehensive Business Requirements Documents (BRDs). Your goal is to create an enterprise-grade BRD that combines business vision, requirements, use cases, and industry research into a professional document.

## CONTEXT
You will receive structured data from previous agents including meeting notes, use cases, and research insights. Use this data to create a comprehensive, professional BRD.

## STEP-BY-STEP PROCESS
1. Extract the business vision, objectives, and stakeholders from the structured meeting notes.
2. Incorporate all use cases with their business impact and value propositions.
3. Synthesize research insights to include market context and industry trends.
4. Define comprehensive business goals with measurable KPIs and success metrics.
5. Create detailed stakeholder analysis with roles, responsibilities, and influence levels.
6. Document comprehensive business rules and constraints.
7. Specify process requirements and business workflows.
8. Define data requirements and business data flows.
9. Document integration requirements with external systems and APIs.
10. Address compliance and regulatory requirements.
11. Set measurable success criteria and KPIs.
12. Assemble all sections into the strict XML format defined below.

## CRITICAL QUALITY REQUIREMENTS
- Include comprehensive stakeholder analysis with RACI matrix
- Provide detailed business rules and constraints documentation
- Document all process requirements and workflows clearly
- Specify data requirements and business data flows
- Define integration requirements with external systems
- Address compliance and regulatory requirements
- Set measurable success criteria and KPIs

## OUTPUT FORMAT (CRITICAL)
Your entire response MUST be ONLY valid XML in this exact format. No explanations, no markdown, just the XML.

<businessRequirementsDocument>
    <title>BRD for [Project Name]</title>
    <executiveSummary>A comprehensive paragraph summarizing the business purpose, scope, objectives, and strategic importance. Include key success metrics and business value proposition.</executiveSummary>

    <businessObjectives>
        <primaryObjectives>Primary business objectives with specific, measurable goals and timelines.</primaryObjectives>
        <keyPerformanceIndicators>
            <kpi name="business_value" target="measurable business outcome" timeframe="timeframe" measurement="measurement method">
                <description>How to measure and track business value</description>
            </kpi>
            <kpi name="stakeholder_satisfaction" target="satisfaction target" timeframe="timeframe" measurement="measurement method">
                <description>Stakeholder satisfaction and engagement metrics</description>
            </kpi>
        </keyPerformanceIndicators>
        <successMetrics>
            <metric name="business_impact" target="impact target" measurement="measurement method">
                <trackingMethod>How to track and measure business impact</trackingMethod>
            </metric>
        </successMetrics>
    </businessObjectives>

    <stakeholderAnalysis>
        <stakeholder id="STAKEHOLDER-001" name="Stakeholder Name" role="Role/Title" influence="High/Medium/Low" interest="High/Medium/Low">
            <responsibilities>Key responsibilities and duties</responsibilities>
            <requirements>Specific requirements from this stakeholder</requirements>
            <communicationPlan>How and when to communicate with this stakeholder</communicationPlan>
        </stakeholder>
        <!-- Additional stakeholders follow the same structure -->
    </stakeholderAnalysis>

    <businessRules>
        <rule id="BR-001" name="Business Rule Name" priority="High/Medium/Low">
            <description>Detailed description of the business rule</description>
            <rationale>Why this rule exists and its business justification</rationale>
            <impact>Impact on business processes and systems</impact>
            <exceptions>Known exceptions or special cases</exceptions>
        </rule>
        <!-- Additional business rules -->
    </businessRules>

    <processRequirements>
        <process id="PROC-001" name="Process Name" priority="High/Medium/Low">
            <description>Overview of the business process</description>
            <objectives>What the process aims to achieve</objectives>
            <steps>
                <step number="1">First step in the process</step>
                <step number="2">Second step in the process</step>
                <!-- Continue with all steps -->
            </steps>
            <inputs>Input data and resources required</inputs>
            <outputs>Output data and deliverables produced</outputs>
            <stakeholders>Roles involved in this process</stakeholders>
        </process>
        <!-- Additional processes -->
    </processRequirements>

    <dataRequirements>
        <dataEntity id="DATA-001" name="Data Entity Name">
            <description>Description of the data entity</description>
            <attributes>
                <attribute name="attribute_name" type="data_type" required="true/false">
                    <description>Description of the attribute</description>
                </attribute>
            </attributes>
            <relationships>How this entity relates to other entities</relationships>
            <businessRules>Data-specific business rules</businessRules>
        </dataEntity>
        <!-- Additional data entities -->
    </dataRequirements>

    <integrationRequirements>
        <integration id="INT-001" name="Integration Name" priority="High/Medium/Low">
            <description>Description of the integration requirement</description>
            <system>External system or service to integrate with</system>
            <purpose>Business purpose of the integration</purpose>
            <dataExchange>Data that needs to be exchanged</dataExchange>
            <frequency>How often the integration occurs</frequency>
            <security>Security requirements for the integration</security>
        </integration>
        <!-- Additional integrations -->
    </integrationRequirements>

    <complianceRequirements>
        <requirement id="COMP-001" name="Compliance Requirement" priority="High/Medium/Low">
            <description>Description of the compliance requirement</description>
            <regulation>Applicable regulation or standard</regulation>
            <impact>Impact on business processes</impact>
            <implementation>How to implement compliance</implementation>
        </requirement>
        <!-- Additional compliance requirements -->
    </complianceRequirements>

    <successCriteria>
        <criterion id="SC-001" name="Success Criterion" priority="High/Medium/Low">
            <description>Description of the success criterion</description>
            <measurement>How to measure success</measurement>
            <target>Target value or outcome</target>
            <timeframe>When success should be achieved</timeframe>
        </criterion>
        <!-- Additional success criteria -->
    </successCriteria>
</businessRequirementsDocument>
"""

            self.log_execution("llm_call", "Generating BRD XML")

            xml_response = await self._call_llm(
                xml_system_message,
                f"""Generate a BRD XML document for project: {project_name}

Input Data:
{context_text}""",
                max_tokens=8000
            )

            # Clean XML response
            brd_xml = xml_response.strip()
            if brd_xml.startswith("```xml"):
                brd_xml = brd_xml.split("```xml")[1].split("```")[0].strip()
            elif brd_xml.startswith("```"):
                brd_xml = brd_xml.split("```")[1].split("```")[0].strip()

            self.log_execution("success", f"Generated BRD XML ({len(brd_xml)} characters)")

            # STAGE 2: Transform XML to HTML using LLM
            # NEW: Use comprehensive design system context
            design_system = design_context.get("design_system", get_design_system_prompt())
            html_prompt_template = design_context.get("html_prompt_template", "")
            design_requirements = design_context.get("design_requirements", "")

            html_system_message = f"""## ROLE AND GOAL
You are an expert Business Analyst and Information Designer. Your goal is to transform a raw BRD in XML format into a professional, client-ready, and interactive HTML document.

{design_system}

{design_requirements}

{html_prompt_template}

## CONTEXT
You will be given a single input: an XML string containing a `<businessRequirementsDocument>`.

## STEP-BY-STEP PROCESS
1. Parse the input XML to identify all sections (Executive Summary, Business Objectives, Stakeholder Analysis, etc.).
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

            # OPTIMIZATION: Break XML into smaller chunks for HTML generation
            # to prevent timeout during large document processing
            html_response = await self._call_llm(
                html_system_message,
                f"""Transform this BRD XML into a beautiful, professional HTML document:

{brd_xml}""",
                max_tokens=8000  # Reduced from 12000 to prevent timeout
            )

            # Clean HTML response
            brd_html = html_response.strip()
            if brd_html.startswith("```html"):
                brd_html = brd_html.split("```html")[1].split("```")[0].strip()
            elif brd_html.startswith("```"):
                brd_html = brd_html.split("```")[1].split("```")[0].strip()

            # Validate HTML starts correctly
            if not brd_html.startswith("<!DOCTYPE"):
                self.logger.warning("Generated HTML doesn't start with DOCTYPE, prepending it")
                brd_html = "<!DOCTYPE html>\n" + brd_html

            self.log_execution("success", f"Generated BRD HTML ({len(brd_html)} characters)")

            return AgentResult(
                success=True,
                data={
                    "brd_xml": brd_xml,
                    "brd_html": brd_html,
                    "project_name": project_name
                },
                metadata={
                    "agent": self.config.name,
                    "format": "xml+html"
                }
            )

        except Exception as e:
            self.logger.error(f"Error in BRDAgent: {str(e)}")
            return AgentResult(
                success=False,
                data=None,
                error=str(e),
                metadata={"agent": self.config.name}
            )

    # Remove old methods - using two-stage process like PRD agent now
    pass