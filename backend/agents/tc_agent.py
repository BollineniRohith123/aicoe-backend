"""
TC Agent - Test Cases Document Generator
Follows Rule 07: Test Cases Document Guidelines
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentConfig, AgentResult
import logging

logger = logging.getLogger(__name__)


class TCAgent(BaseAgent):
    """
    TC Agent creates comprehensive Test Cases Documents
    following AICoE rule 07 guidelines for test cases documentation.
    """

    def __init__(self, llm_client):
        config = AgentConfig(
            name="TC Agent",
            description="Test Cases Document Generator",
            model="x-ai/grok-code-fast-1",
            temperature=0.7,
            max_tokens=4000,
            timeout=120
        )
        super().__init__(config, llm_client)
        self.logger = logging.getLogger("tc_agent")
        
        # Rule 07: Test Cases Document Guidelines
        self.rule_guidelines = {
            "document_structure": [
                "Test Strategy Overview",
                "Test Environment Setup",
                "Unit Test Cases",
                "Integration Test Cases",
                "System Test Cases",
                "User Acceptance Test Cases",
                "Performance Test Cases",
                "Security Test Cases",
                "Test Execution Results"
            ],
            "content_requirements": {
                "test_strategy": "Comprehensive testing strategy and approach",
                "test_cases": "Detailed test cases with steps and expected results",
                "test_data": "Test data requirements and datasets",
                "test_environment": "Test environment specifications",
                "acceptance_criteria": "Clear acceptance criteria for each test",
                "test_automation": "Automation opportunities and scripts",
                "defect_tracking": "Defect tracking and resolution process",
                "test_metrics": "Test coverage and quality metrics"
            },
            "formatting": {
                "structure": "Professional testing document format",
                "test_cases": "Standard test case format with ID, steps, expected results",
                "tables": "Use tables for test case matrices and coverage",
                "diagrams": "Include test flow diagrams where applicable",
                "aicoe_branding": "Apply AICoE design system branding"
            }
        }

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Execute TC generation based on input data and context
        
        Args:
            input_data: Contains use_cases, business_requirements, functional_requirements, prd_content, research_insights, rule_context
            context: Project context and metadata
            
        Returns:
            AgentResult with TC content and metadata
        """
        try:
            project_name = input_data.get("project_name", "Unknown Project")
            use_cases = input_data.get("use_cases", [])
            business_requirements = input_data.get("business_requirements", {})
            functional_requirements = input_data.get("functional_requirements", {})
            prd_content = input_data.get("prd_content", "")
            research_insights = input_data.get("research_insights", {})
            rule_context = input_data.get("rule_context", "")
            
            self.logger.info(f"Starting TC generation for project: {project_name}")
            self.logger.info(f"Processing {len(use_cases)} use cases and requirements")
            self.logger.info(f"Using rule context: {len(rule_context)} characters")

            # Generate comprehensive TC content with rule context
            tc_content = await self._generate_tc_content(
                project_name=project_name,
                use_cases=use_cases,
                business_requirements=business_requirements,
                functional_requirements=functional_requirements,
                prd_content=prd_content,
                research_insights=research_insights,
                rule_context=rule_context
            )

            # Generate XML representation
            tc_xml = self._convert_to_xml(tc_content, "test_cases_document")

            # Generate HTML with AICoE branding
            tc_html = await self._generate_tc_html(tc_content, project_name)

            # Prepare result data
            result_data = {
                "project_name": project_name,
                "document_type": "Test Cases Document",
                "test_cases": tc_content,
                "tc_xml": tc_xml,
                "tc_html": tc_html,
                "use_cases_processed": len(use_cases),
                "business_requirements_included": bool(business_requirements),
                "functional_requirements_included": bool(functional_requirements),
                "research_categories": list(research_insights.keys()) if research_insights else [],
                "generated_at": self._get_timestamp(),
                "rule_compliance": "Rule 07 - Test Cases Document Guidelines"
            }

            self.logger.info(f"TC generation completed successfully for {project_name}")
            return AgentResult(success=True, data=result_data)

        except Exception as e:
            self.logger.error(f"TC generation failed: {str(e)}")
            return AgentResult(success=False, data={}, error=str(e))

    async def _generate_tc_content(
        self,
        project_name: str,
        use_cases: List[Dict[str, Any]],
        business_requirements: Dict[str, Any],
        functional_requirements: Dict[str, Any],
        prd_content: str,
        research_insights: Dict[str, Any],
        rule_context: str = ""
    ) -> Dict[str, Any]:
        """Generate comprehensive TC content following Rule 07 guidelines"""
        
        # Create enhanced prompt with rule context
        prompt = f"""
        {rule_context}
        
        Create comprehensive Test Cases (TC) for the project: {project_name}
        
        Follow the AICoE Rule 07 guidelines provided above for test case documentation.
        
        PROJECT CONTEXT:
        - Project Name: {project_name}
        - Use Cases: {use_cases}
        - Business Requirements: {business_requirements}
        - Functional Requirements: {functional_requirements}
        - PRD Content: {prd_content}
        - Research Insights: {research_insights}
        
        TC STRUCTURE REQUIREMENTS:
        {self.rule_guidelines['document_structure']}
        
        CONTENT REQUIREMENTS:
        {self.rule_guidelines['content_requirements']}
        
        Generate detailed test cases that include:
        1. Test case identification and description
        2. Preconditions and test data
        3. Step-by-step test procedures
        4. Expected results and acceptance criteria
        5. Test types (functional, integration, system, acceptance)
        6. Priority and traceability mapping
        7. Test environment requirements
        8. Pass/fail criteria
        
        IMPORTANT: Follow the AICoE standards and guidelines provided in the rule context above.
        Use qualitative language over quantitative metrics.
        Focus on business value over technical details.
        Apply light theme design principles.
        
        Format each TC with: ID, Title, Description, Test Type, Priority, Preconditions, Test Data, Test Steps, Expected Results, Actual Results, Status.
        """

        try:
            response = await self._call_llm(
                system_message="You are a test analyst creating comprehensive Test Cases Documents following AICoE standards.",
                user_message=prompt,
                temperature=0.7,
                max_tokens=4000
            )
            tc_content = self._parse_tc_response(response)
            
            # Enhance with additional test context
            enhanced_content = self._enhance_tc_content(tc_content, use_cases, functional_requirements)
            
            return enhanced_content
            
        except Exception as e:
            self.logger.error(f"Error generating TC content: {str(e)}")
            return self._generate_fallback_tc(project_name, use_cases, functional_requirements)

    def _parse_tc_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response into structured TC format"""
        try:
            # Try to extract structured content from response
            sections = {
                "test_strategy": "",
                "test_environment": {},
                "unit_test_cases": [],
                "integration_test_cases": [],
                "system_test_cases": [],
                "uat_test_cases": [],
                "performance_test_cases": [],
                "security_test_cases": [],
                "test_execution_results": []
            }
            
            # Basic parsing logic - enhance as needed
            lines = response_text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Detect section headers
                for section in sections.keys():
                    if section.replace('_', ' ').title() in line:
                        current_section = section
                        break
                
                # Add content to current section
                if current_section and line:
                    if isinstance(sections[current_section], list):
                        sections[current_section].append(line)
                    elif isinstance(sections[current_section], dict):
                        # Parse key-value pairs for environment setup
                        if ":" in line:
                            key, value = line.split(":", 1)
                            sections[current_section][key.strip()] = value.strip()
                    else:
                        sections[current_section] += line + " "
            
            return sections
            
        except Exception as e:
            self.logger.error(f"Error parsing TC response: {str(e)}")
            return {}

    def _enhance_tc_content(
        self, 
        tc_content: Dict[str, Any], 
        use_cases: List[Dict[str, Any]], 
        functional_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enhance TC content with additional context from use cases and functional requirements"""
        
        enhanced = tc_content.copy()
        
        # Generate test cases from use cases
        if "system_test_cases" in enhanced and use_cases:
            test_cases = []
            for i, uc in enumerate(use_cases, 1):
                test_case = {
                    "test_id": f"TC-{i:03d}",
                    "test_name": f"Test {uc.get('id', f'UC-{i:03d}')}",
                    "objective": f"Verify {uc.get('description', 'use case functionality')}",
                    "preconditions": "User is authenticated and system is available",
                    "test_steps": [
                        "1. Navigate to the application",
                        "2. Perform the required actions",
                        "3. Verify the expected outcome"
                    ],
                    "expected_result": uc.get("expected_outcome", "System functions as specified"),
                    "priority": uc.get("priority", "Medium"),
                    "test_data": "Standard test dataset"
                }
                test_cases.append(test_case)
            enhanced["system_test_cases"] = test_cases
        
        # Add functional requirements as test specifications
        if "unit_test_cases" in enhanced and "functional_specifications" in functional_requirements:
            unit_tests = []
            for i, spec in enumerate(functional_requirements["functional_specifications"][:5], 1):
                unit_test = {
                    "test_id": f"UT-{i:03d}",
                    "test_name": f"Unit Test {i}",
                    "objective": f"Test {spec}",
                    "preconditions": "Component is properly initialized",
                    "test_steps": [
                        "1. Call the function/method",
                        "2. Verify return value",
                        "3. Check side effects"
                    ],
                    "expected_result": "Function executes successfully with correct output",
                    "priority": "High"
                }
                unit_tests.append(unit_test)
            enhanced["unit_test_cases"] = unit_tests
        
        return enhanced

    def _generate_fallback_tc(self, project_name: str, use_cases: List[Dict[str, Any]], functional_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback TC content if LLM generation fails"""
        
        # Generate test cases from use cases
        test_cases = []
        for i, uc in enumerate(use_cases[:10], 1):  # Limit to 10 test cases
            test_cases.append({
                "test_id": f"TC-{i:03d}",
                "test_name": f"Test {uc.get('id', f'UC-{i:03d}')}",
                "objective": f"Verify {uc.get('description', 'use case functionality')}",
                "preconditions": "User is authenticated and system is available",
                "test_steps": [
                    "1. Navigate to the application",
                    "2. Perform the required actions",
                    "3. Verify the expected outcome"
                ],
                "expected_result": uc.get("expected_outcome", "System functions as specified"),
                "priority": uc.get("priority", "Medium"),
                "test_data": "Standard test dataset"
            })
        
        return {
            "test_strategy": f"Comprehensive testing strategy for {project_name}",
            "test_environment": {
                "hardware": "Standard development environment",
                "software": "Latest stable version of application",
                "network": "Local network with internet access",
                "data": "Test database with sample data"
            },
            "unit_test_cases": [
                {
                    "test_id": "UT-001",
                    "test_name": "Authentication Test",
                    "objective": "Verify user authentication functionality",
                    "preconditions": "User account exists in system",
                    "test_steps": ["1. Enter valid credentials", "2. Click login", "3. Verify redirect"],
                    "expected_result": "User successfully authenticated and redirected",
                    "priority": "High"
                }
            ],
            "integration_test_cases": [
                {
                    "test_id": "IT-001",
                    "test_name": "Database Integration Test",
                    "objective": "Verify database connectivity and operations",
                    "preconditions": "Database service is running",
                    "test_steps": ["1. Connect to database", "2. Perform CRUD operations", "3. Verify data integrity"],
                    "expected_result": "All database operations complete successfully",
                    "priority": "High"
                }
            ],
            "system_test_cases": test_cases,
            "uat_test_cases": [
                {
                    "test_id": "UAT-001",
                    "test_name": "Business Process Test",
                    "objective": "Verify end-to-end business process",
                    "preconditions": "All system components are operational",
                    "test_steps": ["1. Start business process", "2. Complete all steps", "3. Verify final outcome"],
                    "expected_result": "Business process completes successfully",
                    "priority": "High"
                }
            ],
            "performance_test_cases": [
                {
                    "test_id": "PT-001",
                    "test_name": "Load Test",
                    "objective": "Verify system performance under load",
                    "preconditions": "Load testing tools are configured",
                    "test_steps": ["1. Simulate 100 concurrent users", "2. Monitor system response", "3. Measure performance metrics"],
                    "expected_result": "System maintains acceptable performance under load",
                    "priority": "Medium"
                }
            ],
            "security_test_cases": [
                {
                    "test_id": "ST-001",
                    "test_name": "Access Control Test",
                    "objective": "Verify proper access controls",
                    "preconditions": "User roles are configured",
                    "test_steps": ["1. Attempt unauthorized access", "2. Verify access is denied", "3. Test authorized access"],
                    "expected_result": "Access controls function correctly",
                    "priority": "High"
                }
            ],
            "test_execution_results": [
                "Test execution tracking framework",
                "Defect logging and tracking process",
                "Test coverage reporting",
                "Quality metrics dashboard"
            ]
        }

    async def _generate_tc_html(self, tc_content: Dict[str, Any], project_name: str) -> str:
        """Generate HTML version of TC with AICoE branding"""
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Test Cases Document - {project_name}</title>
            <link rel="stylesheet" href="../../Design System/06-reference-aicoe-design-system.css">
        </head>
        <body class="aicoe-document">
            <div class="document-header">
                <img src="../../Design System/08-asset-aicoe-logo.png" alt="AICoE Logo" class="logo">
                <h1>Test Cases Document</h1>
                <h2>{project_name}</h2>
                <p class="document-meta">Generated on {self._get_timestamp()}</p>
            </div>
            
            <div class="document-content">
                {self._convert_tc_to_html_sections(tc_content)}
            </div>
            
            <div class="document-footer">
                <p>&copy; 2024 AICoE - Test Cases Document</p>
            </div>
        </body>
        </html>
        """
        
        return html_template

    def _convert_tc_to_html_sections(self, tc_content: Dict[str, Any]) -> str:
        """Convert TC content to HTML sections"""
        html_sections = ""
        
        section_mapping = {
            "test_strategy": "Test Strategy Overview",
            "test_environment": "Test Environment Setup",
            "unit_test_cases": "Unit Test Cases",
            "integration_test_cases": "Integration Test Cases",
            "system_test_cases": "System Test Cases",
            "uat_test_cases": "User Acceptance Test Cases",
            "performance_test_cases": "Performance Test Cases",
            "security_test_cases": "Security Test Cases",
            "test_execution_results": "Test Execution Results"
        }
        
        for key, title in section_mapping.items():
            if key in tc_content and tc_content[key]:
                html_sections += f"""
                <section class="document-section">
                    <h3>{title}</h3>
                    <div class="section-content">
                        {self._format_section_content(tc_content[key])}
                    </div>
                </section>
                """
        
        return html_sections

    def _format_section_content(self, content) -> str:
        """Format section content for HTML display"""
        if isinstance(content, list):
            if content and isinstance(content[0], dict) and "test_id" in content[0]:
                # Test cases format
                test_cases_html = ""
                for test_case in content:
                    test_cases_html += f"""
                    <div class="test-case">
                        <h4>{test_case.get('test_id', '')}: {test_case.get('test_name', '')}</h4>
                        <p><strong>Objective:</strong> {test_case.get('objective', '')}</p>
                        <p><strong>Preconditions:</strong> {test_case.get('preconditions', '')}</p>
                        <h5>Test Steps:</h5>
                        <ol>
                            {''.join(f'<li>{step}</li>' for step in test_case.get('test_steps', []))}
                        </ol>
                        <p><strong>Expected Result:</strong> {test_case.get('expected_result', '')}</p>
                        <p><strong>Priority:</strong> {test_case.get('priority', 'Medium')}</p>
                    </div>
                    """
                return test_cases_html
            else:
                return "<ul>" + "".join(f"<li>{item}</li>" for item in content) + "</ul>"
        elif isinstance(content, dict):
            return "<table>" + "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in content.items()) + "</table>"
        else:
            return f"<p>{content}</p>"

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    def _convert_to_xml(self, data: Any, root_name: str = "data") -> str:
        """Convert data to XML format"""
        import xml.etree.ElementTree as ET
        
        def dict_to_xml(data_dict, parent):
            for key, value in data_dict.items():
                safe_key = "".join(c if c.isalnum() or c in "_-" else "_" for c in str(key))
                if isinstance(value, dict):
                    child = ET.SubElement(parent, safe_key)
                    dict_to_xml(value, child)
                elif isinstance(value, list):
                    list_element = ET.SubElement(parent, safe_key)
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            item_element = ET.SubElement(list_element, f"item_{i}")
                            dict_to_xml(item, item_element)
                        else:
                            item_element = ET.SubElement(list_element, f"item_{i}")
                            item_element.text = str(item)
                else:
                    element = ET.SubElement(parent, safe_key)
                    element.text = str(value) if value is not None else ""
        
        root = ET.Element(root_name)
        if isinstance(data, dict):
            dict_to_xml(data, root)
        else:
            root.text = str(data)
            
        return ET.tostring(root, encoding="unicode")