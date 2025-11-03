"""
Mockup Agent - Generates Apple-style HTML mockups using LLM transformation
Advanced architecture: Makes SEPARATE API calls for each mockup for premium quality
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .design_system import get_design_system_prompt
import json
import asyncio


class MockupAgent(BaseAgent):
    """
    Agent responsible for generating Apple-style HTML mockups
    Makes separate LLM calls for each mockup to ensure premium quality

    Architecture:
    1. Generate index.html (dashboard) - 1 API call
    2. For each use case, generate mockup - 1 API call per use case
    3. Combine all results
    """

    def __init__(self, llm_client):
        config = AgentConfig(
            name="MockupAgent",
            description="Generates premium Apple-style HTML mockups with AICOE branding",
            model="x-ai/grok-code-fast-1",
            temperature=0.6,
            max_tokens=16000,  # Per mockup (not all at once)
        )
        super().__init__(config, llm_client)

    async def execute(
        self, input_data: Dict[str, Any], context: Dict[str, Any]
    ) -> AgentResult:
        """
        Generate Apple-style HTML mockups with SEPARATE API calls for premium quality

        Input:
            - use_cases: Use cases to visualize
            - project_name: Name of the project
            - structured_notes: Optional context

        Output:
            - mockup_pages: Dictionary of HTML pages
            - use_case_structure: Metadata about generated structure
        """
        try:
            # NEW: Merge workflow context for agent collaboration
            input_data = self._merge_workflow_context(input_data)

            self.log_execution(
                "start", "Generating premium HTML mockups with separate API calls"
            )
            self.validate_input(input_data, ["project_name"])

            project_name = input_data["project_name"]
            use_cases = input_data.get("use_cases", [])
            structured_notes = input_data.get("structured_notes", {})

            num_use_cases = len(use_cases) if isinstance(use_cases, list) else 0

            self.log_execution(
                "info",
                f"Will make {num_use_cases + 1} API calls: 1 for index + {num_use_cases} for use cases",
            )

            # Dictionary to store all generated HTML pages
            all_mockup_pages = {}

            # STEP 1: Generate index.html (dashboard)
            self.log_execution("progress", "Step 1: Generating index.html dashboard")
            index_html = await self._generate_index_page(
                project_name,
                use_cases,
                structured_notes,
                input_data,  # Pass full input with workflow context
            )
            all_mockup_pages["index.html"] = index_html
            self.log_execution("success", "✓ Generated index.html")

            # STEP 2: Generate each use case mockup separately
            self.log_execution(
                "progress", f"Step 2: Generating {num_use_cases} use case mockups"
            )

            for idx, use_case in enumerate(use_cases, 1):
                uc_id = use_case.get("id", f"UC-{idx:03d}")
                uc_name = use_case.get("name", f"Use Case {idx}")

                self.log_execution(
                    "progress",
                    f"  [{idx}/{num_use_cases}] Generating mockup for {uc_id}: {uc_name}",
                )

                # Generate mockup for this specific use case
                uc_mockup_pages = await self._generate_use_case_mockup(
                    project_name, use_case, structured_notes
                )

                # Add to all pages
                all_mockup_pages.update(uc_mockup_pages)

                self.log_execution(
                    "success",
                    f"  ✓ Generated {len(uc_mockup_pages)} page(s) for {uc_id}",
                )

            self.log_execution(
                "success", f"✓ Generated all {len(all_mockup_pages)} mockup pages"
            )

            # Analyze structure for metadata
            use_case_structure = self._analyze_structure(all_mockup_pages)

            return AgentResult(
                success=True,
                data={
                    "mockup_pages": all_mockup_pages,
                    "use_case_structure": use_case_structure,
                    "project_name": project_name,
                    "num_pages": len(all_mockup_pages),
                },
                metadata={
                    "agent": self.config.name,
                    "num_pages": len(all_mockup_pages),
                    "structure": use_case_structure,
                },
            )

        except Exception as e:
            self.logger.error(f"Error in MockupAgent: {str(e)}")
            return AgentResult(
                success=False,
                data=None,
                error=str(e),
                metadata={"agent": self.config.name},
            )

    async def _generate_index_page(
        self,
        project_name: str,
        use_cases: List[Dict[str, Any]],
        structured_notes: Dict[str, Any],
        input_data: Dict[str, Any] = None,
    ) -> str:
        """
        Generate the main index.html dashboard page

        This page showcases all use cases with beautiful cards
        """
        # NEW: Use workflow context design system if available
        design_system = (
            input_data.get("design_system", get_design_system_prompt())
            if input_data
            else get_design_system_prompt()
        )
        html_prompt_template = (
            input_data.get("html_prompt_template", "") if input_data else ""
        )

        # NEW: Get PRD HTML as style reference if available
        prd_html_reference = ""
        if input_data and "all_agent_outputs" in input_data:
            prd_data = input_data["all_agent_outputs"].get("prd", {})
            if prd_data:
                prd_html_reference = "\n\n## STYLE REFERENCE\nMatch the visual style and design patterns from the PRD HTML that was already generated for this project. Use the same colors, typography, spacing, and component styles for consistency."

        system_message = """You are a UI designer. Create a simple HTML mockup for this use case.

Return ONLY a JSON object like this:
{"UC_XXX_mockup.html": "<!DOCTYPE html><html><body><h1>Use Case Name</h1><p>Use case description</p></body></html>"}

No explanations, no markdown, just the JSON."""

        use_cases_summary = []
        for uc in use_cases:
            use_cases_summary.append(
                {
                    "id": uc.get("id", "UC-XXX"),
                    "name": uc.get("name", "Unnamed Use Case"),
                    "description": uc.get("description", "No description provided"),
                }
            )

        user_message = f"""Create the index.html dashboard for:

