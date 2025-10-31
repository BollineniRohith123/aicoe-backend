"""
Bill of Materials (BOM) Agent - Generates detailed component and resource listings
"""
from typing import Dict, Any
from .base_agent import BaseAgent, AgentConfig, AgentResult
import json
import markdown


class BOMAgent(BaseAgent):
    """
    Agent responsible for creating detailed Bill of Materials
    Lists all components, resources, dependencies, and cost estimates
    """
    
    def __init__(self, llm_client):
        config = AgentConfig(
            name="BOMAgent",
            description="Creates detailed Bill of Materials with cost estimates",
            model="z-ai/glm-4.6",  # GLM-4.6 via OpenRouter
            temperature=0.2,  # Very low temperature for precise technical specifications
            max_tokens=8000
        )
        super().__init__(config, llm_client)
    
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Generate Bill of Materials document
        
        Input:
            - project_name: Name of the project
            - use_cases: Use cases from requirements
            - enrichment: Technical architecture from knowledge base
            - research_insights: Technical standards and best practices
            
        Output:
            - bom_json: Structured BOM data
            - bom_pdf: PDF version with AICOE branding
        """
        try:
            self.log_execution("start", "Generating Bill of Materials")
            self.validate_input(input_data, ["project_name"])
            
            project_name = input_data["project_name"]
            use_cases = input_data.get("use_cases", [])
            enrichment = input_data.get("enrichment", {})
            research_insights = input_data.get("research_insights", {})
            
            # Prepare context
            research_text = json.dumps(research_insights, indent=2) if research_insights else "No research insights available"
            
            context_text = f"""
Project Name: {project_name}

Use Cases:
{json.dumps(use_cases, indent=2)}

Technical Architecture:
{json.dumps(enrichment, indent=2)}

Research Insights (for technical standards):
{research_text[:1500]}
"""

            system_message = """You are an expert Technical Architect and Cost Estimator at AICOE.
You create comprehensive Bill of Materials (BOM) documents that list all technical components, resources, and dependencies.
Your BOMs are detailed, accurate, and follow industry standards for cost estimation."""

            user_message = f"""Create a comprehensive Bill of Materials (BOM) based on the following information:

{context_text}

CRITICAL INSTRUCTIONS:
1. Use research insights to identify industry-standard components and tools
2. Include all technical dependencies (frameworks, libraries, services)
3. Provide realistic cost estimates for each component
4. Specify quantities, units, and specifications
5. Categorize components logically (infrastructure, software, services, etc.)
6. Include both one-time and recurring costs
7. Add notes for procurement and licensing requirements

REQUIRED STRUCTURE (return as valid JSON):

{{
    "project_name": "{project_name}",
    "generated_date": "YYYY-MM-DD",
    "version": "1.0",
    "summary": {{
        "total_components": 0,
        "total_one_time_cost": 0,
        "total_recurring_cost_monthly": 0,
        "total_recurring_cost_annual": 0,
        "currency": "USD"
    }},
    "categories": [
        {{
            "category_name": "Infrastructure & Hosting",
            "description": "Cloud infrastructure and hosting services",
            "items": [
                {{
                    "item_id": "INF-001",
                    "name": "Cloud Server Instance",
                    "description": "Production server with specifications",
                    "quantity": 2,
                    "unit": "instances",
                    "specifications": {{
                        "cpu": "4 vCPUs",
                        "memory": "16 GB RAM",
                        "storage": "100 GB SSD"
                    }},
                    "vendor": "AWS/Azure/GCP",
                    "cost_type": "recurring",
                    "unit_cost": 150.00,
                    "total_cost_monthly": 300.00,
                    "total_cost_annual": 3600.00,
                    "procurement_notes": "Reserved instance for cost savings"
                }}
            ]
        }},
        {{
            "category_name": "Software & Frameworks",
            "description": "Development frameworks and libraries",
            "items": []
        }},
        {{
            "category_name": "Third-Party Services",
            "description": "External APIs and SaaS services",
            "items": []
        }},
        {{
            "category_name": "Licenses & Subscriptions",
            "description": "Software licenses and subscriptions",
            "items": []
        }},
        {{
            "category_name": "Development Tools",
            "description": "IDEs, testing tools, CI/CD",
            "items": []
        }},
        {{
            "category_name": "Security & Compliance",
            "description": "Security tools and compliance services",
            "items": []
        }},
        {{
            "category_name": "Monitoring & Analytics",
            "description": "Monitoring, logging, and analytics tools",
            "items": []
        }},
        {{
            "category_name": "Human Resources",
            "description": "Team members and their roles",
            "items": []
        }}
    ],
    "notes": [
        "All costs are estimates and subject to change",
        "Recurring costs are calculated on a monthly basis",
        "Volume discounts may apply for annual commitments"
    ],
    "assumptions": [
        "Production environment with high availability",
        "Standard support tier for all services",
        "US-based infrastructure"
    ]
}}

