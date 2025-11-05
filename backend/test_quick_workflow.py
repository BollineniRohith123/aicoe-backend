#!/usr/bin/env python3
"""
Quick test script to verify complete workflow execution with shorter content
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import OrchestratorAgent
from agents.llm_client import LLMClient

async def test_quick_workflow():
    """Test the workflow with a shorter transcript for faster execution"""
    
    print("🚀 Starting quick workflow test...")
    
    # Initialize real LLM client
    llm_client = LLMClient()
    print("✅ Using real LLM client with OpenRouter API")
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent(llm_client)
    
    # Shorter test transcript for faster execution
    test_transcript = """
    Hi team, we need to build a simple task management app. The main features should include creating tasks, marking them as complete, and setting due dates. We should use a clean, modern design. The backend will be Node.js with Express, and we'll use React for the frontend. Let's make sure it's mobile-friendly too.
    
    Sarah: Sounds good! For the database, should we use MongoDB or PostgreSQL? Also, what about user authentication?
    
    I think PostgreSQL would be better for this type of application. For authentication, we can start with simple email/password and maybe add Google OAuth later. The app should be responsive and work well on both desktop and mobile.
    
    Sarah: Perfect. What about deployment? Should we use AWS or something else?
    
    Let's go with AWS for now. We can deploy using Docker containers and set up CI/CD with GitHub Actions. This will make it easy to scale and maintain.
    """
    
    project_name = "Task Management App - Quick Test"
    
    print(f"📝 Project: {project_name}")
    print(f"📄 Transcript length: {len(test_transcript)} characters")
    print()
    
    try:
        # Execute the complete workflow with shorter timeout
        result = await orchestrator.execute_workflow(
            project_name=project_name,
            transcript=test_transcript,
            workflow_type="full",
            max_workflow_time=600  # 10 minutes max for quick test
        )
        
        print("✅ Quick workflow execution completed!")
        print(f"📊 Status: {result.get('status', 'unknown')}")
        print(f"🆔 Workflow ID: {result.get('workflow_id', 'N/A')}")
        
        if result.get('status') == 'success':
            print(f"📈 Completed stages: {len([s for s in result.get('stages', []) if s['status'] == 'completed'])}")
            print(f"❌ Failed stages: {len([s for s in result.get('stages', []) if s['status'] == 'failed'])}")
            
            # Print stage results summary
            print("\n📋 Stage Results Summary:")
            for stage in result.get('stages', []):
                status_emoji = "✅" if stage['status'] == 'completed' else "❌" if stage['status'] == 'failed' else "⏳"
                duration = f"({stage.get('duration', 0):.1f}s)" if stage.get('duration') else ""
                print(f"  {status_emoji} {stage['name']}: {stage['status']} {duration}")
            
            # Print results summary
            print(f"\n📁 Generated Artifacts:")
            for agent_name, agent_result in result.get('results', {}).items():
                if agent_result and isinstance(agent_result, dict):
                    print(f"  📄 {agent_name}: {len(str(agent_result))} characters of data")
                    
        else:
            print(f"❌ Workflow failed: {result.get('error', 'Unknown error')}")
            
        return result
        
    except Exception as e:
        print(f"❌ Workflow execution failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_quick_workflow())