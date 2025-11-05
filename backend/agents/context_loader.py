"""
Context Loader for AICoE Agent System
Loads rule markdown files and design system files as context for agents
"""

import os
import json
from typing import Dict, List, Any
from pathlib import Path

class ContextLoader:
    """Loads and manages context files for AICoE agents"""
    
    def __init__(self, base_path: str = None):
        self.base_path = base_path or "/Users/rohithbollineni/Downloads/AICOE/AICOE-Main/backend"
        self.rules_path = os.path.join(self.base_path, "Rules to write the documents")
        self.design_system_path = os.path.join(self.base_path, "Design System")
        
    def load_rule_document(self, rule_name: str) -> str:
        """Load a specific rule document by name"""
        rule_files = {
            "use_case": "01-guide-use-case-writing.md",
            "prd": "02-guide-prd-writing.md", 
            "bom": "02-guide-bom-creation.md",
            "data_generic": "03-guide-data-structure-generic.md",
            "data_jde": "04-guide-data-structure-jd-edwards.md",
            "business_requirements": "05-guide-business-requirements.md",
            "functional_requirements": "06-guide-functional-requirements.md",
            "test_cases": "07-guide-test-cases.md",
            "ai_architecture": "08-guide-ai-architecture-diagram.md"
        }
        
        if rule_name not in rule_files:
            raise ValueError(f"Unknown rule: {rule_name}. Available: {list(rule_files.keys())}")
            
        file_path = os.path.join(self.rules_path, rule_files[rule_name])
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Rule file not found: {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_design_system_files(self) -> Dict[str, str]:
        """Load all design system files"""
        design_files = {}
        
        # Load CSS file
        css_path = os.path.join(self.design_system_path, "06-reference-aicoe-design-system.css")
        if os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                design_files['css'] = f.read()
        
        # Load HTML guidelines
        html_guidelines_path = os.path.join(self.design_system_path, "05-reference-ui-design-guidelines.html")
        if os.path.exists(html_guidelines_path):
            with open(html_guidelines_path, 'r', encoding='utf-8') as f:
                design_files['html_guidelines'] = f.read()
                
        # Load mobile guidelines
        mobile_guidelines_path = os.path.join(self.design_system_path, "09-reference-mobile-app-guidelines.html")
        if os.path.exists(mobile_guidelines_path):
            with open(mobile_guidelines_path, 'r', encoding='utf-8') as f:
                design_files['mobile_guidelines'] = f.read()
        
        return design_files
    
    def get_agent_context(self, agent_type: str) -> Dict[str, Any]:
        """Get complete context for a specific agent type"""
        context = {
            "agent_type": agent_type,
            "rule_documents": {},
            "design_system": {},
            "aicoe_standards": self._get_aicoe_standards()
        }
        
        # Map agents to their required rule documents
        agent_rules = {
            "intake": ["use_case"],
            "use_case": ["use_case"],
            "brd": ["business_requirements", "use_case"],
            "fr": ["functional_requirements", "business_requirements"],
            "prd": ["prd", "use_case", "functional_requirements"],
            "mockup": ["prd", "ai_architecture"],  # HTML generation agent
            "architecture": ["ai_architecture", "prd"],  # HTML generation agent
            "bom": ["bom", "ai_architecture"],  # HTML generation agent
            "tc": ["test_cases", "functional_requirements"],
            "proposal": ["prd", "bom", "ai_architecture"],  # HTML generation agent
            "data": ["data_generic", "data_jde"],
            "storage": ["prd", "bom"]
        }
        
        # Load required rule documents
        if agent_type in agent_rules:
            for rule_name in agent_rules[agent_type]:
                try:
                    context["rule_documents"][rule_name] = self.load_rule_document(rule_name)
                except Exception as e:
                    print(f"Warning: Could not load rule {rule_name}: {e}")
        
        # Load design system files
        context["design_system"] = self.load_design_system_files()
        
        return context
    
    def _get_aicoe_standards(self) -> Dict[str, Any]:
        """Get AICoE branding and design standards"""
        return {
            "brand_name": "AICoE",
            "website": "aicoe.io",
            "design_principles": {
                "theme": "light_theme_only",
                "approach": "minimalistic_design",
                "icons": "lucide_icons_exclusively",
                "accessibility": "WCAG_2_1_AA",
                "colors": {
                    "background_primary": "#FFFFFF",
                    "background_secondary": "#F9FAFB", 
                    "text_primary": "#111827",
                    "text_secondary": "#4B5563",
                    "primary": "#2563EB",
                    "border": "#E5E7EB"
                }
            },
            "document_standards": {
                "format": "XML/HTML for structured docs",
                "language": "qualitative_over_quantitative",
                "focus": "business_value_over_technical_details",
                "traceability": "BR_to_FR_to_TC_mapping"
            }
        }
    
    def format_context_for_agent(self, agent_type: str) -> str:
        """Format context as a string for agent consumption"""
        context = self.get_agent_context(agent_type)
        
        formatted = f"""
# AICoE Agent Context for {agent_type.upper()} Agent

## AICoE Standards and Branding
- Organization: {context['aicoe_standards']['brand_name']} ({context['aicoe_standards']['website']})
- Design Theme: {context['aicoe_standards']['design_principles']['theme']}
- Design Approach: {context['aicoe_standards']['design_principles']['approach']}
- Icon Library: {context['aicoe_standards']['design_principles']['icons']}
- Accessibility: {context['aicoe_standards']['design_principles']['accessibility']}

## Rule Documents Context
"""
        
        for rule_name, content in context["rule_documents"].items():
            formatted += f"""
### {rule_name.replace('_', ' ').title()} Guide
```
{content[:2000]}{'...' if len(content) > 2000 else ''}
```

"""
        
        if context["design_system"]:
            formatted += """
## Design System Context
"""
            for file_type, content in context["design_system"].items():
                formatted += f"""
### {file_type.replace('_', ' ').title()}
```
{content[:1000]}{'...' if len(content) > 1000 else ''}
```

"""
        
        formatted += """
## Key AICoE Principles for All Outputs
1. Light theme only - no dark mode support
2. Minimalistic design - content over decoration
3. Lucide icons exclusively - no custom icons
4. Business value focus over technical details
5. Qualitative language over quantitative metrics
6. XML/HTML structured format for documents
7. WCAG 2.1 AA accessibility compliance
8. Professional presentation for stakeholders

## HTML and Mockup Generation Requirements
For agents generating HTML content and mockups:
- MUST follow AICoE design system guidelines exactly
- Use light theme colors: #FFFFFF background, #F9FAFB secondary
- Text colors: #111827 primary, #4B5563 secondary, #6B7280 tertiary
- Primary brand color: #2563EB for interactive elements
- Border color: #E5E7EB for dividers and cards
- Use Inter font family with proper fallbacks
- Implement responsive design (mobile, tablet, desktop)
- Include proper semantic HTML structure
- Apply WCAG 2.1 AA accessibility standards
- Use Lucide icons exclusively (no custom icons or emojis)
- Follow minimalistic design principles
- Ensure professional stakeholder presentation

Generate outputs following these AICoE standards and the rule document guidelines provided above.
"""
        
        return formatted

# Global context loader instance
context_loader = ContextLoader()

def get_agent_context(agent_type: str) -> str:
    """Get formatted context for an agent"""
    return context_loader.format_context_for_agent(agent_type)

def load_specific_rule(rule_name: str) -> str:
    """Load a specific rule document"""
    return context_loader.load_rule_document(rule_name)

if __name__ == "__main__":
    # Test the context loader
    print("Testing Context Loader...")
    
    # Test loading specific rules
    try:
        use_case_rule = load_specific_rule("use_case")
        print(f"✓ Use Case rule loaded: {len(use_case_rule)} characters")
    except Exception as e:
        print(f"✗ Error loading use case rule: {e}")
    
    # Test agent context
    try:
        brd_context = get_agent_context("brd")
        print(f"✓ BRD agent context generated: {len(brd_context)} characters")
    except Exception as e:
        print(f"✗ Error generating BRD context: {e}")
    
    # Test design system loading
    try:
        design_files = context_loader.load_design_system_files()
        print(f"✓ Design system files loaded: {len(design_files)} files")
    except Exception as e:
        print(f"✗ Error loading design system: {e}")