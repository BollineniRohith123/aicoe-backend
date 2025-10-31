"""
System Architecture Diagram Agent - Generates visual system architecture diagrams
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig, AgentResult
import json


class ArchitectureDiagramAgent(BaseAgent):
    """
    Agent responsible for creating interactive system architecture diagrams
    Generates HTML with embedded Mermaid diagrams showing component relationships
    """
    
    def __init__(self, llm_client):
        config = AgentConfig(
            name="ArchitectureDiagramAgent",
            description="Creates interactive system architecture diagrams",
            model="z-ai/glm-4.6",  # GLM-4.6 via OpenRouter
            temperature=0.3,
            max_tokens=8000
        )
        super().__init__(config, llm_client)
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Generate system architecture diagram
        
        Input:
            - project_name: Name of the project
            - enrichment: Technical architecture from knowledge base
            - use_cases: Use cases for understanding system flows
            - research_insights: Technical patterns and best practices
            
        Output:
            - architecture_html: Interactive HTML with Mermaid diagrams
        """
        try:
            self.log_execution("start", "Generating architecture diagram")
            self.validate_input(input_data, ["project_name"])
            
            project_name = input_data["project_name"]
            enrichment = input_data.get("enrichment", {})
            use_cases = input_data.get("use_cases", [])
            research_insights = input_data.get("research_insights", {})
            
            # Prepare context
            research_text = json.dumps(research_insights, indent=2) if research_insights else "No research insights available"
            
            context_text = f"""
Project Name: {project_name}

Technical Architecture:
{json.dumps(enrichment, indent=2)}

Use Cases:
{json.dumps(use_cases[:3], indent=2) if use_cases else "No use cases"}

Research Insights (for architecture patterns):
{research_text[:1500]}
"""

            system_message = """You are an expert Solution Architect at AICOE who creates clear, comprehensive system architecture diagrams.
You excel at visualizing complex systems using Mermaid diagram syntax.
Your diagrams are well-organized, easy to understand, and follow industry best practices."""

            user_message = f"""Create comprehensive system architecture diagrams using Mermaid syntax based on the following information:

{context_text}

CRITICAL INSTRUCTIONS:
1. Create multiple Mermaid diagrams showing different architectural views
2. Include: High-Level Architecture, Component Diagram, Data Flow, Deployment Architecture
3. Use research insights to incorporate industry-standard patterns
4. Show clear relationships between components
5. Include external systems and integrations
6. Use proper Mermaid syntax (graph TD, C4Context, etc.)
7. Add descriptive labels and annotations

REQUIRED OUTPUT FORMAT:
Return a JSON object with the following structure:

{{
    "project_name": "{project_name}",
    "diagrams": [
        {{
            "title": "High-Level System Architecture",
            "description": "Overview of the entire system and its major components",
            "type": "graph TD",
            "mermaid_code": "graph TD\\n    A[Component A] --> B[Component B]\\n    B --> C[Component C]"
        }},
        {{
            "title": "Component Architecture",
            "description": "Detailed view of system components and their interactions",
            "type": "graph LR",
            "mermaid_code": "..."
        }},
        {{
            "title": "Data Flow Diagram",
            "description": "How data flows through the system",
            "type": "graph TD",
            "mermaid_code": "..."
        }},
        {{
            "title": "Deployment Architecture",
            "description": "Infrastructure and deployment topology",
            "type": "graph TB",
            "mermaid_code": "..."
        }}
    ],
    "components": [
        {{
            "name": "Frontend Application",
            "type": "Web Application",
            "technology": "React.js",
            "description": "User-facing web interface",
            "responsibilities": ["User interaction", "Data visualization"]
        }}
    ],
    "integrations": [
        {{
            "name": "External API",
            "type": "REST API",
            "purpose": "Third-party data integration"
        }}
    ],
    "infrastructure": {{
        "hosting": "Cloud-based (AWS/Azure/GCP)",
        "database": "PostgreSQL / MongoDB",
        "caching": "Redis",
        "cdn": "CloudFront / Cloudflare"
    }}
}}

Generate realistic, detailed Mermaid diagrams with at least 8-12 components per diagram.
Use proper Mermaid syntax with correct escaping for newlines (\\n).
Return ONLY valid JSON, no additional text.
"""

            # Call LLM to generate architecture
            self.log_execution("progress", "Calling LLM for architecture generation")
            
            response = await self._call_llm(system_message, user_message)
            
            # Parse JSON response
            try:
                # Clean response
                cleaned_response = response.strip()
                if cleaned_response.startswith('```'):
                    cleaned_response = cleaned_response.split('```')[1]
                    if cleaned_response.startswith('json'):
                        cleaned_response = cleaned_response[4:]
                    cleaned_response = cleaned_response.strip()
                
                architecture_data = json.loads(cleaned_response)
                self.log_execution("success", f"Generated {len(architecture_data.get('diagrams', []))} diagrams")
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse architecture JSON: {str(e)}")
                # Create fallback structure
                architecture_data = {
                    "project_name": project_name,
                    "diagrams": [],
                    "error": "Failed to parse LLM response"
                }
            
            # Generate HTML with embedded Mermaid diagrams
            self.log_execution("start", "Generating interactive HTML")
            architecture_html = self._generate_html(architecture_data, project_name)
            self.log_execution("success", f"Generated HTML ({len(architecture_html)} chars)")
            
            return AgentResult(
                success=True,
                data={
                    "architecture_html": architecture_html,
                    "architecture_data": architecture_data,
                    "project_name": project_name,
                    "diagram_count": len(architecture_data.get('diagrams', []))
                },
                metadata={
                    "agent": self.config.name,
                    "format": "html"
                }
            )
            
        except Exception as e:
            self.log_execution("error", f"Failed to generate architecture: {str(e)}")
            return AgentResult(
                success=False,
                error=f"Architecture generation failed: {str(e)}",
                metadata={"agent": self.config.name}
            )
    
    def _generate_html(self, architecture_data: dict, project_name: str) -> str:
        """Generate interactive HTML with Mermaid diagrams and AICOE branding"""
        diagrams = architecture_data.get('diagrams', [])
        components = architecture_data.get('components', [])
        integrations = architecture_data.get('integrations', [])
        infrastructure = architecture_data.get('infrastructure', {})
        
        # Generate diagram HTML sections
        diagram_sections = []
        for idx, diagram in enumerate(diagrams):
            mermaid_code = diagram.get('mermaid_code', '').replace('\\n', '\n')
            diagram_sections.append(f"""
            <div class="diagram-section">
                <h2>{diagram.get('title', f'Diagram {idx+1}')}</h2>
                <p class="diagram-description">{diagram.get('description', '')}</p>
                <div class="mermaid-container">
                    <pre class="mermaid">
{mermaid_code}
                    </pre>
                </div>
            </div>
            """)
        
        # Generate components table
        components_html = '<table class="components-table"><tr><th>Component</th><th>Type</th><th>Technology</th><th>Description</th></tr>'
        for comp in components:
            components_html += f"""
            <tr>
                <td><strong>{comp.get('name', '')}</strong></td>
                <td>{comp.get('type', '')}</td>
                <td><code>{comp.get('technology', '')}</code></td>
                <td>{comp.get('description', '')}</td>
            </tr>
            """
        components_html += '</table>'
        
        # Generate integrations list
        integrations_html = '<ul class="integrations-list">'
        for integration in integrations:
            integrations_html += f'<li><strong>{integration.get("name", "")}</strong> ({integration.get("type", "")}): {integration.get("purpose", "")}</li>'
        integrations_html += '</ul>'
        
        # Full HTML template with AICOE branding
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - System Architecture</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary-navy: #1a1a2e;
            --midnight-blue: #2a2a3e;
            --deep-purple: #3a2a4e;
            --accent-pink: #ff69b4;
            --accent-cyan: #00ffcc;
            --accent-turquoise: #00e5b3;
            --text-primary: #1a1a1a;
            --text-secondary: #666666;
            --bg-white: #ffffff;
            --bg-gray: #f5f5f7;
            --border-gray: #d2d2d7;
            --shadow: 0 2px 16px rgba(26, 26, 46, 0.08);
            --shadow-hover: 0 4px 24px rgba(26, 26, 46, 0.12);
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif;
            background: var(--bg-gray);
            color: var(--text-primary);
            line-height: 1.6;
            font-size: 17px;
            -webkit-font-smoothing: antialiased;
        }}

        .container {{
            max-width: 1400px;
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

        .diagram-section {{
            background: var(--bg-white);
            border-radius: 24px;
            padding: 48px;
            margin-bottom: 32px;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
        }}

        .diagram-section:hover {{
            box-shadow: var(--shadow-hover);
            transform: translateY(-2px);
        }}

        h2 {{
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 12px;
            color: var(--primary-navy);
        }}

        .diagram-description {{
            font-size: 17px;
            color: var(--text-secondary);
            margin-bottom: 24px;
        }}

        .mermaid-container {{
            background: var(--bg-gray);
            padding: 32px;
            border-radius: 16px;
            overflow-x: auto;
        }}

        .components-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        .components-table th {{
            background: var(--primary-navy);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        .components-table td {{
            padding: 12px;
            border-bottom: 1px solid var(--border-gray);
        }}

        .components-table tr:hover {{
            background: var(--bg-gray);
        }}

        code {{
            background: var(--bg-gray);
            padding: 2px 8px;
            border-radius: 4px;
            color: var(--accent-pink);
            font-family: 'SF Mono', Monaco, monospace;
        }}

        .integrations-list {{
            list-style: none;
            padding: 0;
        }}

        .integrations-list li {{
            padding: 12px;
            margin-bottom: 8px;
            background: var(--bg-gray);
            border-radius: 8px;
            border-left: 4px solid var(--accent-cyan);
        }}

        .info-box {{
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

            .diagram-section {{
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

            .diagram-section {{
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
                <h1>🏗️ System Architecture</h1>
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
                        <span class="metadata-label">Document Type</span>
                        <span class="metadata-value">Architecture Diagrams</span>
                    </div>
                </div>
            </div>
        </header>

        {''.join(diagram_sections)}

        <div class="diagram-section">
            <h2>System Components</h2>
            <p class="diagram-description">Detailed breakdown of all system components and their technologies</p>
            {components_html}
        </div>

        <div class="diagram-section">
            <h2>External Integrations</h2>
            <p class="diagram-description">Third-party services and APIs integrated into the system</p>
            {integrations_html}
        </div>

        <div class="diagram-section">
            <h2>Infrastructure Overview</h2>
            <p class="diagram-description">Hosting and infrastructure details</p>
            <div class="info-box">
                <p><strong>Hosting:</strong> {infrastructure.get('hosting', 'Not specified')}</p>
                <p><strong>Database:</strong> {infrastructure.get('database', 'Not specified')}</p>
                <p><strong>Caching:</strong> {infrastructure.get('caching', 'Not specified')}</p>
                <p><strong>CDN:</strong> {infrastructure.get('cdn', 'Not specified')}</p>
            </div>
        </div>

        <footer>
            <div class="footer-logo">AICOE</div>
            <p>© 2025 AICOE - AI Center of Excellence</p>
            <p style="margin-top: 8px;">Interactive Architecture Diagrams</p>
        </footer>
    </div>

    <script>
        mermaid.initialize({{ 
            startOnLoad: true,
            theme: 'default',
            themeVariables: {{
                primaryColor: '#1a1a2e',
                primaryTextColor: '#fff',
                primaryBorderColor: '#00ffcc',
                lineColor: '#ff69b4',
                secondaryColor: '#3a2a4e',
                tertiaryColor: '#f5f5f7'
            }}
        }});
        lucide.createIcons();
    </script>
</body>
</html>
"""
        
        return html_template

