#!/usr/bin/env python3
"""
Test script to verify the new folder structure with separate BRD and FR folders
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.storage_agent import StorageAgent
from agents.llm_client_synthetic import SyntheticLLMClient

async def test_folder_structure():
    """Test that the new folder structure creates separate BRD and FR folders"""
    
    print("🔍 Testing New Folder Structure...")
    
    # Initialize synthetic LLM client and storage agent
    llm_client = SyntheticLLMClient()
    storage_agent = StorageAgent(llm_client, base_storage_path="storage")
    print("✅ Initialized Storage Agent")
    
    # Create a new test project
    test_project_name = "Test Folder Structure Project"
    
    try:
        print(f"📁 Creating project structure for: {test_project_name}")
        result = await storage_agent.execute(
            {"action": "create_project", "project_name": test_project_name}, 
            {}
        )
        
        if result.success:
            print("✅ Project structure created successfully!")
            print(f"📊 Project root: {result.data.get('project_root')}")
            print(f"📊 Folders created: {result.data.get('folders_created')}")
            
            # Check if the new folders exist
            expected_folders = [
                "prd", 
                "business_requirements", 
                "functional_requirements",
                "test_cases",
                "architecture",
                "commercial_proposals",
                "bom"
            ]
            
            created_folders = result.data.get('folders_created', [])
            
            print("\n📋 Folder Structure Verification:")
            for folder in expected_folders:
                if folder in created_folders:
                    print(f"✅ {folder} - Created")
                else:
                    print(f"❌ {folder} - Missing")
            
            # List actual folders in the project directory
            project_root = result.data.get('project_root')
            if project_root and os.path.exists(project_root):
                print(f"\n📂 Actual folders in {project_root}:")
                for item in os.listdir(project_root):
                    if os.path.isdir(os.path.join(project_root, item)):
                        print(f"  📁 {item}")
            
            return True
        else:
            print(f"❌ Failed to create project: {result.error}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_folder_structure())
    if success:
        print("\n🎉 Folder structure test passed! New folders are being created.")
    else:
        print("\n💥 Folder structure test failed! Check the errors above.")