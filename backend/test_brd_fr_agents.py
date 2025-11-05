#!/usr/bin/env python3
"""
Test script to verify BRD and FR agents with two-stage process
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

async def test_agents():
    """Test BRD and FR agents with new architecture"""
    
    print("🔍 Testing BRD and FR Agents with Two-Stage Process...")
    
    # Initialize synthetic LLM client
    llm_client = SyntheticLLMClient()
    print("✅ Using Synthetic LLM Client")
    
    # Initialize agents
    brd_agent = BRDAgent(llm_client)
    fr_agent = FRAgent(llm_client)
    print("✅ Initialized BRD and FR Agents")
    
    # Test data
    test_input = {
        "project_name": "Test Project",
        "structured_notes": {
            "project_overview": "A test project for verification",
            "stakeholders": ["Project Manager", "Business Analyst"],
            "requirements": ["User authentication", "Data management"]
        },
        "use_cases": [
            {
                "id": "UC-001",
                "name": "Test Use Case",
                "description": "A test use case for verification",
                "steps": ["Step 1", "Step 2", "Step 3"]
            }
        ],
        "business_requirements": {
            "business_objectives": ["Improve efficiency", "Reduce costs"],
            "stakeholder_analysis": [{"role": "Manager", "responsibility": "Oversight"}]
        },
        "research_insights": {
            "industry_trends": "Modern web applications",
            "best_practices": "User-centered design"
        }
    }
    
    test_context = {"project_name": "Test Project"}
    
    try:
        print("📝 Testing BRD agent execution...")
        brd_result = await brd_agent.execute(test_input, test_context)
        
        if brd_result.success:
            print("✅ BRD agent execution successful!")
            print(f"📊 BRD XML length: {len(brd_result.data.get('brd_xml', ''))} characters")
            print(f"📊 BRD HTML length: {len(brd_result.data.get('brd_html', ''))} characters")
        else:
            print(f"❌ BRD agent execution failed: {brd_result.error}")
            
        print("\n📝 Testing FR agent execution...")
        fr_result = await fr_agent.execute(test_input, test_context)
        
        if fr_result.success:
            print("✅ FR agent execution successful!")
            print(f"📊 FR XML length: {len(fr_result.data.get('fr_xml', ''))} characters")
            print(f"📊 FR HTML length: {len(fr_result.data.get('fr_html', ''))} characters")
        else:
            print(f"❌ FR agent execution failed: {fr_result.error}")
            
        return brd_result.success and fr_result.success
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agents())
    if success:
        print("\n🎉 All agent tests passed! Two-stage process is working.")
    else:
        print("\n💥 Agent tests failed! Check the errors above.")