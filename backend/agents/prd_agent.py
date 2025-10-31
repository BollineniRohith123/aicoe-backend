"""
PRD Agent - Assembles comprehensive Product Requirements Document
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig, AgentResult
import json
import markdown


class PRDAgent(BaseAgent):
    """
    Agent responsible for creating comprehensive PRD documents
    Combines all previous agent outputs into a structured PRD
    """
    
    def __init__(self, llm_client):
        config = AgentConfig(
            name="PRDAgent",
            description="Creates comprehensive Product Requirements Documents",
            model="z-ai/glm-4.6",  # GLM-4.6 via OpenRouter
            temperature=0.4,
            max_tokens=8000  # Increased from 6000 to handle complex PRDs
        )
        super().__init__(config, llm_client)
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Generate comprehensive PRD document
        
        Input:
            - structured_notes: From TranscriptAgent
            - use_cases: From RequirementsAgent
            - business_requirements: From RequirementsAgent
            - project_name: Name of the project
            
        Output:
            - prd_markdown: Complete PRD in Markdown format
            - prd_sections: Structured sections of the PRD
        """
        try:
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
"""

            system_message = """You are an expert Product Manager at AICOE who creates world-class Product Requirements Documents (PRDs).
Your PRDs are comprehensive, well-structured, follow AICOE branding standards, and adhere to industry best practices.
You MUST follow the AICOE PRD template exactly and MUST incorporate research insights throughout the document."""

            user_message = f"""Create a comprehensive Product Requirements Document (PRD) with AICOE branding based on the following information:

{context_text}

CRITICAL INSTRUCTIONS FOR USING RESEARCH INSIGHTS:
1. Reference specific competitors and their features in the competitive analysis section
2. Incorporate industry trends into the market context and problem statement
3. Use best practices from research to inform technical architecture and design decisions
4. Apply technical standards from research to non-functional requirements
5. Consider user expectations from research when defining user personas and features
6. Include regulatory requirements from research in compliance sections
7. Add a dedicated "Market Research & Competitive Analysis" section

MANDATORY AICOE PRD TEMPLATE STRUCTURE:

---
**AICOE Product Requirements Document**

**Document Classification:** Internal - Confidential
**Version:** 1.0
**Date:** {{current_date}}
**Prepared By:** AICOE Multi-Agent Platform
**Project:** {project_name}

---

# {project_name} - Product Requirements Document

## 1. Executive Summary
Brief overview of the project, its purpose, expected impact, and business value.
Include key stakeholders and target timeline.

## 2. Goals & Objectives
Clear, measurable SMART objectives this product aims to achieve.
- Business goals
- User goals
- Technical goals

## 3. Problem Statement
- What problem are we solving?
- Who has this problem?
- Current pain points and limitations
- Opportunity size and market context

## 4. Market Research & Competitive Analysis
**IMPORTANT: Use research insights extensively in this section**
- **Industry Trends:** Key trends shaping the market (reference specific trends from research)
- **Competitive Landscape:** Analysis of competitors and their offerings (reference specific competitors from research)
- **Market Opportunities:** Gaps in the market and differentiation opportunities
- **Best Practices:** Industry best practices to adopt (from research insights)
- **Technical Standards:** Relevant technical standards and frameworks (from research)
- **User Expectations:** What users expect based on market analysis (from research)
- **Regulatory Landscape:** Compliance requirements and regulations (from research)

## 5. User Personas & Stakeholders
Detailed user personas with:
- Role/Title
- Goals and motivations
- Pain points
- Technical proficiency
Key stakeholders and their interests.

## 6. Features & User Stories
Detailed features organized by priority (Must-Have, Should-Have, Nice-to-Have).
User stories in format: "As a [role], I want [feature] so that [benefit]"

## 7. Use Cases
Detailed use cases with:
- Use Case ID and Name
- Actors
- Preconditions
- Main Flow
- Alternative Flows
- Postconditions
- Success Criteria

## 8. Functional Requirements
Specific, testable functional requirements organized by feature area.
Format: FR-XX: [Requirement description]
Each requirement should be:
- Specific and measurable
- Testable
- Traceable to use cases

## 9. Non-Functional Requirements
- **Performance:** Response times, throughput, scalability targets
- **Security:** Authentication, authorization, data protection, compliance (reference regulatory requirements from research)
- **Usability:** User experience standards, accessibility (WCAG 2.1)
- **Reliability:** Uptime targets, error handling, disaster recovery
- **Maintainability:** Code quality, documentation standards

## 10. Technical Architecture
High-level technical approach (aligned with technical standards from research):
- System components and their interactions
- Technology stack recommendations
- Integration points and APIs
- Data flow and storage
- Deployment architecture

