#!/usr/bin/env python3
"""
Comprehensive End-to-End Testing Framework for All Backend Agents
Tests each agent individually and validates complete workflow execution
"""

import asyncio
import sys
import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.storage_agent import StorageAgent
from agents.intake_agent import IntakeAgent
from agents.researcher_agent import ResearcherAgent
from agents.blueprint_agent import BlueprintAgent
from agents.brd_agent import BRDAgent
from agents.fr_agent import FRAgent
from agents.prd_agent import PRDAgent
from agents.mockup_agent import MockupAgent
from agents.architecture_agent import ArchitectureAgent
from agents.bom_agent import BOMAgent
from agents.data_agent import DataAgent
from agents.proposal_agent import ProposalAgent
from agents.gallery_agent import CaseStudyGalleryAgent
from agents.llm_client_synthetic import SyntheticLLMClient

class ComprehensiveAgentTester:
    """Comprehensive testing framework for all agents"""
    
    def __init__(self):
        self.llm_client = SyntheticLLMClient()
        # Use same base storage path as orchestrator
        from agents.storage_agent import StorageAgent
        self.storage_agent = StorageAgent(self.llm_client, base_storage_path="storage")
        self.test_results = []
        self.project_name = f"Comprehensive Test Project {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.test_transcript = """
        Hi team, we need to build a comprehensive project management system. The main features should include task management, team collaboration, real-time updates, and analytics dashboard. We should use modern technologies like React for frontend, Node.js for backend, and PostgreSQL for database. The system should be scalable, secure, and user-friendly.
        
        Sarah: Sounds great! What about user authentication and authorization? Should we implement role-based access control?
        
        Yes, absolutely. We'll need different user roles like admin, project manager, and team member. Each role should have different permissions and access levels. Also, let's make sure the system supports real-time notifications and has a mobile-responsive design.
        
        Sarah: Perfect. For the database design, should we use a relational approach or consider NoSQL for better scalability?
        
        I think PostgreSQL would be better for this type of application since we need complex relationships between users, projects, tasks, and teams. We can always add Redis for caching and real-time features. Let's also plan for API integrations with popular tools like Slack and Microsoft Teams.
        """
        
    async def test_agent(self, agent_name: str, agent, input_data: dict, expected_outputs: list) -> dict:
        """Test individual agent and validate outputs"""
        print(f"\n🧪 Testing {agent_name}...")
        
        start_time = time.time()
        try:
            # Execute agent with timeout protection
            result = await asyncio.wait_for(
                agent.execute(input_data, {}),
                timeout=300  # 5 minutes max per agent
            )
            
            execution_time = time.time() - start_time
            
            if result.success:
                # Validate expected outputs
                missing_outputs = []
                for output in expected_outputs:
                    if output not in result.data:
                        missing_outputs.append(output)
                
                if missing_outputs:
                    status = "partial_success"
                    message = f"Missing outputs: {missing_outputs}"
                else:
                    status = "success"
                    message = "All expected outputs generated"
                
                # Log successful execution
                print(f"✅ {agent_name}: {status} ({execution_time:.1f}s)")
                
                return {
                    "agent": agent_name,
                    "status": status,
                    "execution_time": execution_time,
                    "message": message,
                    "data": result.data,
                    "error": None
                }
            else:
                print(f"❌ {agent_name}: failed - {result.error}")
                return {
                    "agent": agent_name,
                    "status": "failed",
                    "execution_time": execution_time,
                    "message": "Agent execution failed",
                    "data": None,
                    "error": result.error
                }
                
        except asyncio.TimeoutError:
            print(f"⏰ {agent_name}: timeout")
            return {
                "agent": agent_name,
                "status": "timeout",
                "execution_time": 300,
                "message": "Agent execution timed out",
                "data": None,
                "error": "Timeout after 300 seconds"
            }
        except Exception as e:
            print(f"💥 {agent_name}: exception - {str(e)}")
            return {
                "agent": agent_name,
                "status": "exception",
                "execution_time": time.time() - start_time,
                "message": "Agent execution exception",
                "data": None,
                "error": str(e)
            }
    
    async def test_storage_agent(self) -> dict:
        """Test Storage Agent"""
        # Use the properly initialized storage agent with correct base path
        agent = self.storage_agent
        input_data = {
            "action": "create_project",
            "project_name": self.project_name
        }
        return await self.test_agent("Storage Agent", agent, input_data, ["project_name", "project_root"])
    
    async def test_intake_agent(self) -> dict:
        """Test Intake Agent"""
        agent = IntakeAgent(self.llm_client)
        input_data = {
            "project_name": self.project_name,
            "transcript": self.test_transcript
        }
        return await self.test_agent("Intake Agent", agent, input_data, ["structured_notes"])
    
    async def test_researcher_agent(self) -> dict:
        """Test Researcher Agent"""
        agent = ResearcherAgent(self.llm_client)
        input_data = {
            "topic": self.project_name,
            "context": self.test_transcript,
            "structured_notes": {
                "project_name": self.project_name,
                "requirements": ["task management", "team collaboration"],
                "decisions_made": ["Use React", "Use Node.js", "Use PostgreSQL"]
            }
        }
        return await self.test_agent("Researcher Agent", agent, input_data, ["research_insights"])
    
    async def test_blueprint_agent(self) -> dict:
        """Test Blueprint Agent"""
        agent = BlueprintAgent(self.llm_client)
        input_data = {
            "project_name": self.project_name,
            "structured_notes": {
                "project_name": self.project_name,
                "requirements": ["task management", "team collaboration"],
                "decisions_made": ["Use React", "Use Node.js", "Use PostgreSQL"]
            },
            "research_insights": {
                "industry_trends": ["AI integration", "Cloud-first approach"],
                "technical_standards": ["REST APIs", "OAuth 2.0"]
            }
        }
        return await self.test_agent("Blueprint Agent", agent, input_data, ["use_cases"])
    
    async def test_brd_agent(self, previous_results: dict) -> dict:
        """Test BRD Agent"""
        agent = BRDAgent(self.llm_client)
        input_data = {
            "project_name": self.project_name,
            "structured_notes": previous_results.get("intake", {}).get("data", {}).get("structured_notes", {}),
            "use_cases": previous_results.get("blueprint", {}).get("data", {}).get("use_cases", []),
            "research_insights": previous_results.get("researcher", {}).get("data", {}).get("research_insights", {})
        }
        return await self.test_agent("BRD Agent", agent, input_data, ["brd_xml", "brd_html"])
    
    async def test_fr_agent(self, previous_results: dict) -> dict:
        """Test FR Agent"""
        agent = FRAgent(self.llm_client)
        input_data = {
            "project_name": self.project_name,
            "structured_notes": previous_results.get("intake", {}).get("data", {}).get("structured_notes", {}),
            "use_cases": previous_results.get("blueprint", {}).get("data", {}).get("use_cases", []),
            "business_requirements": previous_results.get("brd", {}).get("data", {}).get("business_requirements", {}),
            "research_insights": previous_results.get("researcher", {}).get("data", {}).get("research_insights", {})
        }
        return await self.test_agent("FR Agent", agent, input_data, ["fr_xml", "fr_html"])
    
    async def test_prd_agent(self, previous_results: dict) -> dict:
        """Test PRD Agent"""
        agent = PRDAgent(self.llm_client)
        input_data = {
            "project_name": self.project_name,
            "structured_notes": previous_results.get("intake", {}).get("data", {}).get("structured_notes", {}),
            "use_cases": previous_results.get("blueprint", {}).get("data", {}).get("use_cases", []),
            "business_requirements": previous_results.get("brd", {}).get("data", {}).get("business_requirements", {}),
            "functional_requirements": previous_results.get("fr", {}).get("data", {}).get("functional_requirements", {}),
            "research_insights": previous_results.get("researcher", {}).get("data", {}).get("research_insights", {})
        }
        return await self.test_agent("PRD Agent", agent, input_data, ["prd_xml", "prd_html"])
    
    async def test_mockup_agent(self, previous_results: dict) -> dict:
        """Test Mockup Agent"""
        agent = MockupAgent(self.llm_client)
        input_data = {
            "project_name": self.project_name,
            "use_cases": previous_results.get("blueprint", {}).get("data", {}).get("use_cases", []),
            "structured_notes": previous_results.get("intake", {}).get("data", {}).get("structured_notes", {}),
            "business_requirements": previous_results.get("brd", {}).get("data", {}).get("business_requirements", {}),
            "functional_requirements": previous_results.get("fr", {}).get("data", {}).get("functional_requirements", {}),
            "prd_content": previous_results.get("prd", {}).get("data", {}).get("prd_content", ""),
            "research_insights": previous_results.get("researcher", {}).get("data", {}).get("research_insights", {})
        }
        return await self.test_agent("Mockup Agent", agent, input_data, ["mockup_html", "mockup_pages"])
    
    async def test_architecture_agent(self, previous_results: dict) -> dict:
        """Test Architecture Agent"""
        agent = ArchitectureAgent(self.llm_client)
        input_data = {
            "project_name": self.project_name,
            "use_cases": previous_results.get("blueprint", {}).get("data", {}).get("use_cases", []),
            "business_requirements": previous_results.get("brd", {}).get("data", {}).get("business_requirements", {}),
            "functional_requirements": previous_results.get("fr", {}).get("data", {}).get("functional_requirements", {}),
            "prd_content": previous_results.get("prd", {}).get("data", {}).get("prd_content", ""),
            "research_insights": previous_results.get("researcher", {}).get("data", {}).get("research_insights", {})
        }
        return await self.test_agent("Architecture Agent", agent, input_data, ["architecture_xml", "architecture_html"])
    
    async def test_bom_agent(self, previous_results: dict) -> dict:
        """Test BOM Agent"""
        agent = BOMAgent(self.llm_client)
        input_data = {
            "project_name": self.project_name,
            "use_cases": previous_results.get("blueprint", {}).get("data", {}).get("use_cases", []),
            "business_requirements": previous_results.get("brd", {}).get("data", {}).get("business_requirements", {}),
            "functional_requirements": previous_results.get("fr", {}).get("data", {}).get("functional_requirements", {}),
            "architecture_content": previous_results.get("architecture", {}).get("data", {}).get("architecture_content", ""),
            "research_insights": previous_results.get("researcher", {}).get("data", {}).get("research_insights", {})
        }
        return await self.test_agent("BOM Agent", agent, input_data, ["bom_xml", "bom_html"])
    
    async def test_data_agent(self, previous_results: dict) -> dict:
        """Test Data Agent"""
        agent = DataAgent(self.llm_client)
        input_data = {
            "project_name": self.project_name,
            "use_cases": previous_results.get("blueprint", {}).get("data", {}).get("use_cases", []),
            "business_requirements": previous_results.get("brd", {}).get("data", {}).get("business_requirements", {}),
            "functional_requirements": previous_results.get("fr", {}).get("data", {}).get("functional_requirements", {}),
            "prd_content": previous_results.get("prd", {}).get("data", {}).get("prd_content", ""),
            "research_insights": previous_results.get("researcher", {}).get("data", {}).get("research_insights", {})
        }
        return await self.test_agent("Data Agent", agent, input_data, ["data_xml", "data_html"])
    
    async def test_proposal_agent(self, previous_results: dict) -> dict:
        """Test Proposal Agent"""
        agent = ProposalAgent(self.llm_client)
        input_data = {
            "project_name": self.project_name,
            "prd_content": previous_results.get("prd", {}).get("data", {}).get("prd_content", ""),
            "use_cases": previous_results.get("blueprint", {}).get("data", {}).get("use_cases", []),
            "business_requirements": previous_results.get("brd", {}).get("data", {}).get("business_requirements", {}),
            "functional_requirements": previous_results.get("fr", {}).get("data", {}).get("functional_requirements", {}),
            "bom_content": previous_results.get("bom", {}).get("data", {}).get("bom_content", ""),
            "data_content": previous_results.get("data", {}).get("data", {}).get("data_content", ""),
            "research_insights": previous_results.get("researcher", {}).get("data", {}).get("research_insights", {})
        }
        return await self.test_agent("Proposal Agent", agent, input_data, ["proposal_xml", "proposal_html"])
    
    async def test_gallery_agent(self, previous_results: dict) -> dict:
        """Test Gallery Agent"""
        agent = CaseStudyGalleryAgent(self.llm_client)
        input_data = {
            "current_project_name": self.project_name,
            "force_regenerate": False
        }
        return await self.test_agent("Gallery Agent", agent, input_data, ["gallery_html", "gallery_data"])
    
    async def run_comprehensive_test(self):
        """Run comprehensive end-to-end test of all agents"""
        print("🚀 Starting Comprehensive End-to-End Agent Testing")
        print(f"📋 Project: {self.project_name}")
        print(f"⏰ Start Time: {datetime.now().isoformat()}")
        
        overall_start_time = time.time()
        results = {}
        
        # Test agents in sequential order matching orchestrator workflow
        test_sequence = [
            ("storage", self.test_storage_agent),
            ("intake", self.test_intake_agent),
            ("researcher", self.test_researcher_agent),
            ("blueprint", self.test_blueprint_agent),
            ("brd", lambda: self.test_brd_agent(results)),
            ("fr", lambda: self.test_fr_agent(results)),
            ("prd", lambda: self.test_prd_agent(results)),
            ("mockup", lambda: self.test_mockup_agent(results)),
            ("architecture", self.test_architecture_agent),
            ("bom", lambda: self.test_bom_agent(results)),
            ("data", lambda: self.test_data_agent(results)),
            ("proposal", lambda: self.test_proposal_agent(results)),
            ("gallery", lambda: self.test_gallery_agent(results))
        ]
        
        for agent_key, test_func in test_sequence:
            try:
                result = await test_func()
                results[agent_key] = result
                self.test_results.append(result)
                
                # Stop on critical failures
                if result["status"] in ["failed", "exception"] and agent_key in ["storage", "intake", "blueprint"]:
                    print(f"🛑 Critical agent {agent_key} failed, stopping test sequence")
                    break
                    
            except Exception as e:
                print(f"💥 Test function for {agent_key} failed: {str(e)}")
                results[agent_key] = {
                    "agent": agent_key,
                    "status": "test_exception",
                    "execution_time": 0,
                    "message": "Test function exception",
                    "data": None,
                    "error": str(e)
                }
        
        overall_time = time.time() - overall_start_time
        
        # Generate comprehensive report
        await self.generate_test_report(results, overall_time)
        
        return results
    
    async def generate_test_report(self, results: dict, overall_time: float):
        """Generate comprehensive test report"""
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("="*80)
        
        # Summary statistics
        total_agents = len(results)
        successful_agents = len([r for r in results.values() if r["status"] == "success"])
        partial_agents = len([r for r in results.values() if r["status"] == "partial_success"])
        failed_agents = len([r for r in results.values() if r["status"] in ["failed", "exception", "timeout", "test_exception"]])
        
        print(f"\n📈 SUMMARY STATISTICS:")
        print(f"   Total Agents Tested: {total_agents}")
        print(f"   ✅ Successful: {successful_agents}")
        print(f"   ⚠️  Partial Success: {partial_agents}")
        print(f"   ❌ Failed: {failed_agents}")
        print(f"   ⏱️  Total Execution Time: {overall_time:.1f} seconds")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for agent_key, result in results.items():
            status_emoji = {
                "success": "✅",
                "partial_success": "⚠️",
                "failed": "❌",
                "exception": "💥",
                "timeout": "⏰",
                "test_exception": "🧪"
            }.get(result["status"], "❓")
            
            print(f"   {status_emoji} {result['agent']}: {result['status']} ({result['execution_time']:.1f}s)")
            if result["error"]:
                print(f"      Error: {result['error']}")
            elif result["message"]:
                print(f"      Message: {result['message']}")
        
        # Performance analysis
        print(f"\n⚡ PERFORMANCE ANALYSIS:")
        execution_times = [r["execution_time"] for r in results.values() if r["execution_time"] > 0]
        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)
            max_time = max(execution_times)
            min_time = min(execution_times)
            print(f"   Average Execution Time: {avg_time:.1f}s")
            print(f"   Maximum Execution Time: {max_time:.1f}s")
            print(f"   Minimum Execution Time: {min_time:.1f}s")
        
        # Recommendations
        print(f"\n🎯 RECOMMENDATIONS:")
        if failed_agents > 0:
            print(f"   • {failed_agents} agents failed - immediate attention required")
        if partial_agents > 0:
            print(f"   • {partial_agents} agents partially successful - review output validation")
        if successful_agents == total_agents:
            print(f"   • All agents working correctly - system ready for production")
        
        # Save detailed report
        report_data = {
            "test_timestamp": datetime.now().isoformat(),
            "project_name": self.project_name,
            "overall_execution_time": overall_time,
            "summary": {
                "total_agents": total_agents,
                "successful": successful_agents,
                "partial_success": partial_agents,
                "failed": failed_agents
            },
            "detailed_results": results
        }
        
        with open(f"comprehensive_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: comprehensive_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

async def main():
    """Main testing function"""
    tester = ComprehensiveAgentTester()
    results = await tester.run_comprehensive_test()
    
    # Return success if majority of agents work
    successful_count = len([r for r in results.values() if r["status"] == "success"])
    total_count = len(results)
    
    if successful_count >= total_count * 0.8:  # 80% success rate
        print(f"\n🎉 COMPREHENSIVE TEST PASSED: {successful_count}/{total_count} agents successful")
        return True
    else:
        print(f"\n❌ COMPREHENSIVE TEST FAILED: Only {successful_count}/{total_count} agents successful")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)