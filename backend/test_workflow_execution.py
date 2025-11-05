#!/usr/bin/env python3
"""
Test script to execute the complete multi-agent workflow
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

async def test_workflow():
    """Test the complete workflow execution"""
    
    print("🚀 Starting comprehensive workflow test...")
    
    # Initialize real LLM client
    llm_client = LLMClient()
    print("✅ Using real LLM client with OpenRouter API")
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent(llm_client)
    
    # Test transcript (messy, realistic conversation)
    test_transcript = """
    Hey Sarah, did you get my email about the insurance portal project? We need to discuss the customer dashboard features. I think we should focus on policy management and claims tracking. Also, what about the mobile app integration? The client mentioned something about real-time notifications. Let me know when you have time to review the requirements document I sent. Thanks! Also, can we schedule a meeting for next week? I have some additional thoughts on the user interface design.
    
    Sarah: Yeah, I got your email. The policy management and claims tracking sound good. For mobile app integration, we should probably use React Native since we already have that expertise. The real-time notifications could be handled through Firebase Cloud Messaging. When do you want to meet? I'm free Tuesday or Wednesday afternoon.
    
    Great! Tuesday works. Also, I was thinking about the user interface - should we go with a modern, clean design? Maybe something similar to what we did for the banking app last year? The client mentioned they want it to be user-friendly for older customers too, so we need to make sure the text is large enough and the navigation is intuitive.
    
    Sarah: Good point about the older customers. Let's definitely make sure we have good accessibility features. For the design, I think a clean, modern approach would work well. We should also consider having a dark mode option, even though the client didn't specifically ask for it. It might be a nice bonus feature.
    
    Yeah, dark mode is always a good addition. What about the backend architecture? I was thinking we could use Node.js with Express for the API, and PostgreSQL for the database. For the insurance-specific features, we'll need to integrate with some third-party services for policy validation and claims processing.
    
    Sarah: That sounds solid. For the third-party integrations, we should probably use a microservices architecture so we can easily swap out providers if needed. Also, we'll need to make sure we have proper logging and monitoring in place since this is a financial application.
    
    Absolutely. Security is going to be crucial here. We'll need to implement proper authentication, maybe using OAuth 2.0, and ensure all data is encrypted both in transit and at rest. The client mentioned they need to comply with some insurance industry regulations too.
    
    Sarah: Right, we should definitely look into SOC 2 compliance and maybe GDPR if they have European customers. Also, we should plan for scalability from the start - insurance companies can have thousands of users, so we need to make sure our architecture can handle that load.
    
    Good points. Let's also think about the testing strategy. We'll need unit tests, integration tests, and probably some automated UI tests. The client mentioned they want to be involved in the testing process too.
    
    Sarah: Definitely. We should set up a staging environment where they can test features before we deploy to production. Also, we should plan for a phased rollout rather than a big bang deployment.
    
    Agreed. I think we have a pretty solid plan here. Let me compile all of this into a proper requirements document and we can review it together next week.
    
    Sarah: Sounds good. Oh, one more thing - the client mentioned they might want to add a feature for customers to upload photos of damage for claims. We should keep that in mind for future iterations.
    
    Great catch! We'll definitely include that in the roadmap. Thanks for the productive discussion, Sarah.
    """
    
    project_name = "Insurance Customer Portal - Comprehensive Test"
    
    print(f"📝 Project: {project_name}")
    print(f"📄 Transcript length: {len(test_transcript)} characters")
    print()
    
    try:
        # Execute the complete workflow
        result = await orchestrator.execute_workflow(
            project_name=project_name,
            transcript=test_transcript,
            workflow_type="full",
            max_workflow_time=1800  # 30 minutes max for testing
        )
        
        print("✅ Workflow execution completed!")
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
    asyncio.run(test_workflow())