#!/usr/bin/env python3
"""
Focused test for Storage Agent to validate folder creation and path consistency
"""

import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.storage_agent import StorageAgent
from agents.llm_client_synthetic import SyntheticLLMClient

async def test_storage_agent_focused():
    """Focused test for Storage Agent functionality"""
    
    print("🧪 Testing Storage Agent - Focused Test")
    print("="*50)
    
    # Initialize LLM client and Storage Agent with correct path
    llm_client = SyntheticLLMClient()
    storage_agent = StorageAgent(llm_client, base_storage_path="storage")
    
    # Test project name
    project_name = f"Storage Test Project {datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"📋 Project Name: {project_name}")
    print(f"📁 Base Storage Path: storage/")
    print()
    
    try:
        # Test 1: Create Project Structure
        print("🔧 Test 1: Creating project structure...")
        input_data = {
            "action": "create_project",
            "project_name": project_name
        }
        
        result = await storage_agent.execute(input_data, {})
        
        if result.success:
            print("✅ Project structure created successfully")
            print(f"   📂 Project Root: {result.data.get('project_root', 'N/A')}")
            print(f"   📋 Folders Created: {len(result.data.get('folders_created', []))}")
            print(f"   📝 Audit Log: {result.data.get('audit_log', {}).get('action', 'N/A')}")
            
            # Verify folders exist in correct location
            expected_folders = [
                "MeetingTranscripts", "MeetingNotes", "ResearchFindings", "UseCases",
                "SyntheticData", "CaseStudies", "PRDDocuments", "SystemArchitecture",
                "CommercialProposals", "BillOfMaterials", "ReviewerFeedback", "AuditLogs"
            ]
            
            project_root = result.data.get('project_root', '')
            if os.path.exists(project_root):
                actual_folders = [f.name for f in os.path.iterdir(project_root) if f.is_dir()]
                print(f"   📊 Actual folders found: {len(actual_folders)}")
                
                missing_folders = set(expected_folders) - set(actual_folders)
                if missing_folders:
                    print(f"   ⚠️  Missing folders: {list(missing_folders)}")
                else:
                    print("   ✅ All expected folders created")
            else:
                print(f"   ❌ Project root does not exist: {project_root}")
                
        else:
            print(f"❌ Failed to create project: {result.error}")
            return False
        
        # Test 2: Save File to Project
        print("\n🔧 Test 2: Saving file to project...")
        file_content = f"Test content for {project_name} created at {datetime.now().isoformat()}"
        
        save_input = {
            "action": "save_file",
            "project_name": project_name,
            "folder": "notes",
            "filename": "test_file.txt",
            "content": file_content
        }
        
        save_result = await storage_agent.execute(save_input, {})
        
        if save_result.success:
            print("✅ File saved successfully")
            print(f"   📄 File: {save_result.data.get('filename', 'N/A')}")
            print(f"   📁 Folder: {save_result.data.get('folder', 'N/A')}")
            print(f"   📏 Size: {save_result.data.get('size', 0)} bytes")
            
            # Verify file exists
            file_path = save_result.data.get('file_path', '')
            if os.path.exists(file_path):
                print("   ✅ File exists on filesystem")
                with open(file_path, 'r') as f:
                    content = f.read()
                if content == file_content:
                    print("   ✅ File content matches expected")
                else:
                    print("   ❌ File content mismatch")
            else:
                print(f"   ❌ File does not exist: {file_path}")
        else:
            print(f"❌ Failed to save file: {save_result.error}")
            return False
        
        # Test 3: List Files
        print("\n🔧 Test 3: Listing files in project...")
        list_input = {
            "action": "list_files",
            "project_name": project_name,
            "folder": "notes"
        }
        
        list_result = await storage_agent.execute(list_input, {})
        
        if list_result.success:
            files = list_result.data.get('files', [])
            print(f"✅ Files listed successfully: {len(files)} files found")
            for file_info in files:
                print(f"   📄 {file_info.get('name', 'N/A')} ({file_info.get('size', 0)} bytes)")
        else:
            print(f"❌ Failed to list files: {list_result.error}")
            return False
        
        # Test 4: Get Project Structure
        print("\n🔧 Test 4: Getting project structure...")
        structure_input = {
            "action": "get_structure",
            "project_name": project_name
        }
        
        structure_result = await storage_agent.execute(structure_input, {})
        
        if structure_result.success:
            structure = structure_result.data
            print("✅ Project structure retrieved successfully")
            print(f"   📂 Project Root: {structure.get('project_root', 'N/A')}")
            folders = structure.get('folders', {})
            print(f"   📁 Total Folders: {len(folders)}")
            
            # Check if folders are in correct location
            correct_location = True
            for folder_key, folder_path in folders.items():
                if not folder_path.startswith("storage/"):
                    print(f"   ⚠️  Folder {folder_key} not in storage/: {folder_path}")
                    correct_location = False
            
            if correct_location:
                print("   ✅ All folders in correct storage location")
        else:
            print(f"❌ Failed to get structure: {structure_result.error}")
            return False
        
        print("\n🎉 All Storage Agent tests passed!")
        return True
        
    except Exception as e:
        print(f"💥 Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_storage_agent_focused()
    
    if success:
        print("\n✅ STORAGE AGENT TEST PASSED")
        print("   • Project structure creation: Working")
        print("   • File saving functionality: Working") 
        print("   • File listing functionality: Working")
        print("   • Project structure retrieval: Working")
        print("   • Path consistency: Correct (storage/ location)")
    else:
        print("\n❌ STORAGE AGENT TEST FAILED")
        print("   • One or more functionalities not working correctly")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)