#!/usr/bin/env python3
"""
Simple Workflow Test - Test basic agent execution without timeouts
"""

import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add agents to path
sys.path.append('agents')

from agents.orchestrator import OrchestratorAgent
from agents.llm_client_synthetic import SyntheticLLMClient

async def test_simple_workflow():
    """Test a simple workflow with minimal agents"""
    print("🚀 Starting Simple Workflow Test")
    
    # Initialize with shorter timeout
    llm_client = SyntheticLLMClient()
    orchestrator = OrchestratorAgent(llm_client)
    
    project_name = f"Simple Test {datetime.now().strftime('%Y%m%d_%H%M%S')}"
    transcript = "Build a simple task management app with user login and basic CRUD operations."
    
    print(f"📋 Project: {project_name}")
    print(f"📝 Transcript: {transcript}")
    
    try:
        # Test with shorter timeout and fewer agents
        result = await orchestrator.execute_workflow(
            project_name=project_name,
            transcript=transcript,
            workflow_type="full",
            max_workflow_time=300  # 5 minutes total
        )
        
        print(f"✅ Workflow completed!")
        print(f"Status: {result.get('status')}")
        print(f"Results keys: {list(result.get('results', {}).keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simple_workflow())
    sys.exit(0 if success else 1)