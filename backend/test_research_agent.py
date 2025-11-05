#!/usr/bin/env python3
"""
Test script for Research Agent with OpenAI gpt-4o-mini-search-preview
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append('.')

from agents.llm_client import LLMClient
from agents.research_agent import ResearchAgent

async def test_research_agent():
    try:
        print("🔍 Testing Research Agent with OpenAI gpt-4o-mini-search-preview...")
        
        # Initialize LLM client
        llm_client = LLMClient()
        
        # Initialize research agent
        research_agent = ResearchAgent(llm_client)
        
        # Test input data
        test_input = {
            'project_name': 'Test Insurance Portal',
            'structured_notes': {
                'company_name': 'Test Insurance Co',
                'project_overview': 'A comprehensive insurance customer portal'
            }
        }
        
        print(f"📋 Test Input:")
        print(f"   Project: {test_input['project_name']}")
        print(f"   Company: {test_input['structured_notes']['company_name']}")
        print(f"   Overview: {test_input['structured_notes']['project_overview']}")
        print()
        
        # Execute research agent
        result = await research_agent.execute(test_input, {})
        
        if result.success:
            print('✅ Research Agent test PASSED')
            research_insights = result.data.get("research_insights", {})
            print(f'📊 Research insights generated: {len(research_insights)} categories')
            print(f'🏢 Company: {result.data.get("company_name", "N/A")}')
            print(f'📱 Product Type: {result.data.get("product_type", "N/A")}')
            print(f'🔗 Sources found: {result.data.get("sources_count", 0)}')
            
            # Show some insights
            if research_insights:
                print(f"\n📈 Sample Insights:")
                for key, value in list(research_insights.items())[:3]:
                    if isinstance(value, list) and value:
                        print(f"   {key}: {value[0]}")
                    elif isinstance(value, str):
                        print(f"   {key}: {value[:100]}...")
        else:
            print('❌ Research Agent test FAILED')
            print(f'Error: {result.error}')
            
    except Exception as e:
        print(f'❌ Research Agent test FAILED with exception: {str(e)}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_research_agent())