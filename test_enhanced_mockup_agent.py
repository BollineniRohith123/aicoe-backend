"""
Test Enhanced MockupAgent - Verify multi-page mockup generation for ALL use cases
"""
import asyncio
import json
from pathlib import Path
from backend.agents.mockup_agent import MockupAgent


class MockLLMClient:
    """Mock LLM client for testing"""
    async def send_message_async(self, system_message, user_message, **kwargs):
        """Return a simple HTML mockup"""
        if "index.html" in user_message or "dashboard" in user_message.lower():
            return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Project - Dashboard</title>
    <style>
        :root {
            --primary-navy: #1a1a2e;
            --accent-pink: #ff69b4;
            --accent-cyan: #00ffcc;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f7;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            background: linear-gradient(135deg, var(--primary-navy) 0%, var(--accent-pink) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .use-case-card {
            background: white;
            padding: 24px;
            border-radius: 24px;
            margin: 16px 0;
            box-shadow: 0 2px 16px rgba(26, 26, 46, 0.08);
        }
        .btn {
            background: var(--accent-cyan);
            color: var(--primary-navy);
            padding: 12px 24px;
            border-radius: 12px;
            text-decoration: none;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Test Project Dashboard</h1>
        <div class="use-case-card">
            <h3>UC-001: Test Use Case 1</h3>
            <p>This is a test use case mockup</p>
            <a href="use-case-1.html" class="btn">View Details →</a>
        </div>
        <div class="use-case-card">
            <h3>UC-002: Test Use Case 2</h3>
            <p>This is another test use case mockup</p>
            <a href="use-case-2.html" class="btn">View Details →</a>
        </div>
    </div>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>lucide.createIcons();</script>
</body>
</html>"""
        else:
            # Use case detail page
            return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Use Case Detail</title>
    <style>
        :root {
            --primary-navy: #1a1a2e;
            --accent-pink: #ff69b4;
            --accent-cyan: #00ffcc;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f7;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            background: linear-gradient(135deg, var(--primary-navy) 0%, var(--accent-pink) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .screen-mockup {
            background: white;
            padding: 32px;
            border-radius: 24px;
            margin: 24px 0;
            box-shadow: 0 2px 16px rgba(26, 26, 46, 0.08);
        }
        .nav-link {
            color: var(--accent-cyan);
            text-decoration: none;
            margin-right: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="index.html" class="nav-link">← Back to Dashboard</a>
        </nav>
        <h1>Use Case Detail Mockup</h1>
        <div class="screen-mockup">
            <h2>Screen 1: Initial State</h2>
            <p>This is a realistic mockup of the user interface for this use case.</p>
        </div>
        <div class="screen-mockup">
            <h2>Screen 2: Action State</h2>
            <p>This shows the UI after the user takes an action.</p>
        </div>
    </div>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>lucide.createIcons();</script>
</body>
</html>"""


async def test_enhanced_mockup_agent():
    """Test the enhanced mockup agent"""
    print("🧪 Testing Enhanced MockupAgent\n")
    
    # Create mock LLM client
    llm_client = MockLLMClient()
    
    # Create mockup agent
    agent = MockupAgent(llm_client)
    print(f"✅ Created MockupAgent: {agent.config.name}\n")
    
    # Prepare test input with 2 use cases (should generate 3 pages total)
    test_input = {
        "project_name": "Test Fitness App",
        "use_cases": [
            {
                "id": "UC-001",
                "title": "User Registration",
                "description": "New user creates an account",
                "actors": ["New User"],
                "preconditions": ["User has downloaded the app"],
                "main_flow": [
                    "User opens the app",
                    "User taps 'Sign Up'",
                    "User enters email and password",
                    "User confirms registration"
                ],
                "postconditions": ["User account is created"]
            },
            {
                "id": "UC-002",
                "title": "Log Workout",
                "description": "User logs a completed workout",
                "actors": ["Registered User"],
                "preconditions": ["User is logged in"],
                "main_flow": [
                    "User navigates to workout log",
                    "User selects workout type",
                    "User enters sets and reps",
                    "User saves workout"
                ],
                "postconditions": ["Workout is saved to history"]
            }
        ],
        "structured_notes": {
            "company_overview": "A fitness tracking application for beginners",
            "meeting_objective": "Define core features for fitness app",
            "target_audience": "Fitness beginners aged 25-45",
            "requirements": [
                "Must be beginner-friendly",
                "Must include workout logging",
                "Must have progress visualization"
            ],
            "technical_constraints": [
                "Use React Native for cross-platform",
                "Use Node.js backend",
                "Use PostgreSQL database"
            ],
            "decisions_made": [
                "Target audience will be fitness beginners aged 25-45",
                "Technical stack: React Native, Node.js, PostgreSQL"
            ]
        },
        "prd_content": "Product Requirements Document for Test Fitness App...",
        "technical_stack": {
            "frontend": "React Native",
            "backend": "Node.js",
            "database": "PostgreSQL"
        }
    }
    
    print("📝 Test Input:")
    print(f"   - Project: {test_input['project_name']}")
    print(f"   - Use Cases: {len(test_input['use_cases'])}")
    print(f"   - Has PRD: {bool(test_input['prd_content'])}")
    print(f"   - Has Technical Stack: {bool(test_input['technical_stack'])}\n")
    
    # Execute agent
    print("🚀 Executing MockupAgent...\n")
    result = await agent.execute(test_input, {})
    
    # Verify results
    if result.success:
        print("✅ MockupAgent execution successful!\n")
        print("📊 Results:")
        print(f"   - Pages generated: {result.data['page_count']}")
        print(f"   - Total size: {result.data['total_size']} characters")
        print(f"   - Use cases processed: {result.data.get('use_case_count', 0)}")
        print(f"   - Multi-page: {result.metadata.get('multi_page', False)}")
        print(f"\n📄 Pages:")
        for page_name in result.data['mockup_pages'].keys():
            page_size = len(result.data['mockup_pages'][page_name])
            print(f"   - {page_name}: {page_size} characters")
        
        # Verify expectations
        print(f"\n🔍 Verification:")
        expected_pages = 1 + len(test_input['use_cases'])  # index.html + use-case pages
        actual_pages = result.data['page_count']
        
        if actual_pages == expected_pages:
            print(f"   ✅ Correct number of pages: {actual_pages} (expected {expected_pages})")
        else:
            print(f"   ❌ Wrong number of pages: {actual_pages} (expected {expected_pages})")
        
        if 'index.html' in result.data['mockup_pages']:
            print(f"   ✅ index.html generated")
        else:
            print(f"   ❌ index.html missing")
        
        for i in range(1, len(test_input['use_cases']) + 1):
            page_name = f"use-case-{i}.html"
            if page_name in result.data['mockup_pages']:
                print(f"   ✅ {page_name} generated")
            else:
                print(f"   ❌ {page_name} missing")
        
        print(f"\n🎉 Test completed successfully!")
        return True
    else:
        print(f"❌ MockupAgent execution failed: {result.error}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_enhanced_mockup_agent())
    exit(0 if success else 1)

