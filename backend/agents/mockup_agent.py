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
            description="Generates Apple-style HTML mockups with UC001 AICOE branding",
            model="openai/gpt-oss-120b",  # OpenAI GPT-OSS-120B via OpenRouter
            temperature=0.6,
            max_tokens=12000  # Increased from 6000 to handle complex mockups
        )
        super().__init__(config, llm_client)
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Generate Apple-style HTML mockup with multi-page support

        Input:
            - use_cases: Use cases to visualize
            - project_name: Name of the project
            - structured_notes: Optional context

        Output:
            - mockup_pages: Dictionary of HTML pages (index.html and additional pages)
            - mockup_html: Main index.html content (for backward compatibility)
        """
        try:
            self.log_execution("start", "Generating HTML mockup prototypes")
            self.validate_input(input_data, ["project_name"])

            project_name = input_data["project_name"]
            use_cases = input_data.get("use_cases", [])
            structured_notes = input_data.get("structured_notes", {})
            
            # Prepare context
            use_cases_text = json.dumps(use_cases, indent=2) if use_cases else "No specific use cases provided"
            notes_text = json.dumps(structured_notes, indent=2) if structured_notes else "No additional context"

            # Determine if we need multiple pages
            num_use_cases = len(use_cases) if isinstance(use_cases, list) else 0
            needs_multiple_pages = num_use_cases > 3  # If more than 3 use cases, create separate pages

            # Generate main index.html
            self.log_execution("llm_call", "Generating index.html")
            index_html = await self._generate_index_page(project_name, use_cases, structured_notes, needs_multiple_pages)

            # Store all pages
            mockup_pages = {
                "index.html": index_html
            }

            # Generate additional pages if needed
            if needs_multiple_pages and isinstance(use_cases, list):
                self.log_execution("llm_call", f"Generating {num_use_cases} additional use case pages")
                for idx, use_case in enumerate(use_cases, 1):
                    page_name = f"use-case-{idx}.html"
                    page_html = await self._generate_use_case_page(project_name, use_case, idx, num_use_cases)
                    mockup_pages[page_name] = page_html

            total_chars = sum(len(html) for html in mockup_pages.values())
            self.log_execution("success", f"Generated {len(mockup_pages)} HTML pages ({total_chars} total characters)")

            return AgentResult(
                success=True,
                data={
                    "mockup_pages": mockup_pages,
                    "mockup_html": index_html,  # Backward compatibility
                    "project_name": project_name,
                    "page_count": len(mockup_pages),
                    "total_size": total_chars
                },
                metadata={
                    "agent": self.config.name,
                    "format": "html",
                    "multi_page": needs_multiple_pages
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

    async def _generate_index_page(self, project_name: str, use_cases: list, structured_notes: dict, has_subpages: bool) -> str:
        """Generate the main index.html page"""
        use_cases_text = json.dumps(use_cases, indent=2) if use_cases else "No specific use cases provided"
        notes_text = json.dumps(structured_notes, indent=2) if structured_notes else "No additional context"

        system_message = """## ROLE AND GOAL
You are a world-class UI/UX Engineer who specializes in creating pixel-perfect, interactive, multi-page web prototypes. Your design philosophy is inspired by Apple's clean, minimalist, and high-contrast aesthetic. Your goal is to take a set of use cases and produce a fully functional, navigable set of HTML files.

## CONTEXT
You will receive the `<useCaseModel>` XML from the Blueprint Agent and the JSON data from the Data Agent.

## STEP-BY-STEP PROCESS
1. Analyze the use cases to identify the number of distinct screens required.
2. Create a main `index.html` page that serves as a dashboard or entry point, linking to each use case mockup.
3. For each `<useCase>` in the XML, create a corresponding `use-case-X.html` file that visually represents the main flow.
4. Use the synthetic JSON data to populate the mockups with realistic content.
5. Implement navigation between all pages (e.g., "Back to Home," "Next Use Case").
6. Apply the AICOE branding and design guidelines with absolute precision.
7. Return all generated files as a single JSON object.

