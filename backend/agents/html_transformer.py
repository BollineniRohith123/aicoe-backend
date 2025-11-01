"""
AICOE HTML Generator - Creates beautiful, branded HTML from XML artifacts
"""
from typing import Dict, Any, Optional
import xml.etree.ElementTree as ET
import json
import logging
from datetime import datetime
import os
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from lxml import etree
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False
    logger.warning("lxml not available, XSLT transformation will not work")


class AICOEHTMLGenerator:
    """
    Generates beautiful, branded HTML documents from XML artifacts using AICOE design system.
    """

    def __init__(self):
        self.aicoe_colors = {
            'primary': '#2563eb',      # Blue-600
            'primary_dark': '#1d4ed8', # Blue-700
            'secondary': '#64748b',    # Slate-500
            'accent': '#06b6d4',       # Cyan-500
            'success': '#10b981',      # Emerald-500
            'warning': '#f59e0b',      # Amber-500
            'error': '#ef4444',        # Red-500
            'background': '#f8fafc',   # Slate-50
            'surface': '#ffffff',      # White
            'text': '#1e293b',         # Slate-800
            'text_light': '#64748b',   # Slate-500
            'border': '#e2e8f0',       # Slate-200
        }

    def generate_html_from_xml(self, xml_string: str, document_type: str, project_name: str = "Project") -> str:
        """
        Generate branded HTML from XML content.

        Args:
            xml_string: The XML content as string
            document_type: Type of document ('prd', 'proposal', 'architecture', 'bom', 'mockup')
            project_name: Name of the project

        Returns:
            Complete HTML document as string
        """
        try:
            # Parse XML
            root = ET.fromstring(xml_string)

            # Generate HTML based on document type
            if document_type == 'prd':
                html_content = self._generate_prd_html(root, project_name)
            elif document_type == 'proposal':
                html_content = self._generate_proposal_html(root, project_name)
            elif document_type == 'architecture':
                html_content = self._generate_architecture_html(root, project_name)
            elif document_type == 'bom':
                html_content = self._generate_bom_html(root, project_name)
            elif document_type == 'mockup':
                html_content = self._generate_mockup_html(root, project_name)
            else:
                html_content = self._generate_generic_html(root, project_name)

            # Wrap in full HTML document
            return self._wrap_in_html_template(html_content, project_name, document_type)

        except Exception as e:
            logger.error(f"Error generating HTML from XML: {str(e)}")
            return self._generate_error_html(str(e))

    def generate_html_from_xml_xslt(self, xml_string: str, document_type: str, project_name: str = "Project") -> str:
        """
        Generate HTML from XML using XSLT templates.

        Args:
            xml_string: The XML content as string
            document_type: Type of document ('prd', 'proposal', 'architecture', 'bom')
            project_name: Name of the project

        Returns:
            Complete HTML document as string
        """
        if not LXML_AVAILABLE:
            logger.error("lxml not available, falling back to programmatic HTML generation")
            return self.generate_html_from_xml(xml_string, document_type, project_name)

        try:
            # Get the XSLT template path
            template_dir = Path(__file__).parent / "templates"
            xslt_file = template_dir / f"{document_type}_template.xslt"

            if not xslt_file.exists():
                logger.error(f"XSLT template not found: {xslt_file}")
                return self.generate_html_from_xml(xml_string, document_type, project_name)

            # Parse XSLT
            xslt_doc = etree.parse(str(xslt_file))
            transform = etree.XSLT(xslt_doc)

            # Parse XML
            xml_doc = etree.fromstring(xml_string.encode('utf-8'))

            # Apply transformation
            result_tree = transform(xml_doc)
            html_content = str(result_tree)

            return html_content

        except Exception as e:
            logger.error(f"Error generating HTML from XML using XSLT: {str(e)}")
            # Fallback to programmatic generation
            return self.generate_html_from_xml(xml_string, document_type, project_name)

    def _generate_prd_html(self, root: ET.Element, project_name: str) -> str:
        """Generate PRD HTML content."""
        html_parts = []

        # Title
        title = root.find('title')
        if title is not None:
            html_parts.append(f'<h1 class="document-title">{title.text}</h1>')

        # Executive Summary
        exec_summary = root.find('executiveSummary')
        if exec_summary is not None:
            html_parts.append(f'''
            <div class="section">
                <h2 class="section-title">Executive Summary</h2>
                <div class="executive-summary">
                    <p>{exec_summary.text}</p>
                </div>
            </div>
            ''')

        # Scope
        scope = root.find('scope')
        if scope is not None:
            html_parts.append('<div class="section"><h2 class="section-title">Project Scope</h2>')

            in_scope = scope.find('inScope')
            if in_scope is not None:
                html_parts.append(f'<div class="scope-section"><h3>In Scope</h3><div class="scope-content">{in_scope.text}</div></div>')

            out_scope = scope.find('outOfScope')
            if out_scope is not None:
                html_parts.append(f'<div class="scope-section"><h3>Out of Scope</h3><div class="scope-content">{out_scope.text}</div></div>')

            html_parts.append('</div>')

        # Business Goals
        goals = root.find('businessGoals')
        if goals is not None:
            html_parts.append('<div class="section"><h2 class="section-title">Business Goals</h2><ul class="goals-list">')
            for goal in goals.findall('goal'):
                html_parts.append(f'<li>{goal.text}</li>')
            html_parts.append('</ul></div>')

        # Use Cases
        use_cases = root.find('useCases')
        if use_cases is not None:
            html_parts.append('<div class="section"><h2 class="section-title">Use Cases</h2>')
            html_parts.append(self._generate_use_cases_html(use_cases))
            html_parts.append('</div>')

        # Non-functional Requirements
        nfr = root.find('nonFunctionalRequirements')
        if nfr is not None:
            html_parts.append('<div class="section"><h2 class="section-title">Non-Functional Requirements</h2><div class="requirements-grid">')
            for req in nfr.findall('requirement'):
                req_type = req.get('type', 'General')
                html_parts.append(f'<div class="requirement-card"><div class="requirement-type">{req_type}</div><div class="requirement-text">{req.text}</div></div>')
            html_parts.append('</div></div>')

        return '\n'.join(html_parts)

    def _generate_use_cases_html(self, use_cases_element: ET.Element) -> str:
        """Generate HTML for use cases section."""
        html_parts = []

        for use_case in use_cases_element.findall('useCase'):
            uc_id = use_case.get('id', '')
            title = use_case.find('title')
            primary_actor = use_case.find('primaryActor')
            description = use_case.find('description')

            html_parts.append(f'<div class="use-case-card">')
            html_parts.append(f'<div class="use-case-header"><span class="use-case-id">{uc_id}</span><h3>{title.text if title is not None else "Use Case"}</h3></div>')

            if primary_actor is not None:
                html_parts.append(f'<div class="actor-info"><strong>Primary Actor:</strong> {primary_actor.text}</div>')

            if description is not None:
                html_parts.append(f'<div class="use-case-description">{description.text}</div>')

            # Main Flow
            main_flow = use_case.find('mainFlow')
            if main_flow is not None:
                html_parts.append('<div class="flow-section"><h4>Main Flow</h4><ol class="flow-steps">')
                for step in main_flow.findall('step'):
                    html_parts.append(f'<li>{step.text}</li>')
                html_parts.append('</ol></div>')

            # Alternative Flows
            alt_flows = use_case.find('alternativeFlows')
            if alt_flows is not None and alt_flows.findall('flow'):
                html_parts.append('<div class="flow-section"><h4>Alternative Flows</h4>')
                for flow in alt_flows.findall('flow'):
                    flow_id = flow.get('id', '')
                    trigger = flow.get('trigger', '')
                    html_parts.append(f'<div class="alt-flow"><div class="flow-trigger"><strong>{flow_id}:</strong> {trigger}</div><ol class="flow-steps">')
                    for step in flow.findall('step'):
                        html_parts.append(f'<li>{step.text}</li>')
                    html_parts.append('</ol></div>')
                html_parts.append('</div>')

            html_parts.append('</div>')

        return '\n'.join(html_parts)

    def _generate_proposal_html(self, root: ET.Element, project_name: str) -> str:
        """Generate proposal HTML content."""
        html_parts = []

        # Title
        title = root.find('title')
        if title is not None:
            html_parts.append(f'<h1 class="document-title">{title.text}</h1>')

        # Executive Summary
        exec_summary = root.find('executiveSummary')
        if exec_summary is not None:
            html_parts.append(f'''
            <div class="section">
                <h2 class="section-title">Executive Summary</h2>
                <div class="executive-summary">
                    <p>{exec_summary.text}</p>
                </div>
            </div>
            ''')

        # Solution Overview
        solution = root.find('solutionOverview')
        if solution is not None:
            html_parts.append(f'''
            <div class="section">
                <h2 class="section-title">Solution Overview</h2>
                <div class="solution-content">
                    {solution.text}
                </div>
            </div>
            ''')

        # Pricing
        pricing = root.find('pricing')
        if pricing is not None:
            html_parts.append('<div class="section"><h2 class="section-title">Pricing & Timeline</h2>')
            html_parts.append('<div class="pricing-grid">')

            for tier in pricing.findall('tier'):
                name = tier.find('name')
                price = tier.find('price')
                timeline = tier.find('timeline')
                features = tier.find('features')

                html_parts.append('<div class="pricing-card">')
                if name is not None:
                    html_parts.append(f'<div class="pricing-name">{name.text}</div>')
                if price is not None:
                    html_parts.append(f'<div class="pricing-price">{price.text}</div>')
                if timeline is not None:
                    html_parts.append(f'<div class="pricing-timeline">{timeline.text}</div>')
                if features is not None:
                    html_parts.append(f'<div class="pricing-features">{features.text}</div>')
                html_parts.append('</div>')

            html_parts.append('</div></div>')

        return '\n'.join(html_parts)

    def _generate_architecture_html(self, root: ET.Element, project_name: str) -> str:
        """Generate architecture HTML content."""
        html_parts = []

        # Title
        title = root.find('title')
        if title is not None:
            html_parts.append(f'<h1 class="document-title">{title.text}</h1>')

        # Overview
        overview = root.find('overview')
        if overview is not None:
            html_parts.append(f'''
            <div class="section">
                <h2 class="section-title">Architecture Overview</h2>
                <div class="architecture-overview">
                    <p>{overview.text}</p>
                </div>
            </div>
            ''')

        # Components
        components = root.find('components')
        if components is not None:
            html_parts.append('<div class="section"><h2 class="section-title">System Components</h2><div class="components-grid">')
            for component in components.findall('component'):
                name = component.find('name')
                description = component.find('description')
                tech = component.find('technology')

                html_parts.append('<div class="component-card">')
                if name is not None:
                    html_parts.append(f'<h3>{name.text}</h3>')
                if description is not None:
                    html_parts.append(f'<p>{description.text}</p>')
                if tech is not None:
                    html_parts.append(f'<div class="component-tech">Technology: {tech.text}</div>')
                html_parts.append('</div>')
            html_parts.append('</div></div>')

        # Diagrams
        diagrams = root.find('diagrams')
        if diagrams is not None:
            html_parts.append('<div class="section"><h2 class="section-title">Architecture Diagrams</h2>')
            for diagram in diagrams.findall('diagram'):
                title = diagram.find('title')
                mermaid = diagram.find('mermaidCode')

                if title is not None and mermaid is not None:
                    html_parts.append(f'<div class="diagram-section"><h3>{title.text}</h3><div class="mermaid-diagram">{mermaid.text}</div></div>')
            html_parts.append('</div>')

        return '\n'.join(html_parts)

    def _generate_bom_html(self, root: ET.Element, project_name: str) -> str:
        """Generate BOM HTML content."""
        html_parts = []

        # Title
        title = root.find('title')
        if title is not None:
            html_parts.append(f'<h1 class="document-title">{title.text}</h1>')

        # Summary
        summary = root.find('summary')
        if summary is not None:
            html_parts.append(f'''
            <div class="section">
                <h2 class="section-title">BOM Summary</h2>
                <div class="bom-summary">
                    <p>{summary.text}</p>
                </div>
            </div>
            ''')

        # Components
        components = root.find('components')
        if components is not None:
            html_parts.append('<div class="section"><h2 class="section-title">Components & Materials</h2>')
            html_parts.append('<div class="bom-table-container"><table class="bom-table">')
            html_parts.append('<thead><tr><th>Component</th><th>Description</th><th>Quantity</th><th>Unit Cost</th><th>Total Cost</th><th>Supplier</th></tr></thead><tbody>')

            for component in components.findall('component'):
                name = component.find('name')
                desc = component.find('description')
                qty = component.find('quantity')
                cost = component.find('unitCost')
                total = component.find('totalCost')
                supplier = component.find('supplier')

                html_parts.append('<tr>')
                html_parts.append(f'<td>{name.text if name is not None else ""}</td>')
                html_parts.append(f'<td>{desc.text if desc is not None else ""}</td>')
                html_parts.append(f'<td>{qty.text if qty is not None else ""}</td>')
                html_parts.append(f'<td>${cost.text if cost is not None else ""}</td>')
                html_parts.append(f'<td>${total.text if total is not None else ""}</td>')
                html_parts.append(f'<td>{supplier.text if supplier is not None else ""}</td>')
                html_parts.append('</tr>')

            html_parts.append('</tbody></table></div></div>')

        # Total Cost
        total_cost = root.find('totalCost')
        if total_cost is not None:
            html_parts.append(f'''
            <div class="section">
                <h2 class="section-title">Total Cost Summary</h2>
                <div class="total-cost">
                    <div class="cost-breakdown">{total_cost.text}</div>
                </div>
            </div>
            ''')

        return '\n'.join(html_parts)

    def _generate_mockup_html(self, root: ET.Element, project_name: str) -> str:
        """Generate mockup HTML content."""
        html_parts = []

        # Title
        title = root.find('title')
        if title is not None:
            html_parts.append(f'<h1 class="document-title">{title.text}</h1>')

        # Pages
        pages = root.find('pages')
        if pages is not None:
            html_parts.append('<div class="section"><h2 class="section-title">Application Mockups</h2>')
            for page in pages.findall('page'):
                page_title = page.find('title')
                html_code = page.find('htmlCode')

                if page_title is not None and html_code is not None:
                    html_parts.append(f'<div class="mockup-page"><h3>{page_title.text}</h3><div class="mockup-preview">{html_code.text}</div></div>')
            html_parts.append('</div>')

        return '\n'.join(html_parts)

    def _generate_generic_html(self, root: ET.Element, project_name: str) -> str:
        """Generate generic HTML for unknown document types."""
        html_parts = []

        # Generic title
        html_parts.append(f'<h1 class="document-title">{project_name} Document</h1>')

        # Convert XML to basic HTML structure
        html_parts.append('<div class="section"><div class="generic-content">')
        html_parts.append(self._xml_to_basic_html(root))
        html_parts.append('</div></div>')

        return '\n'.join(html_parts)

    def _xml_to_basic_html(self, element: ET.Element, level: int = 0) -> str:
        """Convert XML element to basic HTML recursively."""
        html_parts = []

        tag_name = element.tag
        if level == 0:
            html_parts.append(f'<div class="xml-root">')
        else:
            html_parts.append(f'<div class="xml-element" style="margin-left: {level * 20}px;"><strong>{tag_name}:</strong> ')

        if element.text and element.text.strip():
            html_parts.append(f'<span class="xml-text">{element.text.strip()}</span>')

        for child in element:
            html_parts.append(self._xml_to_basic_html(child, level + 1))

        html_parts.append('</div>')

        return '\n'.join(html_parts)

    def _wrap_in_html_template(self, content: str, project_name: str, document_type: str) -> str:
        """Wrap content in complete HTML document with AICOE branding."""
        css_styles = self._generate_css_styles()
        js_scripts = self._generate_js_scripts()

        html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - {document_type.upper()}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lucide-static@0.321.0/font/lucide.css">
    <style>
        {css_styles}
    </style>