Project Name: {project_name}

Use Cases ({len(use_cases)} total):
{json.dumps(use_cases_summary, indent=2)}

Make it absolutely stunning - this is the first page users see!"""

        response = await self._call_llm(system_message, user_message, max_tokens=8000)

        # Clean response
        html_content = self._clean_html_response(response)

        return html_content

    async def _generate_use_case_mockup(
        self,
        project_name: str,
        use_case: Dict[str, Any],
        structured_notes: Dict[str, Any],
    ) -> Dict[str, str]:
        """
        Generate mockup(s) for a single use case

        Returns a dictionary of filename -> HTML content
        Can return single page or multiple pages depending on complexity
        """
        design_system = get_design_system_prompt()

        uc_id = use_case.get("id", "UC-XXX")
        uc_name = use_case.get("name", "Unnamed Use Case")
        uc_description = use_case.get("description", "")
        uc_steps = use_case.get("steps", [])
        num_steps = len(uc_steps) if isinstance(uc_steps, list) else 0

        system_message = f"""You are an expert UI/UX designer specializing in Apple-inspired interfaces.

{design_system}

**CRITICAL REQUIREMENTS:**
1. Use the COMPLETE AICOE design system CSS variables (copy the entire :root block)
2. Create a stunning, interactive mockup with smooth animations
3. Follow Apple Human Interface Guidelines
4. Include realistic UI components (buttons, forms, cards, etc.)
5. Make it visually impressive and functional
6. Use gradient backgrounds, glassmorphism effects, and modern CSS
7. Ensure mobile responsiveness

**OUTPUT FORMAT:**
Return ONLY a JSON object with ONE key-value pair:
{{"{uc_id}_mockup.html": "<!DOCTYPE html><html lang='en'>...</html>"}}

The HTML must be:
- Complete and valid HTML5
- Include the full AICOE design system in <style> tags
- Feature smooth animations and transitions
- Be visually stunning with proper spacing and typography
- Use semantic HTML elements

No explanations, no markdown formatting, just pure JSON."""

        user_message = f"""Create a premium Apple-inspired HTML mockup for:

**Project:** {project_name}

**Use Case ID:** {uc_id}
**Use Case Name:** {uc_name}
**Description:** {uc_description}

**Steps:** {json.dumps(uc_steps, indent=2) if uc_steps else "See description"}

Make this mockup absolutely stunning - worthy of an Apple product launch!
Include interactive elements, smooth animations, and the complete AICOE design system."""

        response = await self._call_llm(system_message, user_message, max_tokens=8000)

        # Use the robust JSON parsing from base agent
        self.logger.info(
            f"Mockup agent received response for {uc_id}, length: {len(response)}"
        )
        if len(response.strip()) == 0:
            self.logger.error(f"Empty response from LLM for {uc_id}")
            mockup_pages = {
                f"{uc_id}_mockup.html": f"<!DOCTYPE html><html><body><h1>Mockup for {uc_name}</h1><p>LLM returned empty response. Using fallback.</p></body></html>"
            }
        else:
            mockup_pages = self.parse_json_response(response, f"{uc_id}_mockup")

            # If parsing failed and we got a fallback, create a simple error page
            if "parse_error" in mockup_pages:
                self.logger.error(
                    f"Failed to parse use case mockup JSON for {uc_id}: {mockup_pages['parse_error']}"
                )
                mockup_pages = {
                    f"{uc_id}_mockup.html": f"<!DOCTYPE html><html><body><h1>Error generating mockup for {uc_name}</h1><p>Could not parse LLM response.</p></body></html>"
                }

        # Unescape HTML content
        unescaped_pages = {}
        for page_name, html_content in mockup_pages.items():
            if isinstance(html_content, str):
                unescaped_html = (
                    html_content.replace("\\n", "\n")
                    .replace("\\t", "\t")
                    .replace('\\"', '"')
                )
                unescaped_pages[page_name] = unescaped_html
            else:
                unescaped_pages[page_name] = html_content

        return unescaped_pages

    def _clean_html_response(self, response: str) -> str:
        """Clean HTML response from LLM"""
        response_clean = response.strip()

        # Remove markdown code fences if present
        if response_clean.startswith("```html"):
            response_clean = response_clean.split("```html")[1].split("```")[0].strip()
        elif response_clean.startswith("```"):
            response_clean = response_clean.split("```")[1].split("```")[0].strip()

        # Unescape if needed
        response_clean = (
            response_clean.replace("\\n", "\n").replace("\\t", "\t").replace('\\"', '"')
        )

        return response_clean

    def _analyze_structure(self, mockup_pages: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze the generated mockup structure

        Returns metadata about single-page vs multi-screen use cases
        """
        structure = {
            "total_pages": len(mockup_pages),
            "has_index": "index.html" in mockup_pages,
            "use_cases": {},
        }

        # Analyze each page
        for filename in mockup_pages.keys():
            if filename == "index.html":
                continue

            # Extract use case ID
            if "_" in filename:
                uc_id = filename.split("_")[0]  # e.g., "UC-001"

                if uc_id not in structure["use_cases"]:
                    structure["use_cases"][uc_id] = {"type": "unknown", "pages": []}

                structure["use_cases"][uc_id]["pages"].append(filename)

                # Determine type
                if "screen-" in filename:
                    structure["use_cases"][uc_id]["type"] = "multi-screen"
                elif filename.endswith("_mockup.html"):
                    structure["use_cases"][uc_id]["type"] = "single-page"
                elif filename.endswith("_index.html"):
                    structure["use_cases"][uc_id]["type"] = "multi-screen"

        return structure
