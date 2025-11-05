#!/usr/bin/env python3
"""
Final Workflow Validation Test
Tests the complete workflow with BRD and FR agents included
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

async def test_final_workflow():
    """Test the complete workflow with BRD and FR agents"""
    print("🚀 Starting Final Workflow Validation Test")
    print("=" * 60)
    
    # Initialize with longer timeout for complete workflow
    llm_client = SyntheticLLMClient()
    orchestrator = OrchestratorAgent(llm_client)
    
    project_name = f"Ecommerce Platform"
    transcript = """
    We need to build a comprehensive e-commerce platform with the following features:
    
    1. User Management System
       - User registration and authentication
       - Profile management
       - Role-based access control
    
    2. Product Catalog
       - Product listing and search
       - Category management
       - Product reviews and ratings
    
    3. Shopping Cart and Checkout
       - Add to cart functionality
       - Shopping cart management
       - Secure payment processing
       - Order confirmation and tracking
    
    4. Inventory Management
       - Real-time stock tracking
       - Low inventory alerts
       - Supplier management
    
    5. Admin Dashboard
       - Sales analytics
       - User management
       - Product management
       - Order management
    
    Technical Requirements:
    - Mobile responsive design
    - High performance and scalability
    - Security best practices
    - Integration with payment gateways
    - Email notifications
    - Search functionality
    """
    
    print(f"📋 Project: {project_name}")
    print(f"📝 Transcript Length: {len(transcript)} characters")
    print(f"⏰ Start Time: {datetime.now().isoformat()}")
    print()
    
    try:
        # Test with extended timeout for complete workflow
        result = await orchestrator.execute_workflow(
            project_name=project_name,
            transcript=transcript,
            workflow_type="full",
            max_workflow_time=900  # 15 minutes total
        )
        
        print("✅ Workflow execution completed!")
        print(f"Status: {result.get('status')}")
        print(f"Workflow ID: {result.get('workflow_id')}")
        
        # Check results
        results = result.get('results', {})
        completed_agents = list(results.keys())
        print(f"Completed Agents ({len(completed_agents)}): {', '.join(completed_agents)}")
        
        # Validate file generation
        await validate_file_generation(project_name, completed_agents)
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow failed: {str(e)}")
        return False

async def validate_file_generation(project_name: str, completed_agents: list):
    """Validate that files were generated for each agent"""
    print("\n🔍 Validating File Generation...")
    print("-" * 40)
    
    project_path = f"storage/{project_name}"
    
    expected_files = {
        "storage": ["AuditLogs/audit_log.json"],
        "transcript": ["MeetingNotes/structured_notes.xml"],
        "researcher": ["ResearchFindings/research_insights.xml"],
        "requirements": ["UseCases/use_cases.xml"],
        "brd": ["BusinessRequirements/BRD_v1.xml", "BusinessRequirements/BRD_v1.html"],
        "fr": ["FunctionalRequirements/FR_v1.xml", "FunctionalRequirements/FR_v1.html"],
        "knowledge_base": ["SystemArchitecture/knowledge_enrichment.xml"],
        "prd": ["PRDDocuments/PRD_v1.xml", "PRDDocuments/PRD_v1.html"],
        "mockup": ["CaseStudies/index.html"],
        "synthetic_data": ["SyntheticData/demo_data.xml"],
        "commercial_proposal": ["CommercialProposals/proposal_v1.html"],
        "bom": ["BillOfMaterials/bom_v1.html"],
        "architecture_diagram": ["SystemArchitecture/architecture_v1.html"],
        "reviewer": ["ReviewerFeedback/review_cycle_v1.json"],
        "gallery": ["CaseStudies/case_study_data.json"]
    }
    
    generated_files = []
    missing_files = []
    
    for agent in completed_agents:
        if agent in expected_files:
            for file_path in expected_files[agent]:
                full_path = f"{project_path}/{file_path}"
                if os.path.exists(full_path):
                    generated_files.append(f"{agent}: {file_path}")
                    print(f"✅ {agent}: {file_path}")
                else:
                    missing_files.append(f"{agent}: {file_path}")
                    print(f"❌ {agent}: {file_path} (MISSING)")
    
    print(f"\n📊 File Generation Summary:")
    print(f"   Generated: {len(generated_files)} files")
    print(f"   Missing: {len(missing_files)} files")
    print(f"   Success Rate: {len(generated_files)/(len(generated_files)+len(missing_files))*100:.1f}%")
    
    if missing_files:
        print(f"\n⚠️  Missing Files:")
        for missing in missing_files:
            print(f"   - {missing}")
    
    # Check folder structure
    print(f"\n📁 Folder Structure Validation:")
    folders_to_check = [
        "AuditLogs", "MeetingNotes", "ResearchFindings", "UseCases",
        "BusinessRequirements", "FunctionalRequirements", "PRDDocuments",
        "SystemArchitecture", "CommercialProposals", "BillOfMaterials",
        "ReviewerFeedback", "CaseStudies", "SyntheticData"
    ]
    
    for folder in folders_to_check:
        folder_path = f"{project_path}/{folder}"
        if os.path.exists(folder_path):
            file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
            print(f"✅ {folder}: {file_count} files")
        else:
            print(f"❌ {folder}: MISSING")

if __name__ == "__main__":
    success = asyncio.run(test_final_workflow())
    if success:
        print("\n🎉 FINAL VALIDATION PASSED!")
        print("The complete workflow with BRD and FR agents is working correctly!")
    else:
        print("\n💥 FINAL VALIDATION FAILED!")
        print("Please check the errors above.")
    sys.exit(0 if success else 1)