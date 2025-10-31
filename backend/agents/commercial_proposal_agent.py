"""
Commercial Proposal Agent - Generates professional commercial proposals
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig, AgentResult
import json
import markdown


class CommercialProposalAgent(BaseAgent):
    """
    Agent responsible for creating professional commercial proposals
    Generates pricing, timelines, and business terms for client presentations
    """
    
    def __init__(self, llm_client):
        config = AgentConfig(
            name="CommercialProposalAgent",
            description="Creates professional commercial proposals with pricing and timelines",
            model="z-ai/glm-4.6",  # GLM-4.6 via OpenRouter
            temperature=0.3,  # Lower temperature for professional business documents
            max_tokens=8000
        )
        super().__init__(config, llm_client)
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Generate commercial proposal document
        
        Input:
            - project_name: Name of the project
            - prd_markdown: PRD content for context
            - use_cases: Use cases from requirements
            - research_insights: Market research for pricing context
            
        Output:
            - proposal_markdown: Complete proposal in Markdown format
            - proposal_pdf: PDF version with AICOE branding
        """
        try:
            self.log_execution("start", "Generating commercial proposal")
            self.validate_input(input_data, ["project_name"])
            
            project_name = input_data["project_name"]
            prd_content = input_data.get("prd_markdown", "")
            use_cases = input_data.get("use_cases", [])
            research_insights = input_data.get("research_insights", {})
            
            # Prepare context
            research_text = json.dumps(research_insights, indent=2) if research_insights else "No research insights available"
            
            context_text = f"""
Project Name: {project_name}

PRD Summary:
{prd_content[:2000] if prd_content else "No PRD available"}

Use Cases:
{json.dumps(use_cases, indent=2)}

Research Insights (for pricing and market context):
{research_text[:1500]}
"""

            system_message = """You are an expert Business Development Manager at AICOE who creates compelling commercial proposals.
Your proposals are professional, data-driven, and follow AICOE branding standards.
You excel at pricing strategy, timeline estimation, and presenting business value."""

            user_message = f"""Create a comprehensive commercial proposal based on the following information:

{context_text}

CRITICAL INSTRUCTIONS:
1. Use research insights to inform competitive pricing
2. Reference industry standards for timeline estimates
3. Highlight unique value propositions and differentiators
4. Include clear pricing tiers and payment terms
5. Provide realistic project timelines with milestones
6. Address risk mitigation and quality assurance
7. Include executive summary for quick decision-making

REQUIRED SECTIONS (use this exact structure):

# Commercial Proposal: [Project Name]

## Executive Summary
- Brief overview of the solution
- Key benefits and value proposition
- Total investment and timeline summary

## 1. Solution Overview
- Problem statement
- Proposed solution
- Key features and capabilities
- Technology stack

## 2. Scope of Work
- Deliverables breakdown
- Included services
- Exclusions (out of scope)

## 3. Project Timeline
- Phase breakdown with durations
- Key milestones and dependencies
- Go-live date estimate

## 4. Pricing Structure
### Investment Breakdown
- Development costs
- Infrastructure costs
- Licensing and third-party services
- Support and maintenance

### Payment Terms
- Payment schedule
- Milestone-based payments
- Accepted payment methods

## 5. Team Composition
- Project roles and responsibilities
- Team expertise and qualifications
- Dedicated resources

## 6. Quality Assurance
- Testing methodology
- Code review process
- Performance benchmarks
- Security measures

## 7. Risk Management
- Identified risks
- Mitigation strategies
- Contingency plans

## 8. Support & Maintenance
- Post-launch support
- Maintenance packages
- SLA commitments

## 9. Terms & Conditions
- Contract duration
- Intellectual property rights
- Confidentiality
- Termination clauses

## 10. Next Steps
- Proposal validity period
- Acceptance process
- Project kickoff timeline

---
**AICOE - Transforming Ideas into Intelligent Solutions**

Generate a professional, compelling proposal that demonstrates clear ROI and business value.
Use specific numbers, timelines, and pricing (make realistic estimates based on project complexity).
"""

            # Call LLM to generate proposal
            self.log_execution("progress", "Calling LLM for proposal generation")
            
            response = await self._call_llm(system_message, user_message)
            proposal_content = response.strip()
            
            # Validate proposal has required sections
            required_sections = ["Executive Summary", "Solution Overview", "Pricing Structure", "Project Timeline"]
            missing_sections = [s for s in required_sections if s not in proposal_content]
            
            if missing_sections:
                self.logger.warning(f"Proposal missing sections: {missing_sections}")
            
            self.log_execution("success", f"Generated proposal ({len(proposal_content)} chars)")

            # Generate HTML version with AICOE branding
            self.log_execution("start", "Generating HTML version")
            proposal_html = self._generate_html(proposal_content, project_name)
            self.log_execution("success", f"Generated HTML ({len(proposal_html)} characters)")

            return AgentResult(
                success=True,
                data={
                    "proposal_markdown": proposal_content,
                    "proposal_html": proposal_html,
                    "project_name": project_name,
                    "length": len(proposal_content),
                    "sections": self._extract_sections(proposal_content)
                },
                metadata={
                    "agent": self.config.name,
                    "format": "markdown+html"
                }
            )
            
        except Exception as e:
            self.log_execution("error", f"Failed to generate proposal: {str(e)}")
            return AgentResult(
                success=False,
                error=f"Proposal generation failed: {str(e)}",
                metadata={"agent": self.config.name}
            )
    
    def _generate_html(self, markdown_content: str, project_name: str) -> str:
        """Generate comprehensive HTML from Markdown content with AICOE branding (UC001 style)"""
        # Convert Markdown to HTML
        html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])

        # AICOE-branded HTML template with UC001 styling
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - Commercial Proposal</title>
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

        .proposal-document {{
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

        .content strong {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        .content em {{
            font-style: italic;
            color: var(--text-secondary);
        }}

        .pricing-highlight {{
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.03) 0%, rgba(58, 42, 78, 0.05) 100%);
            padding: 24px;
            border-radius: 16px;
            margin: 24px 0;
            border-left: 4px solid var(--accent-pink);
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

            .proposal-document {{
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

            .proposal-document {{
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
                <h1>💼 Commercial Proposal</h1>
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
                        <span class="metadata-label">Date</span>
                        <span class="metadata-value">{self._get_current_date()}</span>
                    </div>
                </div>
            </div>
        </header>

        <div class="proposal-document">
            <div class="content">
                {html_content}
            </div>
        </div>

        <footer>
            <div class="footer-logo">AICOE</div>
            <p>© 2025 AICOE - AI Center of Excellence</p>
            <p style="margin-top: 8px;">This proposal is confidential and proprietary to AICOE</p>
        </footer>
    </div>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
"""

        return html_template
    
    def _extract_sections(self, content: str) -> list:
        """Extract section headings from markdown content"""
        sections = []
        for line in content.split('\n'):
            if line.startswith('##'):
                sections.append(line.strip('# ').strip())
        return sections
    
    def _get_current_date(self) -> str:
        """Get current date in readable format"""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")

