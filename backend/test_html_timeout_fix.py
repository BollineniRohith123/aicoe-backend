#!/usr/bin/env python3
"""
Test script to verify HTML generation timeout fix
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.brd_agent import BRDAgent
from agents.fr_agent import FRAgent
from agents.llm_client_synthetic import SyntheticLLMClient

async def test_html_generation_fix():
    """Test that HTML generation no longer times out"""
    
    print("🚀 Testing HTML generation timeout fix...")
    
    # Initialize synthetic LLM client
    llm_client = SyntheticLLMClient()
    
    # Test BRD Agent
    print("\n📄 Testing BRD Agent HTML generation...")
    brd_agent = BRDAgent(llm_client)
    
    # Sample input data
    test_input = {
        "project_name": "Test Project",
        "structured_notes": {
            "project_name": "Test Project",
            "requirements": ["Build a web app", "User authentication"],
            "decisions_made": ["Use React for frontend", "Use Node.js for backend"]
        },
        "use_cases": [
            {
                "id": "UC-001",
                "title": "User Login",
                "description": "User can log into the system"
            }
        ],
        "research_insights": {
            "industry_trends": ["AI integration", "Cloud-first approach"],
            "technical_standards": ["REST APIs", "OAuth 2.0"]
        }
    }
    
    try:
        # Test BRD HTML generation with timeout protection
        result = await asyncio.wait_for(
            brd_agent.execute(test_input, {}),
            timeout=300  # 5 minutes max
        )
        
        if result.success:
            brd_html = result.data.get("brd_html", "")
            print(f"✅ BRD HTML generated successfully: {len(brd_html)} characters")
            
            # Check if HTML is complete (has closing tags)
            if brd_html.endswith("</html>") or brd_html.endswith("</body>"):
                print("✅ BRD HTML appears complete (has closing tags)")
            else:
                print("⚠️  BRD HTML may be incomplete (missing closing tags)")
                
        else:
            print(f"❌ BRD Agent failed: {result.error}")
            
    except asyncio.TimeoutError:
        print("❌ BRD Agent timed out - fix may not be working")
    except Exception as e:
        print(f"❌ BRD Agent error: {str(e)}")
    
    # Test FR Agent
    print("\n📄 Testing FR Agent HTML generation...")
    fr_agent = FRAgent(llm_client)
    
    test_input_fr = {
        "project_name": "Test Project",
        "structured_notes": test_input["structured_notes"],
        "use_cases": test_input["use_cases"],
        "business_requirements": {
            "objectives": "Build a functional web application"
        }
    }
    
    try:
        # Test FR HTML generation with timeout protection
        result = await asyncio.wait_for(
            fr_agent.execute(test_input_fr, {}),
            timeout=300  # 5 minutes max
        )
        
        if result.success:
            fr_html = result.data.get("fr_html", "")
            print(f"✅ FR HTML generated successfully: {len(fr_html)} characters")
            
            # Check if HTML is complete (has closing tags)
            if fr_html.endswith("</html>") or fr_html.endswith("</body>"):
                print("✅ FR HTML appears complete (has closing tags)")
            else:
                print("⚠️  FR HTML may be incomplete (missing closing tags)")
                
        else:
            print(f"❌ FR Agent failed: {result.error}")
            
    except asyncio.TimeoutError:
        print("❌ FR Agent timed out - fix may not be working")
    except Exception as e:
        print(f"❌ FR Agent error: {str(e)}")
    
    print("\n🎯 HTML generation timeout fix test completed!")

if __name__ == "__main__":
    asyncio.run(test_html_generation_fix())