#!/usr/bin/env python3
"""
Test script to verify BRD and FR files are stored in separate folders
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
from agents.brd_agent import BRDAgent
from agents.fr_agent import FRAgent
from agents.llm_client_synthetic import SyntheticLLMClient

async def test_brd_fr_storage():
    """Test that BRD and FR files are stored in separate folders"""
    
    print("🔍 Testing BRD and FR Storage in Separate Folders...")
    
    # Initialize clients and agents
    llm_client = SyntheticLLMClient()
    storage_agent = StorageAgent(llm_client, base_storage_path="storage")
    brd_agent = BRDAgent(llm_client)
    fr_agent = FRAgent(llm_client)
    print("✅ Initialized all agents")
    
    # Create a new test project
    test_project_name = "BRD FR Storage Test Project"
    
    try:
        # Step 1: Create project structure
        print(f"📁 Creating project structure for: {test_project_name}")
        create_result = await storage_agent.execute(
            {"action": "create_project", "project_name": test_project_name}, 
            {}
        )
        
        if not create_result.success:
            print(f"❌ Failed to create project: {create_result.error}")
            return False
        
        print("✅ Project structure created successfully!")
        
        # Step 2: Generate BRD content
        print("📝 Generating BRD content...")
        test_input = {
            "project_name": test_project_name,
            "structured_notes": {
                "project_overview": "A test project for BRD/FR storage verification",
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
        
        brd_result = await brd_agent.execute(test_input, {"project_name": test_project_name})
        
        if not brd_result.success:
            print(f"❌ BRD generation failed: {brd_result.error}")
            return False
        
        print("✅ BRD content generated successfully!")
        
        # Step 3: Generate FR content
        print("📝 Generating FR content...")
        fr_result = await fr_agent.execute(test_input, {"project_name": test_project_name})
        
        if not fr_result.success:
            print(f"❌ FR generation failed: {fr_result.error}")
            return False
        
        print("✅ FR content generated successfully!")
        
        # Step 4: Save BRD files to storage
        print("💾 Saving BRD files to BusinessRequirements folder...")
        brd_save_input = {
            "action": "save_file",
            "project_name": test_project_name,
            "folder": "business_requirements",
            "filename": "BRD_v1.xml",
            "content": brd_result.data.get("brd_xml", "")
        }
        
        brd_xml_result = await storage_agent.execute(brd_save_input, {})
        
        brd_html_save_input = {
            "action": "save_file",
            "project_name": test_project_name,
            "folder": "business_requirements",
            "filename": "BRD_v1.html",
            "content": brd_result.data.get("brd_html", "")
        }
        
        brd_html_result = await storage_agent.execute(brd_html_save_input, {})
        
        # Step 5: Save FR files to storage
        print("💾 Saving FR files to FunctionalRequirements folder...")
        fr_save_input = {
            "action": "save_file",
            "project_name": test_project_name,
            "folder": "functional_requirements",
            "filename": "FR_v1.xml",
            "content": fr_result.data.get("fr_xml", "")
        }
        
        fr_xml_result = await storage_agent.execute(fr_save_input, {})
        
        fr_html_save_input = {
            "action": "save_file",
            "project_name": test_project_name,
            "folder": "functional_requirements",
            "filename": "FR_v1.html",
            "content": fr_result.data.get("fr_html", "")
        }
        
        fr_html_result = await storage_agent.execute(fr_html_save_input, {})
        
        # Step 6: Verify files are in correct folders
        print("🔍 Verifying file storage...")
        
        project_root = create_result.data.get('project_root')
        business_requirements_path = os.path.join(project_root, "BusinessRequirements")
        functional_requirements_path = os.path.join(project_root, "FunctionalRequirements")
        
        # Check BRD files
        brd_xml_exists = os.path.exists(os.path.join(business_requirements_path, "BRD_v1.xml"))
        brd_html_exists = os.path.exists(os.path.join(business_requirements_path, "BRD_v1.html"))
        
        # Check FR files
        fr_xml_exists = os.path.exists(os.path.join(functional_requirements_path, "FR_v1.xml"))
        fr_html_exists = os.path.exists(os.path.join(functional_requirements_path, "FR_v1.html"))
        
        print("\n📋 Storage Verification Results:")
        print(f"📁 BusinessRequirements folder: {business_requirements_path}")
        print(f"  ✅ BRD_v1.xml: {'EXISTS' if brd_xml_exists else 'MISSING'}")
        print(f"  ✅ BRD_v1.html: {'EXISTS' if brd_html_exists else 'MISSING'}")
        
        print(f"\n📁 FunctionalRequirements folder: {functional_requirements_path}")
        print(f"  ✅ FR_v1.xml: {'EXISTS' if fr_xml_exists else 'MISSING'}")
        print(f"  ✅ FR_v1.html: {'EXISTS' if fr_html_exists else 'MISSING'}")
        
        # List actual files in each folder
        if os.path.exists(business_requirements_path):
            print(f"\n📂 Files in BusinessRequirements:")
            for file in os.listdir(business_requirements_path):
                print(f"  📄 {file}")
        
        if os.path.exists(functional_requirements_path):
            print(f"\n📂 Files in FunctionalRequirements:")
            for file in os.listdir(functional_requirements_path):
                print(f"  📄 {file}")
        
        # Overall success check
        all_files_exist = brd_xml_exists and brd_html_exists and fr_xml_exists and fr_html_exists
        
        if all_files_exist:
            print("\n🎉 SUCCESS: All BRD and FR files are stored in their correct separate folders!")
            return True
        else:
            print("\n❌ FAILURE: Some files are missing from their expected folders.")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_brd_fr_storage())
    if success:
        print("\n🎉 BRD and FR storage test PASSED! Files are properly organized in separate folders.")
    else:
        print("\n💥 BRD and FR storage test FAILED! Check the errors above.")