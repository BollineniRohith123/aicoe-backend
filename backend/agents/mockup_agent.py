"""
Mockup Agent - Generates Apple-style HTML mockups
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig, AgentResult
import json


class MockupAgent(BaseAgent):
    """
    Agent responsible for generating Apple-style HTML mockups
    Creates interactive, beautiful HTML pages following AICOE design guidelines
    """
    
    def __init__(self, llm_client):
        config = AgentConfig(
            name="MockupAgent",
            description="Generates Apple-style HTML mockups",
            model="gpt-4o",
            temperature=0.6,
            max_tokens=6000
        )
        super().__init__(config, llm_client)
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Generate Apple-style HTML mockup
        
        Input:
            - use_cases: Use cases to visualize
            - project_name: Name of the project
            - structured_notes: Optional context
            
        Output:
            - mockup_html: Complete HTML page with inline CSS and JS
        """
        try:
            self.log_execution("start", "Generating HTML mockup")
            self.validate_input(input_data, ["project_name"])
            
            project_name = input_data["project_name"]
            use_cases = input_data.get("use_cases", [])
            structured_notes = input_data.get("structured_notes", {})
            
            # Prepare context
            use_cases_text = json.dumps(use_cases, indent=2) if use_cases else "No specific use cases provided"
            notes_text = json.dumps(structured_notes, indent=2) if structured_notes else "No additional context"
            
            system_message = """You are an expert UI/UX designer specializing in Apple-style, minimalist web design.
You create beautiful, modern, responsive HTML mockups with clean aesthetics and excellent user experience."""
            
            user_message = f"""Create a beautiful, Apple-style HTML mockup for the following project:

Project Name: {project_name}

Use Cases:
{use_cases_text}

Context:
{notes_text}

Design Requirements:
1. **Apple-Style Design**: Clean, minimalist, with plenty of white space
2. **Color Scheme**: 
   - Primary: #0066cc (blue)
   - Accent: #00d9ff (cyan)
   - Background: #ffffff (white)
   - Text: #1d1d1f (dark gray)
   - Secondary text: #6e6e73 (medium gray)
3. **Typography**: 
   - Use system fonts (San Francisco, -apple-system, BlinkMacSystemFont)
   - Clean hierarchy with proper font sizes and weights
4. **Layout**:
   - Navigation bar at top (sticky)
   - Hero section with project title and description
   - Features section showcasing key use cases (2-3 columns grid)
   - Interactive elements with hover effects
   - Footer with project information
5. **Responsive**: Must work on desktop and mobile
6. **Interactive**: Include smooth transitions, hover effects, and subtle animations
7. **Printer-Friendly**: Include print stylesheet
8. **Icons**: Use Unicode symbols or CSS-based icons (no external dependencies)
9. **Self-Contained**: All CSS and JavaScript must be inline (no external files)

Create a complete, production-ready HTML page that showcases the project features in an elegant way.
The mockup should be fully functional and visually stunning.

Return ONLY the complete HTML code, starting with <!DOCTYPE html>. No explanations or markdown."""

            self.log_execution("llm_call", "Generating HTML mockup")
            response = await self._call_llm(
                system_message,
                user_message,
                max_tokens=6000
            )
            
            # Clean response
            html_content = response.strip()
            if html_content.startswith("```html"):
                html_content = html_content.split("```html")[1].split("```")[0].strip()
            elif html_content.startswith("```"):
                html_content = html_content.split("```")[1].split("```")[0].strip()
            
            # Ensure it starts with <!DOCTYPE html>
            if not html_content.upper().startswith("<!DOCTYPE HTML"):
                self.logger.warning("Response doesn't start with DOCTYPE, may not be valid HTML")
            
            self.log_execution("success", f"Generated HTML mockup ({len(html_content)} characters)")
            
            return AgentResult(
                success=True,
                data={
                    "mockup_html": html_content,
                    "project_name": project_name,
                    "length": len(html_content),
                    "has_doctype": "<!DOCTYPE" in html_content
                },
                metadata={
                    "agent": self.config.name,
                    "format": "html"
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error in MockupAgent: {str(e)}")
            return AgentResult(
                success=False,
                data=None,
                error=str(e),
                metadata={"agent": self.config.name}
            )
