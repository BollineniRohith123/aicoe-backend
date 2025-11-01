"""
End-to-End Test for AICOE Platform
Tests the complete workflow including enhanced MockupAgent and Gallery Agent
"""
import asyncio
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from agents.mockup_agent import MockupAgent
from agents.gallery_agent import CaseStudyGalleryAgent


class MockLLMClient:
    """Mock LLM client for testing"""
    def __init__(self):
        self.call_count = 0
    
    async def send_message_async(self, system_message, user_message, **kwargs):
        """Return realistic HTML mockups"""
        self.call_count += 1
        
        if "index.html" in user_message or "dashboard" in user_message.lower():
            return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E2E Test Project - Dashboard</title>
    <style>
        :root {
            --primary-navy: #1a1a2e;
            --accent-pink: #ff69b4;
            --accent-cyan: #00ffcc;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
            background: #f5f5f7;
            -webkit-font-smoothing: antialiased;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        h1 {
            font-size: 48px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-navy) 0%, var(--accent-pink) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 16px;
        }
        .subtitle { color: #666; font-size: 20px; margin-bottom: 40px; }
        .use-case-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 24px; }
        .use-case-card {
            background: white;
            padding: 32px;
            border-radius: 24px;
            box-shadow: 0 2px 16px rgba(26, 26, 46, 0.08);
            transition: all 0.3s ease;
        }
        .use-case-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 24px rgba(26, 26, 46, 0.12);
        }
        .use-case-id { color: var(--accent-cyan); font-weight: 600; font-size: 14px; margin-bottom: 8px; }
        .use-case-title { font-size: 24px; font-weight: 600; color: var(--primary-navy); margin-bottom: 12px; }
        .use-case-desc { color: #666; line-height: 1.6; margin-bottom: 20px; }
        .btn {
            display: inline-block;
            background: var(--accent-cyan);
            color: var(--primary-navy);
            padding: 12px 24px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .btn:hover { background: var(--accent-pink); color: white; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 E2E Test Project</h1>
        <p class="subtitle">Comprehensive end-to-end testing of AICOE platform</p>
        
        <div class="use-case-grid">
            <div class="use-case-card">
                <div class="use-case-id">UC-001</div>
                <h3 class="use-case-title">User Registration</h3>
                <p class="use-case-desc">New user creates an account and sets up their profile</p>
                <a href="use-case-1.html" class="btn">View Mockup →</a>
            </div>
            
            <div class="use-case-card">
                <div class="use-case-id">UC-002</div>
                <h3 class="use-case-title">Dashboard Overview</h3>
                <p class="use-case-desc">User views their personalized dashboard with key metrics</p>
                <a href="use-case-2.html" class="btn">View Mockup →</a>
            </div>
        </div>
    </div>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>lucide.createIcons();</script>
</body>
</html>"""
        else:
            # Use case detail page with realistic UI mockups
            return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Use Case Mockup</title>
    <style>
        :root {
            --primary-navy: #1a1a2e;
            --accent-pink: #ff69b4;
            --accent-cyan: #00ffcc;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif;
            background: #f5f5f7;
            -webkit-font-smoothing: antialiased;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 40px 20px; }
        nav { margin-bottom: 32px; }
        .nav-link {
            color: var(--accent-cyan);
            text-decoration: none;
            font-weight: 600;
            margin-right: 20px;
        }
        h1 {
            font-size: 40px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-navy) 0%, var(--accent-pink) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 32px;
        }
        .screen-mockup {
            background: white;
            padding: 40px;
            border-radius: 24px;
            box-shadow: 0 2px 16px rgba(26, 26, 46, 0.08);
            margin-bottom: 32px;
        }
        .screen-title { font-size: 24px; font-weight: 600; color: var(--primary-navy); margin-bottom: 16px; }
        .screen-content { color: #666; line-height: 1.8; }
        .ui-element {
            background: #f5f5f7;
            padding: 16px;
            border-radius: 12px;
            margin: 16px 0;
            border: 2px solid #e0e0e0;
        }
        .form-field {
            margin: 12px 0;
            padding: 12px;
            border: 1px solid #d0d0d0;
            border-radius: 8px;
            background: white;
        }
        .button-primary {
            background: var(--accent-cyan);
            color: var(--primary-navy);
            padding: 14px 28px;
            border-radius: 12px;
            border: none;
            font-weight: 600;
            cursor: pointer;
            display: inline-block;
            margin-top: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <nav>
            <a href="index.html" class="nav-link">← Back to Dashboard</a>
        </nav>
        
        <h1>Use Case: Realistic UI Mockup</h1>
        
        <div class="screen-mockup">
            <h2 class="screen-title">📱 Screen 1: Initial State</h2>
            <div class="screen-content">
                <p>This is a realistic mockup showing the actual user interface:</p>
                <div class="ui-element">
                    <div class="form-field">Email: user@example.com</div>
                    <div class="form-field">Password: ••••••••</div>
                    <button class="button-primary">Sign In</button>
                </div>
            </div>
        </div>
        
        <div class="screen-mockup">
            <h2 class="screen-title">✅ Screen 2: Success State</h2>
            <div class="screen-content">
                <p>After successful action, the UI updates to show:</p>
                <div class="ui-element">
                    <p style="color: #00cc99; font-weight: 600;">✓ Action completed successfully!</p>
                    <p>You can now proceed to the next step.</p>
                </div>
            </div>
        </div>
    </div>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>lucide.createIcons();</script>
</body>
</html>"""


async def test_mockup_agent():
    """Test MockupAgent with enhanced features"""
    print("\n" + "="*80)
    print("🧪 TEST 1: ENHANCED MOCKUP AGENT")
    print("="*80 + "\n")
    
    llm_client = MockLLMClient()
    agent = MockupAgent(llm_client)
    
    test_input = {
        "project_name": "E2E Test Project",
        "use_cases": [
            {
                "id": "UC-001",
                "title": "User Registration",
                "description": "New user creates an account",
                "actors": ["New User"],
                "main_flow": ["Open app", "Enter details", "Submit", "Verify email"]
            },
            {
                "id": "UC-002",
                "title": "Dashboard Overview",
                "description": "User views dashboard",
                "actors": ["Registered User"],
                "main_flow": ["Login", "View metrics", "Check notifications"]
            }
        ],
        "structured_notes": {
            "company_overview": "E2E testing platform",
            "meeting_objective": "Test all features",
            "requirements": ["Must be comprehensive", "Must be realistic"]
        },
        "prd_content": "Test PRD content",
        "technical_stack": {"frontend": "React", "backend": "Node.js"}
    }
    
    print(f"📝 Input: {test_input['project_name']}")
    print(f"   Use Cases: {len(test_input['use_cases'])}")
    print(f"   Expected Pages: {1 + len(test_input['use_cases'])}\n")
    
    result = await agent.execute(test_input, {})
    
    if result.success:
        print(f"✅ MockupAgent SUCCESS")
        print(f"   Pages Generated: {result.data['page_count']}")
        print(f"   Total Size: {result.data['total_size']:,} characters")
        print(f"   LLM Calls: {llm_client.call_count}")
        
        for page_name in result.data['mockup_pages'].keys():
            size = len(result.data['mockup_pages'][page_name])
            print(f"   ✓ {page_name}: {size:,} characters")
        
        return True
    else:
        print(f"❌ MockupAgent FAILED: {result.error}")
        return False


async def test_gallery_agent():
    """Test Gallery Agent"""
    print("\n" + "="*80)
    print("🧪 TEST 2: CASE STUDY GALLERY AGENT")
    print("="*80 + "\n")
    
    llm_client = MockLLMClient()
    agent = CaseStudyGalleryAgent(llm_client)
    
    print(f"📝 Scanning existing projects in backend/storage/\n")
    
    result = await agent.execute({}, {})
    
    if result.success:
        print(f"✅ GalleryAgent SUCCESS")
        print(f"   Case Studies Found: {result.data.get('case_study_count', 0)}")
        print(f"   Gallery HTML Size: {result.data.get('gallery_size', 0):,} characters")
        print(f"   Gallery Location: {result.data.get('gallery_path', 'N/A')}")
        
        return True
    else:
        print(f"❌ GalleryAgent FAILED: {result.error}")
        return False


async def main():
    """Run all end-to-end tests"""
    print("\n" + "🚀 " * 20)
    print("AICOE PLATFORM - COMPREHENSIVE END-TO-END TEST")
    print("🚀 " * 20)
    
    results = []
    
    # Test 1: MockupAgent
    results.append(await test_mockup_agent())
    
    # Test 2: GalleryAgent
    results.append(await test_gallery_agent())
    
    # Summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY")
    print("="*80 + "\n")
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Platform is working correctly.\n")
        return True
    else:
        print("⚠️  Some tests failed. Please review the errors above.\n")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

