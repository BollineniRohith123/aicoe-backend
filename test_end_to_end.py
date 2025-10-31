#!/usr/bin/env python3
"""
End-to-End Test Script for AICOE Multi-Agent Platform
Tests the complete workflow with a messy meeting transcript
"""
import asyncio
import aiohttp
import json
import time
from pathlib import Path

API_BASE_URL = "http://localhost:8000/api"

async def test_workflow():
    """Test the complete workflow"""
    print("=" * 80)
    print("AICOE MULTI-AGENT PLATFORM - END-TO-END TEST")
    print("=" * 80)
    print()
    
    # Read the test transcript
    transcript_file = Path("test_transcript_messy.txt")
    if not transcript_file.exists():
        print("❌ Error: test_transcript_messy.txt not found!")
        return
    
    with open(transcript_file, 'r') as f:
        transcript_content = f.read()
    
    print(f"✅ Loaded test transcript ({len(transcript_content)} characters)")
    print()
    
    # Prepare the request
    project_name = "Fitness Tracking App - E2E Test"
    workflow_data = {
        "project_name": project_name,
        "transcript": transcript_content,
        "workflow_type": "full"
    }
    
    print(f"📋 Project Name: {project_name}")
    print(f"📝 Transcript Length: {len(transcript_content)} characters")
    print(f"🔄 Workflow Type: full (12 agents)")
    print()
    print("=" * 80)
    print("STARTING WORKFLOW...")
    print("=" * 80)
    print()
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Start the workflow
        async with session.post(
            f"{API_BASE_URL}/process-transcript",
            json=workflow_data
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                print(f"❌ Error starting workflow: {error_text}")
                return
            
            result = await response.json()
            workflow_id = result.get("workflow_id")
            project_id = result.get("project_id")
            
            print(f"✅ Workflow started successfully!")
            print(f"   Workflow ID: {workflow_id}")
            print(f"   Project ID: {project_id}")
            print()
        
        # Monitor progress via WebSocket
        print("🔍 Monitoring agent progress...")
        print("-" * 80)

        agent_statuses = {}
        completed_agents = set()

        async with session.ws_connect(
            f"ws://localhost:8000/api/ws/{workflow_id}"
        ) as ws:
            # Send start message to begin workflow
            await ws.send_json({
                "action": "start",
                "project_name": project_name,
                "transcript": transcript_content
            })

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    
                    if data.get("type") == "agent_update":
                        agent_name = data.get("agent")
                        status = data.get("status")
                        message = data.get("message", "")
                        
                        # Track agent status
                        agent_statuses[agent_name] = status
                        
                        # Print status update
                        status_icon = {
                            "running": "🔄",
                            "completed": "✅",
                            "failed": "❌"
                        }.get(status, "⏳")
                        
                        print(f"{status_icon} {agent_name.upper()}: {status} - {message}")
                        
                        if status == "completed" and agent_name not in completed_agents:
                            completed_agents.add(agent_name)
                    
                    elif data.get("type") == "workflow_complete":
                        print()
                        print("=" * 80)
                        print("✅ WORKFLOW COMPLETED SUCCESSFULLY!")
                        print("=" * 80)
                        break
                    
                    elif data.get("type") == "error":
                        print()
                        print("=" * 80)
                        print(f"❌ WORKFLOW ERROR: {data.get('message')}")
                        print("=" * 80)
                        break
                
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print(f"❌ WebSocket error: {ws.exception()}")
                    break
    
    end_time = time.time()
    duration = end_time - start_time
    
    print()
    print("=" * 80)
    print("WORKFLOW SUMMARY")
    print("=" * 80)
    print(f"⏱️  Total Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
    print(f"🤖 Agents Completed: {len(completed_agents)}/12")
    print()
    
    # List completed agents
    print("Completed Agents:")
    for agent in sorted(completed_agents):
        print(f"  ✅ {agent}")
    print()
    
    # Check for generated files
    print("=" * 80)
    print("CHECKING GENERATED DELIVERABLES...")
    print("=" * 80)
    print()
    
    project_dir = Path(f"backend/projects/{project_name}")
    if project_dir.exists():
        print(f"✅ Project directory exists: {project_dir}")
        print()
        
        # Check for specific deliverables
        deliverables = {
            "PRD (Markdown)": project_dir / "PRDDocuments" / "PRD_v1.md",
            "PRD (PDF)": project_dir / "PRDDocuments" / "PRD_v1.pdf",
            "Mockup (index.html)": project_dir / "HTML" / "Version1" / "Mockups" / "index.html",
            "Commercial Proposal (MD)": project_dir / "CommercialProposals" / "proposal_v1.md",
            "Commercial Proposal (PDF)": project_dir / "CommercialProposals" / "proposal_v1.pdf",
            "BOM (JSON)": project_dir / "BillOfMaterials" / "bom_v1.json",
            "BOM (PDF)": project_dir / "BillOfMaterials" / "bom_v1.pdf",
            "Architecture Diagram": project_dir / "SystemArchitecture" / "architecture_diagram_v1.html",
            "Research Insights": project_dir / "ResearchFindings" / "research_insights.json",
            "Use Cases": project_dir / "UseCases" / "use_cases.json",
            "Synthetic Data": project_dir / "SyntheticData" / "demo_data.json",
        }
        
        for name, path in deliverables.items():
            if path.exists():
                size = path.stat().st_size
                print(f"  ✅ {name}: {size:,} bytes")
            else:
                print(f"  ❌ {name}: NOT FOUND")
        
        print()
        
        # Check for additional mockup pages
        mockup_dir = project_dir / "HTML" / "Version1" / "Mockups"
        if mockup_dir.exists():
            html_files = list(mockup_dir.glob("*.html"))
            if len(html_files) > 1:
                print(f"📄 Additional Mockup Pages ({len(html_files) - 1}):")
                for html_file in html_files:
                    if html_file.name != "index.html":
                        print(f"  ✅ {html_file.name}")
                print()
    else:
        print(f"❌ Project directory not found: {project_dir}")
        print()
    
    print("=" * 80)
    print("TEST COMPLETE!")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Navigate to the Results page")
    print("3. Verify all deliverables are displayed correctly")
    print("4. Test all download buttons")
    print("5. Check that mockup pages have proper navigation")
    print()

if __name__ == "__main__":
    asyncio.run(test_workflow())