## OUTPUT FORMAT (CRITICAL)
You MUST produce a single, valid XML document containing the mockup prototype structure. DO NOT include any other text or explanation.

<mockupPrototype>
    <title>Project Mockup Prototype</title>
    <description>A multi-page interactive prototype for the project use cases.</description>
    <screens>
        <screen id="index">
            <title>Main Dashboard</title>
            <content>The main dashboard HTML content with navigation to use cases.</content>
        </screen>
        <screen id="use-case-1">
            <title>Use Case 1: [Title]</title>
            <content>The HTML content for use case 1 mockup.</content>
        </screen>
        <!-- Add more screens as needed -->
    </screens>
</mockupPrototype>

## GUIDELINES & CONSTRAINTS (NON-NEGOTIABLE)
- The XML must contain all the necessary information to generate the HTML mockups.
- Each screen should have a unique id and contain the HTML content structure.
- Include navigation elements between screens.
- Apply AICOE branding and design guidelines.
- Your entire response MUST be only the XML document."""

        navigation_instruction = ""
        if has_subpages:
            navigation_instruction = f"""
IMPORTANT: This is a MULTI-PAGE prototype. Create navigation links to use case detail pages:
- Link format: <a href="use-case-1.html">Use Case 1</a>, <a href="use-case-2.html">Use Case 2</a>, etc.
- Add a "View Details" button on each use case card that links to its detail page
- Include a navigation menu with links to all use case pages
"""

        user_message = f"""Create a beautiful, Apple-style HTML mockup (index.html) with UC001 AICOE branding for the following project:

Project Name: {project_name}

Use Cases:
{use_cases_text}

Context:
{notes_text}

{navigation_instruction}

MANDATORY UC001 AICOE DESIGN REQUIREMENTS:

1. **UC001 AICOE Color Palette** (MUST USE THESE EXACT COLORS):
   CSS Variables to define:
   /* AICOE Primary Colors */
   --primary-navy: #1a1a2e;
   --midnight-blue: #2a2a3e;
   --deep-purple: #3a2a4e;

   /* AICOE Accent Colors */
   --accent-pink: #ff69b4;
   --accent-cyan: #00ffcc;
   --accent-turquoise: #00e5b3;
   --accent-mint: #00cc99;

   /* Supporting Colors */
   --text-primary: #1a1a1a;
   --text-secondary: #666666;
   --bg-white: #ffffff;
   --bg-gray: #f5f5f7;
   --border-gray: #d2d2d7;

   /* Status Colors */
   --success-green: #00cc99;
   --warning-orange: #ff69b4;
   --danger-red: #ff1493;

   /* Shadows */
   --shadow: 0 2px 16px rgba(26, 26, 46, 0.08);
   --shadow-hover: 0 4px 24px rgba(26, 26, 46, 0.12);

2. **Lucide Icons Integration** (MANDATORY):
   - Include Lucide Icons CDN: <script src="https://unpkg.com/lucide@latest"></script>
   - Initialize icons with: lucide.createIcons();
   - Use icons for: navigation (Menu, Home, FileText, Layers, Database, Layout, CheckCircle, Settings)
   - Use icons for features (Zap, Target, Users, TrendingUp, Shield, Clock, etc.)
   - Example: <i data-lucide="home"></i>

3. **UC001 Apple-Style Design**:
   - Clean, minimalist layout with generous white space
   - System fonts: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Segoe UI', sans-serif
   - Smooth transitions (0.3s ease)
   - UC001 shadows: box-shadow: var(--shadow) and var(--shadow-hover)
   - Rounded corners: border-radius: 24px for cards, 12px for buttons
   - Font smoothing: -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;

4. **Layout Structure**:
   - Header with gradient text (h1): background: linear-gradient(135deg, var(--primary-navy) 0%, var(--deep-purple) 50%, var(--accent-pink) 100%);
   - Metadata grid with icons and info
   - Content sections with white background cards
   - Interactive elements with hover effects (transform: translateY(-2px))
   - Footer with AICOE branding and gradient logo