## 11. Acceptance Criteria
Clear, testable acceptance criteria for each major feature.
Format: AC-XX: [Criteria description]

## 12. Success Metrics
Key Performance Indicators (KPIs) to measure product success:
- User adoption metrics
- Business impact metrics
- Technical performance metrics
- User satisfaction metrics

## 13. Timeline & Milestones
Suggested development phases:
- Phase 1: [Scope and timeline]
- Phase 2: [Scope and timeline]
- Phase 3: [Scope and timeline]
Key milestones and dependencies.

## 14. Risks & Mitigation
| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| [Risk description] | High/Med/Low | High/Med/Low | [Mitigation approach] |

## 15. Dependencies & Assumptions
**Dependencies:**
- External systems/APIs
- Third-party services
- Team resources

**Assumptions:**
- Technical assumptions
- Business assumptions
- User behavior assumptions

## 16. Open Questions
Unresolved questions requiring stakeholder input or further research.

---

**Document Footer:**
*This PRD was generated by the AICOE Multi-Agent Platform using AI-powered analysis.*
*For questions or feedback, contact the AICOE Product Team.*

---

IMPORTANT:
- Follow this exact structure and section order
- Use professional, clear language
- Be specific and actionable
- Include tables where appropriate
- Make requirements testable and measurable
- Return ONLY the Markdown content, no code blocks or explanations"""

            self.log_execution("llm_call", "Generating PRD document")

            # Retry logic for handling LLM failures
            max_retries = 2
            prd_content = None

            for attempt in range(max_retries):
                try:
                    response = await self._call_llm(
                        system_message,
                        user_message,
                        max_tokens=8000  # Increased from 6000 to handle complex PRDs
                    )

                    # Clean markdown if wrapped in code blocks
                    prd_content = response.strip()
                    if prd_content.startswith("```markdown"):
                        prd_content = prd_content.split("```markdown")[1].split("```")[0].strip()
                    elif prd_content.startswith("```"):
                        prd_content = prd_content.split("```")[1].split("```")[0].strip()

                    # If we got here, the call succeeded
                    break

                except Exception as e:
                    if attempt < max_retries - 1:
                        self.log_execution("warning", f"LLM call failed (attempt {attempt + 1}/{max_retries}): {str(e)}")
                        # Retry with a simpler prompt
                        user_message = f"""Based on the following information, generate a comprehensive PRD document:

Project: {project_name}

Structured Notes:
{json.dumps(structured_notes, indent=2)}

Use Cases:
{json.dumps(use_cases, indent=2)}

Business Requirements:
{json.dumps(business_reqs, indent=2)}

