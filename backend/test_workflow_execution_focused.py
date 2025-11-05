#!/usr/bin/env python3
"""
Focused Workflow Execution Test
Tests the complete orchestrator workflow to ensure all agents work together properly.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Add agents to path
sys.path.append('agents')

from agents.orchestrator import OrchestratorAgent
from agents.workflow_context import WorkflowContext
from agents.llm_client_synthetic import SyntheticLLMClient

class FocusedWorkflowTester:
    def __init__(self):
        self.test_results = []
        self.project_name = f"Focused Workflow Test {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.base_storage_path = "storage"
        
    async def test_complete_workflow(self):
        """Test the complete orchestrator workflow"""
        print(f"🚀 Starting Focused Workflow Test")
        print(f"📋 Project: {self.project_name}")
        print(f"⏰ Start Time: {datetime.now().isoformat()}")
        print()
        
        try:
            # Initialize LLM client and orchestrator
            llm_client = SyntheticLLMClient()
            orchestrator = OrchestratorAgent(llm_client)
            
            print("🧪 Running Complete Orchestrator Workflow...")
            start_time = datetime.now()
            
            # Execute the complete workflow
            result = await orchestrator.execute_workflow(
                project_name=self.project_name,
                transcript="Create a comprehensive e-commerce platform with user management, product catalog, shopping cart, and payment processing. Include mobile responsiveness and security features.",
                workflow_type="full",
                max_workflow_time=1800  # 30 minutes timeout
            )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"✅ Workflow completed in {duration:.1f} seconds")
            print()
            
            # Validate results
            validation_result = await self.validate_workflow_results()
            
            # Generate report
            await self.generate_workflow_report(result, validation_result, duration)
            
            return validation_result['success']
            
        except Exception as e:
            print(f"❌ Workflow execution failed: {str(e)}")
            await self.generate_error_report(str(e))
            return False
    
    async def validate_workflow_results(self):
        """Validate that all expected files were created"""
        print("🔍 Validating Workflow Results...")
        
        project_path = Path(self.base_storage_path) / self.project_name
        validation_results = {
            'success': True,
            'missing_files': [],
            'created_files': [],
            'validation_details': {}
        }
        
        # Expected file patterns for each agent
        expected_files = {
            'Storage Agent': ['AuditLogs/audit_log.json'],
            'Intake Agent': ['MeetingTranscripts/intake_transcript.json'],
            'Research Agent': ['ResearchFindings/research_findings.json'],
            'Blueprint Agent': ['UseCases/use_cases.json'],
            'BRD Agent': ['BusinessRequirements/BRD_v1.xml', 'BusinessRequirements/BRD_v1.html'],
            'FR Agent': ['FunctionalRequirements/FR_v1.xml', 'FunctionalRequirements/FR_v1.html'],
            'PRD Agent': ['PRDDocuments/PRD_v1.html'],
            'Mockup Agent': ['SyntheticData/mockup_data.json'],
            'Architecture Agent': ['SystemArchitecture/architecture_diagram.json'],
            'BOM Agent': ['BillOfMaterials/bom_v1.json'],
            'TC Agent': ['SyntheticData/test_cases.json'],
            'Proposal Agent': ['CommercialProposals/proposal_v1.html'],
            'Gallery Agent': ['CaseStudies/case_study_data.json']
        }
        
        for agent_name, files in expected_files.items():
            agent_files = []
            for file_path in files:
                full_path = project_path / file_path
                if full_path.exists():
                    agent_files.append(str(full_path))
                    validation_results['created_files'].append(f"{agent_name}: {file_path}")
                else:
                    validation_results['missing_files'].append(f"{agent_name}: {file_path}")
                    validation_results['success'] = False
            
            validation_results['validation_details'][agent_name] = {
                'expected': len(files),
                'found': len(agent_files),
                'files': agent_files
            }
        
        # Print validation summary
        print(f"📊 Validation Summary:")
        print(f"   ✅ Created Files: {len(validation_results['created_files'])}")
        print(f"   ❌ Missing Files: {len(validation_results['missing_files'])}")
        
        if validation_results['missing_files']:
            print(f"   📋 Missing Files:")
            for missing in validation_results['missing_files']:
                print(f"      - {missing}")
        
        print()
        return validation_results
    
    async def generate_workflow_report(self, orchestrator_result, validation_result, duration):
        """Generate a comprehensive workflow report"""
        report_path = Path(self.base_storage_path) / self.project_name / "WorkflowTestReport.json"
        
        report = {
            'test_info': {
                'test_name': 'Focused Workflow Execution Test',
                'project_name': self.project_name,
                'start_time': datetime.now().isoformat(),
                'duration_seconds': duration,
                'test_status': 'PASSED' if validation_result['success'] else 'FAILED'
            },
            'orchestrator_result': {
                'success': orchestrator_result.get('success', False),
                'completed_agents': orchestrator_result.get('completed_agents', []),
                'failed_agents': orchestrator_result.get('failed_agents', []),
                'total_agents': len(orchestrator_result.get('completed_agents', [])) + len(orchestrator_result.get('failed_agents', []))
            },
            'validation_results': validation_result,
            'file_summary': {
                'total_expected': sum(len(files) for files in [
                    ['AuditLogs/audit_log.json'],
                    ['MeetingTranscripts/intake_transcript.json'],
                    ['ResearchFindings/research_findings.json'],
                    ['UseCases/use_cases.json'],
                    ['BusinessRequirements/BRD_v1.xml', 'BusinessRequirements/BRD_v1.html'],
                    ['FunctionalRequirements/FR_v1.xml', 'FunctionalRequirements/FR_v1.html'],
                    ['PRDDocuments/PRD_v1.html'],
                    ['SyntheticData/mockup_data.json'],
                    ['SystemArchitecture/architecture_diagram.json'],
                    ['BillOfMaterials/bom_v1.json'],
                    ['SyntheticData/test_cases.json'],
                    ['CommercialProposals/proposal_v1.html'],
                    ['CaseStudies/case_study_data.json']
                ]),
                'total_created': len(validation_result['created_files']),
                'success_rate': len(validation_result['created_files']) / sum(len(files) for files in [
                    ['AuditLogs/audit_log.json'],
                    ['MeetingTranscripts/intake_transcript.json'],
                    ['ResearchFindings/research_findings.json'],
                    ['UseCases/use_cases.json'],
                    ['BusinessRequirements/BRD_v1.xml', 'BusinessRequirements/BRD_v1.html'],
                    ['FunctionalRequirements/FR_v1.xml', 'FunctionalRequirements/FR_v1.html'],
                    ['PRDDocuments/PRD_v1.html'],
                    ['SyntheticData/mockup_data.json'],
                    ['SystemArchitecture/architecture_diagram.json'],
                    ['BillOfMaterials/bom_v1.json'],
                    ['SyntheticData/test_cases.json'],
                    ['CommercialProposals/proposal_v1.html'],
                    ['CaseStudies/case_study_data.json']
                ]) * 100
            }
        }
        
        # Ensure directory exists
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Workflow report saved to: {report_path}")
        print()
        
        # Print final summary
        print("🎯 FINAL WORKFLOW TEST SUMMARY")
        print("=" * 50)
        print(f"Test Status: {'✅ PASSED' if validation_result['success'] else '❌ FAILED'}")
        print(f"Duration: {duration:.1f} seconds")
        print(f"Files Created: {len(validation_result['created_files'])}")
        print(f"Success Rate: {report['file_summary']['success_rate']:.1f}%")
        print(f"Report Location: {report_path}")
        
    async def generate_error_report(self, error_message):
        """Generate error report if workflow fails"""
        error_report = {
            'test_info': {
                'test_name': 'Focused Workflow Execution Test',
                'project_name': self.project_name,
                'start_time': datetime.now().isoformat(),
                'test_status': 'ERROR',
                'error_message': error_message
            }
        }
        
        report_path = Path(self.base_storage_path) / self.project_name / "WorkflowErrorReport.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(error_report, f, indent=2)
        
        print(f"❌ Error report saved to: {report_path}")

async def main():
    """Main test execution"""
    tester = FocusedWorkflowTester()
    success = await tester.test_complete_workflow()
    
    if success:
        print("\n🎉 All workflow tests PASSED! The system is working correctly.")
        return 0
    else:
        print("\n💥 Some workflow tests FAILED! Please check the reports.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)