</head>
<body>
    <div class="document-container">
        <header class="document-header">
            <div class="header-content">
                <div class="logo-section">
                    <div class="aicoe-logo">
                        <div class="logo-icon">AI</div>
                        <div class="logo-text">AICOE</div>
                    </div>
                    <div class="logo-subtitle">AI Center of Excellence</div>
                </div>
                <div class="header-info">
                    <h1 class="project-title">{project_name}</h1>
                    <div class="document-type">{document_type.upper()} Document</div>
                    <div class="generation-date">Generated: {datetime.now().strftime('%B %d, %Y')}</div>
                </div>
            </div>
        </header>

        <main class="document-content">
            {content}
        </main>

        <footer class="document-footer">
            <div class="footer-content">
                <div class="logo-section">
                    <div class="logo-icon">AI</div>
                    <div class="logo-text">AICOE</div>
                </div>
                <div class="footer-text">
                    <p>© 2025 AICOE - AI Center of Excellence</p>
                    <p>Transforming Ideas into Intelligent Solutions</p>
                </div>
            </div>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <script>
        {js_scripts}
    </script>
</body>
</html>'''

        return html_template

    def _generate_css_styles(self) -> str:
        """Generate comprehensive CSS styles for AICOE branding."""
        colors = self.aicoe_colors

        return f'''
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: {colors['text']};
            background-color: {colors['background']};
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        .document-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: {colors['surface']};
            box-shadow: 0 0 50px rgba(0,0,0,0.1);
            min-height: 100vh;
        }}

        .document-header {{
            background: linear-gradient(135deg, {colors['primary']}, {colors['primary_dark']});
            color: white;
            padding: 40px 30px;
            position: relative;
            overflow: hidden;
        }}

        .document-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.05"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.1;
        }}

        .header-content {{
            position: relative;
            z-index: 1;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 30px;
        }}

        .logo-section {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .aicoe-logo {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }}

        .logo-icon {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, {colors['accent']}, {colors['primary']});
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 18px;
            color: white;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3);
        }}

        .logo-text {{
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}

        .logo-subtitle {{
            font-size: 12px;
            opacity: 0.9;
            font-weight: 500;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .header-info {{
            text-align: right;
        }}

        .project-title {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            line-height: 1.2;
        }}

        .document-type {{
            font-size: 14px;
            opacity: 0.9;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }}

        .generation-date {{
            font-size: 12px;
            opacity: 0.8;
        }}

        .document-content {{
            padding: 50px 30px;
        }}

        .document-title {{
            font-size: 36px;
            font-weight: 700;
            color: {colors['primary']};
            margin-bottom: 40px;
            text-align: center;
            line-height: 1.2;
        }}

        .section {{
            margin-bottom: 50px;
            background: {colors['surface']};
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            border: 1px solid {colors['border']};
        }}

        .section-title {{
            font-size: 24px;
            font-weight: 600;
            color: {colors['primary']};
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid {colors['primary']};
            display: inline-block;
        }}

        .executive-summary {{
            font-size: 18px;
            line-height: 1.7;
            color: {colors['text']};
        }}

        .scope-section {{
            margin-bottom: 30px;
        }}

        .scope-section h3 {{
            font-size: 18px;
            font-weight: 600;
            color: {colors['text']};
            margin-bottom: 15px;
        }}

        .scope-content {{
            background: {colors['background']};
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid {colors['primary']};
        }}

        .goals-list {{
            list-style: none;
            padding: 0;
        }}

        .goals-list li {{
            padding: 15px 0;
            border-bottom: 1px solid {colors['border']};
            position: relative;
            padding-left: 30px;
        }}

        .goals-list li::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: {colors['success']};
            font-weight: bold;
            font-size: 16px;
        }}

        .use-case-card {{
            background: {colors['background']};
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid {colors['border']};
            transition: all 0.3s ease;
        }}

        .use-case-card:hover {{
            box-shadow: 0 8px 30px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}

        .use-case-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }}

        .use-case-id {{
            background: {colors['primary']};
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .use-case-header h3 {{
            font-size: 20px;
            font-weight: 600;
            color: {colors['text']};
            margin: 0;
        }}

        .actor-info {{
            background: {colors['primary']};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-weight: 500;
        }}

        .use-case-description {{
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 25px;
            color: {colors['text_light']};
        }}

        .flow-section {{
            margin-bottom: 25px;
        }}

        .flow-section h4 {{
            font-size: 16px;
            font-weight: 600;
            color: {colors['text']};
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .flow-steps {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid {colors['border']};
        }}

        .flow-steps li {{
            margin-bottom: 10px;
            padding-left: 10px;
            position: relative;
        }}

        .flow-steps li::before {{
            content: '';
            position: absolute;
            left: -15px;
            top: 8px;
            width: 6px;
            height: 6px;
            background: {colors['primary']};
            border-radius: 50%;
        }}

        .alt-flow {{
            background: {colors['background']};
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            border: 1px solid {colors['border']};
        }}

        .flow-trigger {{
            font-weight: 600;
            color: {colors['warning']};
            margin-bottom: 15px;
        }}

        .requirements-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}

        .requirement-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            border: 1px solid {colors['border']};
            transition: all 0.3s ease;
        }}

        .requirement-card:hover {{
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}

        .requirement-type {{
            background: {colors['primary']};
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 15px;
        }}

        .requirement-text {{
            font-size: 16px;
            line-height: 1.6;
            color: {colors['text']};
        }}

        .solution-content {{
            font-size: 16px;
            line-height: 1.7;
            color: {colors['text']};
        }}

        .pricing-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}

        .pricing-card {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            border: 2px solid {colors['border']};
            transition: all 0.3s ease;
            text-align: center;
        }}

        .pricing-card:hover {{
            border-color: {colors['primary']};
            box-shadow: 0 8px 30px rgba(37, 99, 235, 0.1);
        }}

        .pricing-name {{
            font-size: 20px;
            font-weight: 600;
            color: {colors['text']};
            margin-bottom: 15px;
        }}

        .pricing-price {{
            font-size: 32px;
            font-weight: 700;
            color: {colors['primary']};
            margin-bottom: 10px;
        }}

        .pricing-timeline {{
            font-size: 14px;
            color: {colors['text_light']};
            margin-bottom: 20px;
        }}

        .pricing-features {{
            font-size: 14px;
            color: {colors['text']};
            line-height: 1.6;
        }}

        .components-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}

        .component-card {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            border: 1px solid {colors['border']};
            transition: all 0.3s ease;
        }}

        .component-card:hover {{
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}

        .component-card h3 {{
            font-size: 18px;
            font-weight: 600;
            color: {colors['text']};
            margin-bottom: 15px;
        }}

        .component-card p {{
            color: {colors['text_light']};
            line-height: 1.6;
            margin-bottom: 15px;
        }}

        .component-tech {{
            font-size: 12px;
            color: {colors['primary']};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .diagram-section {{
            margin-bottom: 40px;
        }}

        .diagram-section h3 {{
            font-size: 18px;
            font-weight: 600;
            color: {colors['text']};
            margin-bottom: 20px;
        }}

        .mermaid-diagram {{
            background: {colors['background']};
            border-radius: 8px;
            padding: 20px;
            border: 1px solid {colors['border']};
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            line-height: 1.4;
        }}

        .bom-table-container {{
            overflow-x: auto;
            background: white;
            border-radius: 12px;
            border: 1px solid {colors['border']};
        }}

        .bom-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .bom-table th {{
            background: {colors['primary']};
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .bom-table td {{
            padding: 15px;
            border-bottom: 1px solid {colors['border']};
            font-size: 14px;
        }}

        .bom-table tr:hover {{
            background: {colors['background']};
        }}

        .total-cost {{
            background: {colors['primary']};
            color: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
        }}

        .cost-breakdown {{
            font-size: 18px;
            font-weight: 600;
        }}

        .mockup-page {{
            margin-bottom: 40px;
        }}

        .mockup-page h3 {{
            font-size: 20px;
            font-weight: 600;
            color: {colors['text']};
            margin-bottom: 20px;
        }}

        .mockup-preview {{
            background: {colors['background']};
            border-radius: 8px;
            padding: 20px;
            border: 1px solid {colors['border']};
            overflow-x: auto;
        }}

        .document-footer {{
            background: {colors['background']};
            border-top: 1px solid {colors['border']};
            padding: 30px;
            margin-top: 50px;
        }}

        .footer-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
        }}

        .footer-logo {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .footer-logo .logo-icon {{
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, {colors['accent']}, {colors['primary']});
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
            color: white;
        }}

        .footer-logo .logo-text {{
            font-size: 18px;
            font-weight: 700;
            color: {colors['text']};
        }}

        .footer-text {{
            text-align: right;
            font-size: 12px;
            color: {colors['text_light']};
        }}

        .footer-text p {{
            margin-bottom: 5px;
        }}

        @media (max-width: 768px) {{
            .header-content {{
                flex-direction: column;
                text-align: center;
            }}

            .header-info {{
                text-align: center;
            }}

            .document-content {{
                padding: 30px 20px;
            }}

            .section {{
                padding: 25px 20px;
            }}

            .footer-content {{
                flex-direction: column;
                text-align: center;
            }}

            .footer-text {{
                text-align: center;
            }}
        }}

        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .section {{
            animation: fadeIn 0.6s ease-out;
        }}
        '''

    def _generate_js_scripts(self) -> str:
        """Generate JavaScript for interactive features."""
        return '''
        // Initialize Mermaid diagrams
        if (typeof mermaid !== 'undefined') {{
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'default',
                securityLevel: 'loose',
                fontFamily: 'Inter',
                fontSize: 14
            }});
        }}

        // Add smooth scrolling and animations
        document.addEventListener('DOMContentLoaded', function() {{
            // Animate sections on scroll
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }};

            const observer = new IntersectionObserver(function(entries) {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }}
                }});
            }}, observerOptions);

            // Initially hide sections
            document.querySelectorAll('.section').forEach(section => {{
                section.style.opacity = '0';
                section.style.transform = 'translateY(20px)';
                section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(section);
            });

            // Add click handlers for interactive elements
            document.querySelectorAll('.use-case-card').forEach(card => {{
                card.addEventListener('click', function() {{
                    this.classList.toggle('expanded');
                }});
            });

            // Add print functionality
            const printBtn = document.querySelector('.print-btn');
            if (printBtn) {{
                printBtn.addEventListener('click', function() {{
                    window.print();
                }});
            }}
        }});

        // Utility functions
        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(function() {{
                showNotification('Copied to clipboard!', 'success');
            }});
        }}

        function showNotification(message, type) {{
            const notification = document.createElement('div');
            notification.className = `notification notification-${{type}}`;
            notification.textContent = message;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: ${{type === 'success' ? '#10b981' : '#ef4444'}};
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 1000;
                animation: slideIn 0.3s ease;
            `;
            document.body.appendChild(notification);

            setTimeout(() => {{
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }}
        '''

    def _generate_error_html(self, error_message: str) -> str:
        """Generate error HTML page."""
        colors = self.aicoe_colors

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Generation Error</title>
    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: {colors['background']};
            color: {colors['text']};
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            margin: 0;
        }}
        .error-container {{
            background: {colors['surface']};
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
        }}
        .error-icon {{
            width: 80px;
            height: 80px;
            background: {colors['error']};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 32px;
            color: white;
        }}
        .error-title {{
            font-size: 24px;
            font-weight: 600;
            color: {colors['error']};
            margin-bottom: 15px;
        }}
        .error-message {{
            color: {colors['text_light']};
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">⚠️</div>
        <h1 class="error-title">Generation Error</h1>
        <p class="error-message">{error_message}</p>
    </div>
</body>
</html>'''


# Convenience function for direct use
def generate_html_from_xml(xml_string: str, document_type: str, project_name: str = "Project") -> str:
    """
    Convenience function to generate HTML from XML.

    Args:
        xml_string: The XML content as string
        document_type: Type of document ('prd', 'proposal', 'architecture', 'bom', 'mockup')
        project_name: Name of the project

    Returns:
        Complete HTML document as string
    """
    generator = AICOEHTMLGenerator()
    return generator.generate_html_from_xml(xml_string, document_type, project_name)