Generate a complete PRD document following the AICOE template structure."""
                        continue
                    else:
                        # Last attempt failed, re-raise the exception
                        raise

            if prd_content is None:
                raise Exception("Failed to generate PRD after all retry attempts")

            self.log_execution("success", f"Generated PRD ({len(prd_content)} characters)")

            # Generate HTML version with AICOE branding
            self.log_execution("start", "Generating HTML version")
            prd_html = self._generate_html(prd_content, project_name)
            self.log_execution("success", f"Generated HTML ({len(prd_html)} characters)")

            return AgentResult(
                success=True,
                data={
                    "prd_markdown": prd_content,
                    "prd_html": prd_html,
                    "project_name": project_name,
                    "length": len(prd_content),
                    "sections": self._extract_sections(prd_content)
                },
                metadata={
                    "agent": self.config.name,
                    "format": "markdown+html"
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
    
    def _extract_sections(self, markdown_text: str) -> list:
        """Extract section headings from markdown"""
        sections = []
        for line in markdown_text.split('\n'):
            if line.startswith('## '):
                sections.append(line.replace('## ', '').strip())
        return sections

    def _generate_html(self, markdown_content: str, project_name: str) -> str:
        """
        Generate comprehensive HTML from Markdown content with AICOE branding

        Args:
            markdown_content: PRD content in Markdown format
            project_name: Name of the project

        Returns:
            Complete HTML document as string
        """
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code', 'toc'])

        # Extract sections for table of contents
        sections = self._extract_sections(markdown_content)

        # AICOE-branded HTML template with UC001 styling
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - Product Requirements Document</title>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
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

            /* Shadows */
            --shadow: 0 2px 16px rgba(26, 26, 46, 0.08);
            --shadow-hover: 0 4px 24px rgba(26, 26, 46, 0.12);
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', 'Segoe UI', sans-serif;
            background: var(--bg-gray);
            color: var(--text-primary);
            line-height: 1.6;
            font-size: 17px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        header {{
            background: var(--bg-white);
            padding: 60px 0;
            text-align: center;
            margin-bottom: 40px;
            border-radius: 24px;
            box-shadow: var(--shadow);
        }}

        .header-content {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 40px;
        }}

        h1 {{
            font-size: 48px;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 16px;
            background: linear-gradient(135deg, var(--primary-navy) 0%, var(--deep-purple) 50%, var(--accent-pink) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .subtitle {{
            font-size: 21px;
            color: var(--text-secondary);
            margin-bottom: 24px;
            line-height: 1.5;
        }}

        .metadata {{
            display: flex;
            justify-content: center;
            gap: 32px;
            flex-wrap: wrap;
            margin-top: 32px;
            padding-top: 32px;
            border-top: 1px solid var(--border-gray);
        }}

        .metadata-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .metadata-label {{
            font-size: 13px;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }}

        .metadata-value {{
            font-size: 17px;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .prd-document {{
            background: var(--bg-white);
            border-radius: 24px;
            padding: 48px;
            margin-bottom: 32px;
            box-shadow: var(--shadow);
        }}

        .content h2 {{
            font-size: 32px;
            font-weight: 700;
            margin: 40px 0 20px 0;
            color: var(--primary-navy);
            padding-bottom: 12px;
            border-bottom: 2px solid var(--bg-gray);
        }}

        .content h3 {{
            font-size: 24px;
            font-weight: 600;
            margin: 32px 0 16px 0;
            color: var(--text-primary);
        }}

        .content h4 {{
            font-size: 20px;
            font-weight: 600;
            margin: 24px 0 12px 0;
            color: var(--text-primary);
        }}

        .content p {{
            margin-bottom: 16px;
            line-height: 1.7;
            color: var(--text-primary);
        }}

        .content ul, .content ol {{
            margin-bottom: 16px;
            padding-left: 24px;
        }}

        .content li {{
            margin-bottom: 8px;
            color: var(--text-primary);
        }}

        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            background: var(--bg-white);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow);
        }}

        .content th {{
            background: var(--primary-navy);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        .content td {{
            padding: 12px;
            border-bottom: 1px solid var(--border-gray);
        }}

        .content tr:hover {{
            background: var(--bg-gray);
        }}

        .content code {{
            background: var(--bg-gray);
            padding: 2px 8px;
            border-radius: 4px;
            color: var(--accent-pink);
            font-family: 'SF Mono', Monaco, monospace;
            font-size: 15px;
        }}

        .content pre {{
            background: var(--bg-gray);
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid var(--accent-cyan);
            overflow-x: auto;
            margin: 20px 0;
        }}

        .content pre code {{
            background: transparent;
            padding: 0;
        }}

        .content blockquote {{
            border-left: 4px solid var(--accent-cyan);
            padding-left: 20px;
            margin: 20px 0;
            color: var(--text-secondary);
            font-style: italic;
        }}

        .content strong {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        .content em {{
            font-style: italic;
            color: var(--text-secondary);
        }}

        footer {{
            text-align: center;
            padding: 60px 20px 40px;
            color: var(--text-secondary);
            font-size: 15px;
        }}

        .footer-logo {{
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-navy) 0%, var(--accent-pink) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 12px;
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 36px;
            }}

            .subtitle {{
                font-size: 19px;
            }}

            .prd-document {{
                padding: 32px 24px;
            }}

            .metadata {{
                gap: 20px;
            }}
        }}

        @media print {{
            * {{
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }}

            body {{
                background: white;
            }}

            .container {{
                max-width: 100%;
                padding: 20px;
            }}

            header {{
                margin-bottom: 30px;
                page-break-after: avoid;
            }}

            h1 {{
                font-size: 36px;
                color: var(--text-primary) !important;
                -webkit-text-fill-color: var(--text-primary) !important;
            }}

            .prd-document {{
                break-inside: avoid;
                page-break-inside: avoid;
                box-shadow: none;
                border: 1px solid var(--border-gray);
                margin-bottom: 20px;
                padding: 32px;
            }}

            footer {{
                page-break-before: always;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-content">
                <h1>📋 Product Requirements Document</h1>
                <p class="subtitle">{project_name}</p>
                <div class="metadata">
                    <div class="metadata-item">
                        <span class="metadata-label">Project</span>
                        <span class="metadata-value">{project_name}</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Version</span>
                        <span class="metadata-value">1.0</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Generated by</span>
                        <span class="metadata-value">AICOE Platform</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Classification</span>
                        <span class="metadata-value">Internal - Confidential</span>
                    </div>
                </div>
            </div>
        </header>

        <div class="prd-document">
            <div class="content">
                {html_content}
            </div>
        </div>

        <footer>
            <div class="footer-logo">AICOE</div>
            <p>© 2025 AICOE - AI Center of Excellence</p>
            <p style="margin-top: 8px;">Transforming Ideas into Intelligent Solutions</p>
        </footer>
    </div>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
"""

        return html_template