Generate a comprehensive, realistic BOM with at least 20-30 components across all categories.
Include specific vendor names, version numbers, and detailed specifications.
Ensure all costs are realistic based on current market rates.
Return ONLY valid JSON, no additional text.
"""

            # Call LLM to generate BOM
            self.log_execution("progress", "Calling LLM for BOM generation")
            
            response = await self._call_llm(system_message, user_message)
            
            # Parse JSON response
            try:
                # Clean response (remove markdown code blocks if present)
                cleaned_response = response.strip()
                if cleaned_response.startswith('```'):
                    cleaned_response = cleaned_response.split('```')[1]
                    if cleaned_response.startswith('json'):
                        cleaned_response = cleaned_response[4:]
                    cleaned_response = cleaned_response.strip()
                
                bom_data = json.loads(cleaned_response)
                self.log_execution("success", f"Generated BOM with {len(bom_data.get('categories', []))} categories")
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse BOM JSON: {str(e)}")
                # Create fallback BOM structure
                bom_data = {
                    "project_name": project_name,
                    "error": "Failed to parse LLM response",
                    "raw_response": response[:500]
                }
            
            # Generate HTML version
            self.log_execution("start", "Generating HTML version")
            bom_html = self._generate_html(bom_data, project_name)
            self.log_execution("success", f"Generated HTML ({len(bom_html)} characters)")

            return AgentResult(
                success=True,
                data={
                    "bom_json": bom_data,
                    "bom_html": bom_html,
                    "project_name": project_name,
                    "total_components": len([item for cat in bom_data.get('categories', []) for item in cat.get('items', [])])
                },
                metadata={
                    "agent": self.config.name,
                    "format": "json+html"
                }
            )
            
        except Exception as e:
            self.log_execution("error", f"Failed to generate BOM: {str(e)}")
            return AgentResult(
                success=False,
                error=f"BOM generation failed: {str(e)}",
                metadata={"agent": self.config.name}
            )
    
    def _generate_html(self, bom_data: dict, project_name: str) -> str:
        """Generate comprehensive interactive HTML from BOM data with AICOE branding (UC001 style)"""
        # Convert BOM JSON to HTML tables
        html_content = self._bom_to_interactive_html(bom_data)

        # AICOE-branded HTML template with UC001 styling
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - Bill of Materials</title>
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

        .summary {{
            background: var(--bg-white);
            padding: 32px;
            border-radius: 24px;
            margin: 32px 0;
            box-shadow: var(--shadow);
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 24px;
        }}

        .summary-item {{
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.03) 0%, rgba(58, 42, 78, 0.05) 100%);
            padding: 24px;
            border-radius: 16px;
            text-align: center;
            border-left: 4px solid var(--accent-cyan);
        }}

        .summary-item h3 {{
            color: var(--text-secondary);
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }}

        .summary-item .value {{
            color: var(--primary-navy);
            font-size: 32px;
            font-weight: 700;
        }}

        .category {{
            background: var(--bg-white);
            border-radius: 24px;
            padding: 32px;
            margin: 24px 0;
            box-shadow: var(--shadow);
        }}

        .category h2 {{
            color: var(--primary-navy);
            font-size: 28px;
            margin-bottom: 16px;
            font-weight: 700;
        }}

        .category p {{
            color: var(--text-secondary);
            margin-bottom: 24px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: var(--bg-white);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow);
        }}

        th {{
            background: var(--primary-navy);
            color: white;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            user-select: none;
            position: relative;
        }}

        th:hover {{
            background: var(--midnight-blue);
        }}

        th.sortable::after {{
            content: ' ⇅';
            opacity: 0.5;
        }}

        th.sorted-asc::after {{
            content: ' ↑';
            opacity: 1;
        }}

        th.sorted-desc::after {{
            content: ' ↓';
            opacity: 1;
        }}

        td {{
            padding: 12px 15px;
            border-bottom: 1px solid var(--border-gray);
            color: var(--text-primary);
            font-size: 14px;
        }}

        tr:hover {{
            background: var(--bg-gray);
        }}

        .cost {{
            color: var(--accent-cyan);
            font-weight: 600;
        }}

        .notes {{
            background: linear-gradient(135deg, rgba(26, 26, 46, 0.03) 0%, rgba(58, 42, 78, 0.05) 100%);
            padding: 24px;
            border-radius: 16px;
            margin-top: 32px;
            border-left: 4px solid var(--accent-pink);
        }}

        .notes h3 {{
            color: var(--primary-navy);
            margin-bottom: 16px;
            font-weight: 600;
        }}

        .notes ul {{
            padding-left: 24px;
        }}

        .notes li {{
            margin: 8px 0;
            color: var(--text-primary);
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

            .category {{
                padding: 24px;
            }}

            .metadata {{
                gap: 20px;
            }}

            table {{
                font-size: 12px;
            }}

            th, td {{
                padding: 8px;
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

            .category {{
                break-inside: avoid;
                page-break-inside: avoid;
                box-shadow: none;
                border: 1px solid var(--border-gray);
                margin-bottom: 20px;
                padding: 24px;
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
                <h1>📊 Bill of Materials</h1>
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
                        <span class="metadata-label">Generated</span>
                        <span class="metadata-value">{self._get_current_date()}</span>
                    </div>
                </div>
            </div>
        </header>

        {html_content}

        <footer>
            <div class="footer-logo">AICOE</div>
            <p>© 2025 AICOE - AI Center of Excellence</p>
            <p style="margin-top: 8px;">Comprehensive Bill of Materials</p>
        </footer>
    </div>

    <script>
        // Table sorting functionality
        document.querySelectorAll('th.sortable').forEach(header => {{
            header.addEventListener('click', function() {{
                const table = this.closest('table');
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));
                const columnIndex = Array.from(this.parentElement.children).indexOf(this);
                const isAscending = this.classList.contains('sorted-asc');

                // Remove sorting classes from all headers in this table
                table.querySelectorAll('th').forEach(h => {{
                    h.classList.remove('sorted-asc', 'sorted-desc');
                }});

                // Add appropriate class to clicked header
                this.classList.add(isAscending ? 'sorted-desc' : 'sorted-asc');

                // Sort rows
                rows.sort((a, b) => {{
                    const aValue = a.cells[columnIndex].textContent.trim();
                    const bValue = b.cells[columnIndex].textContent.trim();

                    // Try to parse as number
                    const aNum = parseFloat(aValue.replace(/[^0-9.-]/g, ''));
                    const bNum = parseFloat(bValue.replace(/[^0-9.-]/g, ''));

                    if (!isNaN(aNum) && !isNaN(bNum)) {{
                        return isAscending ? bNum - aNum : aNum - bNum;
                    }}

                    return isAscending ?
                        bValue.localeCompare(aValue) :
                        aValue.localeCompare(bValue);
                }});

                // Reappend sorted rows
                rows.forEach(row => tbody.appendChild(row));
            }});
        }});

        // Search/filter functionality
        function filterTable(searchTerm) {{
            const tables = document.querySelectorAll('table');
            searchTerm = searchTerm.toLowerCase();

            tables.forEach(table => {{
                const rows = table.querySelectorAll('tbody tr');
                rows.forEach(row => {{
                    const text = row.textContent.toLowerCase();
                    row.style.display = text.includes(searchTerm) ? '' : 'none';
                }});
            }});
        }}

        // Add search input if controls exist
        const controls = document.querySelector('.controls');
        if (controls) {{
            const searchInput = controls.querySelector('input[type="text"]');
            if (searchInput) {{
                searchInput.addEventListener('input', (e) => filterTable(e.target.value));
            }}
        }}

        // Initialize Lucide icons
        lucide.createIcons();
    </script>
</body>
</html>
"""

        return html_template
    
    def _bom_to_interactive_html(self, bom_data: dict) -> str:
        """Convert BOM JSON to interactive HTML with search and filtering"""
        html = []

        # Summary section with cards
        summary = bom_data.get('summary', {})
        html.append('<div class="summary">')
        html.append('<div class="summary-item">')
        html.append('<h3>Total Components</h3>')
        html.append(f'<div class="value">{summary.get("total_components", 0)}</div>')
        html.append('</div>')
        html.append('<div class="summary-item">')
        html.append('<h3>One-Time Cost</h3>')
        html.append(f'<div class="value cost">${summary.get("total_one_time_cost", 0):,.2f}</div>')
        html.append('</div>')
        html.append('<div class="summary-item">')
        html.append('<h3>Monthly Recurring</h3>')
        html.append(f'<div class="value cost">${summary.get("total_recurring_cost_monthly", 0):,.2f}</div>')
        html.append('</div>')
        html.append('<div class="summary-item">')
        html.append('<h3>Annual Recurring</h3>')
        html.append(f'<div class="value cost">${summary.get("total_recurring_cost_annual", 0):,.2f}</div>')
        html.append('</div>')
        html.append('</div>')

        # Search and filter controls
        html.append('<div class="controls">')
        html.append('<input type="text" placeholder="🔍 Search items..." />')
        html.append('<button onclick="window.print()">🖨️ Print</button>')
        html.append('</div>')

        # Categories with sortable tables
        for category in bom_data.get('categories', []):
            html.append('<div class="category">')
            html.append(f'<h2>{category.get("category_name", "Unknown")}</h2>')
            html.append(f'<p>{category.get("description", "")}</p>')

            items = category.get('items', [])
            if items:
                html.append('<table>')
                html.append('<thead><tr>')
                html.append('<th class="sortable">ID</th>')
                html.append('<th class="sortable">Name</th>')
                html.append('<th class="sortable">Quantity</th>')
                html.append('<th>Specifications</th>')
                html.append('<th class="sortable">Vendor</th>')
                html.append('<th class="sortable">Cost Type</th>')
                html.append('<th class="sortable">Monthly Cost</th>')
                html.append('</tr></thead>')
                html.append('<tbody>')
                for item in items:
                    specs = item.get('specifications', {})
                    specs_str = ', '.join([f"{k}: {v}" for k, v in specs.items()]) if isinstance(specs, dict) else str(specs)
                    html.append('<tr>')
                    html.append(f'<td>{item.get("item_id", "")}</td>')
                    html.append(f'<td>{item.get("name", "")}</td>')
                    html.append(f'<td>{item.get("quantity", 0)} {item.get("unit", "")}</td>')
                    html.append(f'<td>{specs_str}</td>')
                    html.append(f'<td>{item.get("vendor", "TBD")}</td>')
                    html.append(f'<td>{item.get("cost_type", "")}</td>')
                    html.append(f'<td class="cost">${item.get("total_cost_monthly", 0):,.2f}</td>')
                    html.append('</tr>')
                html.append('</tbody>')
                html.append('</table>')
            html.append('</div>')

        # Notes
        notes = bom_data.get('notes', [])
        if notes:
            html.append('<div class="notes">')
            html.append('<h3>📝 Notes</h3>')
            html.append('<ul>')
            for note in notes:
                html.append(f'<li>{note}</li>')
            html.append('</ul>')
            html.append('</div>')

        return '\n'.join(html)
    
    def _get_current_date(self) -> str:
        """Get current date in readable format"""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")

