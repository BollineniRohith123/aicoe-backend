#!/usr/bin/env python3
"""
Test script for Synthetic LLM Client with Intake Agent
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append('.')

from agents.llm_client_synthetic import SyntheticLLMClient
from agents.intake_agent import IntakeAgent

async def test_synthetic_intake():
    try:
        print("🔍 Testing Synthetic LLM Client with Intake Agent...")
        
        # Initialize synthetic LLM client
        synthetic_client = SyntheticLLMClient()
        
        # Initialize intake agent with synthetic client
        intake_agent = IntakeAgent(synthetic_client)
        
        # Test input data
        test_transcript = """
        Meeting: Insurance Customer Portal Development
        Date: November 4, 2025
        
        Participants: Product Manager, Technical Lead, Business Analyst
        
        Discussion:
        We need to build a comprehensive insurance customer portal that allows customers to:
        1. View their policy details
        2. Submit claims
        3. Make payments
        4. Track claim status
        5. Download documents
        
        Technical requirements:
        - Web-based application
        - Mobile responsive
        - Secure authentication
        - Integration with existing insurance systems
        - Real-time notifications
        
        Timeline: 6 months
        Budget: $500,000
        """
        
        test_input = {
            'project_name': 'Insurance Customer Portal - Synthetic Test',
            'transcript': test_transcript
        }
        
        print(f"📋 Test Input:")
        print(f"   Transcript length: {len(test_transcript)} characters")
        print()
        
        # Execute intake agent
        result = await intake_agent.execute(test_input, {})
        
        if result.success:
            print('✅ Synthetic Intake Agent test PASSED')
            structured_notes = result.data.get("structured_notes", {})
            print(f'📊 Structured notes generated: {len(structured_notes)} fields')
            print(f'📄 Notes XML length: {len(result.data.get("notes_xml", ""))} characters')
            
            # Show some sample data
            if structured_notes:
                print(f"\n📈 Sample Structured Notes:")
                for key, value in list(structured_notes.items())[:3]:
                    if isinstance(value, list) and value:
                        print(f"   {key}: {value[0] if len(str(value[0])) < 50 else str(value[0])[:50] + '...'}")
                    elif isinstance(value, str):
                        print(f"   {key}: {value[:50] if len(value) > 50 else value}")
        else:
            print('❌ Synthetic Intake Agent test FAILED')
            print(f'Error: {result.error}')
            
    except Exception as e:
        print(f'❌ Synthetic Intake Agent test FAILED with exception: {str(e)}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_synthetic_intake())