5. **Printer-Friendly CSS** (MANDATORY @media print rules):
   ```css
   @media print {{
     /* Hide navigation, buttons, interactive elements */
     nav, .no-print, button {{ display: none !important; }}
     /* Ensure readable fonts */
     body {{ font-size: 12pt; color: #000; background: #fff; }}
     /* Remove shadows and effects */
     * {{ box-shadow: none !important; text-shadow: none !important; }}
     /* Page breaks */
     .page-break {{ page-break-before: always; }}
     h1, h2, h3 {{ page-break-after: avoid; }}
     /* Show URLs for links */
     a[href]:after {{ content: " (" attr(href) ")"; }}
   }}
   ```

6. **Responsive Design**:
   - Mobile-first approach
   - Breakpoints: 768px (tablet), 1024px (desktop)
   - Flexible grid with CSS Grid or Flexbox
   - Container max-width: 1200px

7. **Interactive Elements**:
   - Smooth hover effects on cards (transform: translateY(-2px))
   - Button hover states with color transitions
   - Box shadow transitions on hover
   - Gradient text effects for headings

8. **UC001 AICOE Branding Elements**:
   - Header with gradient text using UC001 colors
   - Metadata section with icons (Calendar, User, Tag, Clock)
   - Footer: "Powered by AICOE Multi-Agent Platform"
   - Logo with gradient effect
   - Color scheme strictly follows UC001 palette
   - Professional, enterprise-grade appearance

9. **Self-Contained**:
   - All CSS inline in <style> tag
   - All JavaScript inline in <script> tag
   - Only external dependency: Lucide Icons CDN

IMPORTANT: Return ONLY the complete HTML code, starting with <!DOCTYPE html>.
The HTML must be production-ready, fully functional, and visually stunning.
NO explanations, NO markdown code blocks, JUST the raw HTML."""

        response = await self._call_llm(
            system_message,
            user_message,
            max_tokens=8000
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

        return html_content

    async def _generate_use_case_page(self, project_name: str, use_case: dict, page_num: int, total_pages: int) -> str:
        """Generate a detailed use case page"""
        use_case_text = json.dumps(use_case, indent=2)

        system_message = """You are an expert UI/UX designer specializing in Apple-style, minimalist web design with UC001 AICOE branding.
You create beautiful, modern, responsive HTML mockups with clean aesthetics, Lucide icons, and excellent user experience."""

        user_message = f"""Create a detailed use case page (use-case-{page_num}.html) with UC001 AICOE branding:

Project Name: {project_name}
Page: {page_num} of {total_pages}

Use Case Details:
{use_case_text}

REQUIREMENTS:
1. Use the same UC001 AICOE color palette and design system as index.html (--primary-navy, --accent-pink, --accent-cyan, etc.)
2. Include navigation: "Back to Home" link to index.html
3. Include "Previous" and "Next" links to navigate between use case pages (use-case-{page_num-1}.html and use-case-{page_num+1}.html)
4. Display use case details in a beautiful, readable format with gradient text headings
5. Include Lucide icons CDN and initialize with lucide.createIcons()
6. Make it responsive and printer-friendly with @media print rules
7. Add interactive elements (accordions, tabs, etc.) to organize information
8. Use UC001 shadows (--shadow and --shadow-hover) and border-radius: 24px for cards
9. Apply font smoothing and SF Pro Display fonts

Return ONLY the complete HTML code, starting with <!DOCTYPE html>.
NO explanations, NO markdown code blocks, JUST the raw HTML."""

        response = await self._call_llm(
            system_message,
            user_message,
            max_tokens=8000
        )

        # Clean response
        html_content = response.strip()
        if html_content.startswith("```html"):
            html_content = html_content.split("```html")[1].split("```")[0].strip()
        elif html_content.startswith("```"):
            html_content = html_content.split("```")[1].split("```")[0].strip()

        return html_content
