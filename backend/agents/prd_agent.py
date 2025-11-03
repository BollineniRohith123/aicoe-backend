"""
PRD Agent - Assembles comprehensive Product Requirements Document
Generates HTML directly from XML using LLM transformation
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .design_system import get_design_system_prompt
import json


class PRDAgent(BaseAgent):
    """
    Agent responsible for creating comprehensive PRD documents
    Takes XML input and generates beautiful HTML output using LLM
    """

    def __init__(self, llm_client):
        config = AgentConfig(
            name="PRDAgent",
            description="Creates comprehensive Product Requirements Documents",
            model="x-ai/grok-code-fast-1",  # GLM-4.6 via OpenRouter
            temperature=0.4,
            max_tokens=12000  # Increased to handle complex HTML generation
        )
        super().__init__(config, llm_client)

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Generate comprehensive PRD document as HTML

        This is a TWO-STAGE process:
        Stage 1: Generate structured XML (for data storage and IP)
        Stage 2: Transform XML to beautiful HTML using LLM

        Input:
            - structured_notes: From TranscriptAgent
            - use_cases: From RequirementsAgent
            - business_requirements: From RequirementsAgent
            - project_name: Name of the project

        Output:
            - prd_xml: Structured XML document
            - prd_html: Beautiful HTML document
        """
        try:
            # NEW: Merge workflow context for agent collaboration
            input_data = self._merge_workflow_context(input_data)

            self.log_execution("start", "Generating PRD document")
            self.validate_input(input_data, ["project_name"])

            project_name = input_data["project_name"]
            structured_notes = input_data.get("structured_notes", {})
            use_cases = input_data.get("use_cases", [])
            business_reqs = input_data.get("business_requirements", {})
            research_insights = input_data.get("research_insights", {})

            # Prepare context for PRD generation
            research_text = json.dumps(research_insights, indent=2) if research_insights else "No research insights available"

            context_text = f"""
Project Name: {project_name}

Structured Meeting Notes:
{json.dumps(structured_notes, indent=2)}

Use Cases:
{json.dumps(use_cases, indent=2)}

Business Requirements:
{json.dumps(business_reqs, indent=2)}

Research Insights (CRITICAL - Use this extensively):
{research_text}

**ADDITIONAL CONTEXT FOR ENHANCED PRD:**
- Include success metrics (KPIs, measurement criteria)
- Add risk assessment (potential risks and mitigation strategies)
- Define dependencies (external dependencies and prerequisites)
- Document assumptions made during planning
- Specify constraints (technical, business, resource)
- Address accessibility requirements (WCAG 2.1 AA compliance)
- Consider internationalization (multi-language support plans)
- Set performance targets (load time, response time goals)
- Detail security requirements (authentication, authorization, encryption)
- Include compliance requirements (GDPR, CCPA, SOC 2)
"""

            # STAGE 1: Generate XML for data storage
            xml_system_message = """## ROLE AND GOAL
You are an expert Technical Writer creating comprehensive Product Requirements Documents (PRDs). Your goal is to create an enterprise-grade PRD that combines vision, requirements, use cases, and industry research into a professional document.

## CONTEXT
You will receive structured data from previous agents including meeting notes, use cases, business requirements, and research insights. Use this data to create a comprehensive, professional PRD.

## STEP-BY-STEP PROCESS
1. Extract the project vision, business requirements, and stakeholders from the structured meeting notes.
2. Incorporate all use cases with their detailed flows, actors, and alternative scenarios.
3. Synthesize research insights to include market context, competitor analysis, and industry trends.
4. Define comprehensive business goals with measurable KPIs and success metrics.
5. Create detailed success metrics section with specific KPIs, measurement criteria, and tracking methods.
6. Conduct risk assessment with potential risks, likelihood, impact, and mitigation strategies.
7. Document all dependencies (external services, third-party APIs, team prerequisites).
8. State all assumptions made during planning and validation process.
9. Specify constraints including technical limitations, budget restrictions, and resource availability.
10. Define accessibility requirements (WCAG 2.1 AA compliance, keyboard navigation, screen reader support).
11. Outline internationalization strategy (primary language, future language plans, localization requirements).
12. Set explicit performance targets (page load times, API response times, throughput capacity).
13. Detail security requirements (authentication methods, data encryption, access control).
14. Include compliance requirements (GDPR, CCPA, SOC 2, industry-specific regulations).
15. Assemble all sections into the strict XML format defined below.

## CRITICAL QUALITY REQUIREMENTS
- Include comprehensive success metrics with specific KPIs and measurement methods
- Provide detailed risk assessment with mitigation strategies
- Document all external dependencies and prerequisites clearly
- State all assumptions and constraints explicitly
- Address WCAG 2.1 AA accessibility requirements
- Include internationalization and localization strategy
- Specify performance targets (load time < 2s, 99.9% uptime, 95% of API calls < 500ms)
- Detail security requirements (OAuth 2.0, end-to-end encryption, role-based access control)
- Document compliance requirements (GDPR, CCPA, SOC 2 Type II, HIPAA if applicable)

## OUTPUT FORMAT (CRITICAL)
Your entire response MUST be ONLY valid XML in this exact format. No explanations, no markdown, just the XML.

<productRequirementsDocument>
    <title>PRD for [Project Name]</title>
    <executiveSummary>A comprehensive paragraph summarizing the project's purpose, scope, business goals, and competitive positioning, incorporating research insights and market trends. Include key success metrics and strategic importance.</executiveSummary>

    <scope>
        <inScope>A detailed bulleted list of features and capabilities included in the MVP, prioritized by business value. Include core functionality, integrations, and compliance features.</inScope>
        <outOfScope>A detailed bulleted list of features explicitly excluded from the MVP. Include planned future features, dependencies, and out-of-scope technologies or integrations.</outOfScope>
        <dependencies>
            <externalServices>List of external APIs, services, or third-party dependencies (e.g., payment processors, cloud storage, authentication providers)</externalServices>
            <prerequisites>Team and organizational prerequisites (e.g., design system approval, security review, legal compliance)</prerequisites>
        </dependencies>
        <assumptions>Key assumptions made during planning, including market conditions, user behavior, technical feasibility, and resource availability.</assumptions>
        <constraints>
            <technicalConstraints>Technical limitations including platform compatibility, browser support, API restrictions</technicalConstraints>
            <businessConstraints>Budget constraints, timeline constraints, market constraints</businessConstraints>
            <resourceConstraints>Team capacity, skill requirements, tool limitations</resourceConstraints>
        </constraints>
    </scope>

    <businessGoals>
        <primaryObjectives>Primary business objectives with specific, measurable goals and timelines.</primaryObjectives>
        <keyPerformanceIndicators>
            <kpi name="user_adoption" target="10,000 users" timeframe="12 months" measurement="monthly active users">
                <description>How to measure and track user adoption metrics</description>
            </kpi>
            <kpi name="revenue_target" target="$2.5M ARR" timeframe="24 months" measurement="monthly recurring revenue">
                <description>Specific revenue targets and growth milestones</description>
            </kpi>
            <kpi name="user_retention" target="85% retention" timeframe="12 months" measurement="monthly churn rate">
                <description>User retention targets and engagement metrics</description>
            </kpi>
            <kpi name="feature_adoption" target="70% AI feature usage" timeframe="12 months" measurement="feature usage analytics">
                <description>Expected adoption rates for key features</description>
            </kpi>
            <kpi name="performance_sla" target="99.9% uptime" timeframe="continuous" measurement="system monitoring">
                <description>Technical performance KPIs and SLAs</description>
            </kpi>
        </keyPerformanceIndicators>
        <successMetrics>
            <metric name="customer_satisfaction" target="4.5+ stars" measurement="CSAT surveys">
                <trackingMethod>Net Promoter Score (NPS > 40), Customer Satisfaction Score (CSAT > 4.5/5)</trackingMethod>
            </metric>
            <metric name="market_share" target="2% market share" timeframe="24 months" measurement="industry benchmarks">
                <description>Competitive positioning and market penetration goals</description>
            </metric>
        </successMetrics>
    </businessGoals>

    <nonFunctionalRequirements>
        <performance>
            <pageLoadTime target="&lt; 2 seconds" measurement="95th percentile">
                <description>Target page load times for critical user journeys</description>
            </pageLoadTime>
            <apiResponse target="&lt; 500ms" measurement="99th percentile">
                <description>API response time requirements for core endpoints</description>
            </apiResponse>
            <uptime target="99.9%" measurement="monthly availability">
                <description>System uptime and reliability targets</description>
            </uptime>
            <concurrency target="1000 concurrent users" measurement="load testing">
                <description>Expected user concurrency and scalability requirements</description>
            </concurrency>
        </performance>
        <security>
            <authentication target="OAuth 2.0" measurement="SSO support">
                <description>Authentication methods and single sign-on capabilities</description>
            </authentication>
            <authorization target="Role-Based Access Control" measurement="RBAC implementation">
                <description>User roles, permissions, and access control requirements</description>
            </authorization>
            <dataEncryption target="End-to-End" measurement="AES-256">
                <description>Data encryption at rest and in transit requirements</description>
            </dataEncryption>
            <compliance target="GDPR, CCPA, SOC 2" measurement="third-party audit">
                <description>Regulatory compliance requirements and audit schedule</description>
            </compliance>
        </security>
        <accessibility target="WCAG 2.1 AA" measurement="automated testing + manual review">
            <description>Accessibility standards, keyboard navigation, screen reader support</description>
        </accessibility>
        <internationalization target="English (initial) + 3 more languages" measurement="localization testing">
            <description>Primary language support and future internationalization roadmap</description>
        </internationalization>
    </nonFunctionalRequirements>

    <useCases>
        <useCase id="UC-001" name="Use Case 1 Name" priority="High">
            <description>Comprehensive description of the use case including goals and outcomes.</description>
            <primaryActor>Primary user role performing this action</primaryActor>
            <secondaryActors>List of supporting actors/roles</secondaryActors>
            <preconditions>Conditions that must be true before use case can execute</preconditions>
            <mainFlow>
                <step number="1">First step in the main success scenario</step>
                <step number="2">Second step in the main success scenario</step>
                <!-- Continue with all steps -->
            </mainFlow>
            <alternativeFlows>
                <flow id="A1">
                    <description>Alternative flow description</description>
                    <steps>
                        <step number="1">Alternative step 1</step>
                    </steps>
                </flow>
            </alternativeFlows>
            <postconditions>State of system after successful completion</postconditions>
            <errorPaths>
                <path id="E1">
                    <description>Error scenario 1</description>
                    <resolution>User action to resolve error</resolution>
                </path>
            </errorPaths>
            <nonFunctionalRequirements>Security, performance, usability requirements specific to this use case</nonFunctionalRequirements>
        </useCase>
        <!-- Additional use cases follow the same detailed structure -->
    </useCases>

    <riskAssessment>
        <risk level="High" likelihood="Medium" impact="High">
            <description>Detailed description of the risk</description>
            <mitigationStrategy>Step-by-step mitigation plan</mitigationStrategy>
            <owner>Team member responsible for monitoring this risk</owner>
            <status>Current status of risk (Open, In Progress, Mitigated)</status>
        </risk>
        <!-- Additional risks -->
    </riskAssessment>

    <implementationNotes>
        <technicalStack>Primary technologies and frameworks (e.g., React, Node.js, PostgreSQL)</technicalStack>
        <developmentApproach>Methodology and processes (Agile, Waterfall, etc.)</developmentApproach>
        <testingStrategy>Quality assurance and testing plan</testingStrategy>
        <deploymentStrategy>Deployment architecture and hosting requirements</deploymentStrategy>
    </implementationNotes>
    <useCases>
        <useCaseModel>
            <useCase>
                <title>Use Case Title</title>
                <primaryActor>Primary Actor</primaryActor>
                <secondaryActors>
                    <actor>Secondary Actor 1</actor>
                </secondaryActors>
                <description>Use case description</description>
                <mainFlow>
                    <step>Step 1</step>
                    <step>Step 2</step>
                </mainFlow>
                <alternativeFlows>
                    <flow id="A1" trigger="Alternative condition">
                        <step>Alternative step 1</step>
                    </flow>
                </alternativeFlows>
                <exceptionFlows>
                    <flow id="E1" trigger="Exception condition">
                        <step>Exception step 1</step>
                    </flow>
                </exceptionFlows>
            </useCase>
        </useCaseModel>
    </useCases>
    <nonFunctionalRequirements>
        <requirement type="Security">All sensitive data must be encrypted at rest and in transit using industry-standard protocols.</requirement>
        <requirement type="Performance">The system must respond to 95% of user queries in under 2 seconds.</requirement>
    </nonFunctionalRequirements>
</productRequirementsDocument>
"""

            self.log_execution("llm_call", "Generating PRD XML")

            xml_response = await self._call_llm(
                xml_system_message,
                f"""Generate a PRD XML document for project: {project_name}

Input Data:
{context_text}""",
                max_tokens=8000
            )

            # Clean XML response
            prd_xml = xml_response.strip()
            if prd_xml.startswith("```xml"):
                prd_xml = prd_xml.split("```xml")[1].split("```")[0].strip()
            elif prd_xml.startswith("```"):
                prd_xml = prd_xml.split("```")[1].split("```")[0].strip()

            self.log_execution("success", f"Generated PRD XML ({len(prd_xml)} characters)")

            # STAGE 2: Transform XML to HTML using LLM
            design_system = input_data.get("design_system", get_design_system_prompt())
            html_prompt_template = input_data.get("html_prompt_template", "")

            html_system_message = f"""## ROLE AND GOAL
You are an expert Technical Writer and Information Designer. Your goal is to transform a raw PRD in XML format into a professional, client-ready, and interactive HTML document.

{design_system}

{html_prompt_template}

## CONTEXT
You will be given a single input: an XML string containing a `<productRequirementsDocument>`.

## STEP-BY-STEP PROCESS
1. Parse the input XML to identify all sections (Executive Summary, Scope, Use Cases, etc.).
2. Generate a clean HTML structure that represents this document.
3. Create an interactive, smooth-scrolling Table of Contents at the top of the document that links to each major section.
4. Style the entire document with absolute precision according to the AICOE design system above.
5. Return the final, single HTML file as a string.

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
- **Print-friendly:** Include print styles for professional PDF generation."""

            self.log_execution("llm_call", "Transforming XML to HTML")

            html_response = await self._call_llm(
                html_system_message,
                f"""Transform this PRD XML into a beautiful, professional HTML document:

{prd_xml}""",
                max_tokens=12000
            )

            # Clean HTML response
            prd_html = html_response.strip()
            if prd_html.startswith("```html"):
                prd_html = prd_html.split("```html")[1].split("```")[0].strip()
            elif prd_html.startswith("```"):
                prd_html = prd_html.split("```")[1].split("```")[0].strip()

            # Validate HTML starts correctly
            if not prd_html.startswith("<!DOCTYPE"):
                self.logger.warning("Generated HTML doesn't start with DOCTYPE, prepending it")
                prd_html = "<!DOCTYPE html>\n" + prd_html

            self.log_execution("success", f"Generated PRD HTML ({len(prd_html)} characters)")

            return AgentResult(
                success=True,
                data={
                    "prd_xml": prd_xml,
                    "prd_html": prd_html,
                    "project_name": project_name
                },
                metadata={
                    "agent": self.config.name,
                    "format": "xml+html"
                }
            )

        except Exception as e:
            self.logger.error(f"Error in PRDAgent: {str(e)}")
            return AgentResult(
                success=False,
                data=None,
                error=str(e),
                metadata={"agent": self.config.name}
            )
