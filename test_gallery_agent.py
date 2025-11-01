"""
Test script for Case Study Gallery Agent
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from agents.gallery_agent import CaseStudyGalleryAgent
from agents.base_agent import AgentResult


class MockLLMClient:
    """Mock LLM client for testing"""
    async def send_message_async(self, user_message, system_message, temperature, max_tokens):
        """Return a mock HTML response"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AICOE Case Study Gallery</title>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {
            --aicoe-primary: #0066cc;
            --aicoe-accent: #00d9ff;
            --aicoe-dark: #1d1d1f;
            --aicoe-gray: #6e6e73;
            --aicoe-light-gray: #f5f5f7;
            --aicoe-white: #ffffff;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--aicoe-light-gray);
            color: var(--aicoe-dark);
        }
        nav {
            background: var(--aicoe-white);
            padding: 1rem 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav-brand {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--aicoe-primary);
        }
        .hero {
            background: linear-gradient(135deg, var(--aicoe-primary), var(--aicoe-accent));
            color: var(--aicoe-white);
            padding: 4rem 2rem;
            text-align: center;
        }
        .hero h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .hero p {
            font-size: 1.25rem;
            opacity: 0.9;
        }
        .filters {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }
        .filter-group {
            flex: 1;
            min-width: 200px;
        }
        .filter-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: var(--aicoe-gray);
        }
        .filter-group select,
        .filter-group input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
        }
        .gallery {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
        }
        .case-study-card {
            background: var(--aicoe-white);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .case-study-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        }
        .industry-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            background: var(--aicoe-primary);
            color: var(--aicoe-white);
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .card-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--aicoe-dark);
        }
        .card-description {
            color: var(--aicoe-gray);
            margin-bottom: 1rem;
            line-height: 1.6;
        }
        .tech-stack {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        .tech-tag {
            padding: 0.25rem 0.75rem;
            background: var(--aicoe-light-gray);
            color: var(--aicoe-gray);
            border-radius: 12px;
            font-size: 0.875rem;
        }
        .card-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
        }
        .view-button {
            padding: 0.75rem 1.5rem;
            background: var(--aicoe-primary);
            color: var(--aicoe-white);
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .view-button:hover {
            background: #0052a3;
        }
    </style>
</head>
<body>
    <nav>
        <div class="nav-container">
            <div class="nav-brand">AICOE Case Study Gallery</div>
        </div>
    </nav>
    
    <div class="hero">
        <h1>Case Study Gallery</h1>
        <p>Explore our collection of AI-powered project mockups</p>
    </div>
    
    <div class="filters">
        <div class="filter-group">
            <label>Industry</label>
            <select id="industryFilter">
                <option value="">All Industries</option>
            </select>
        </div>
        <div class="filter-group">
            <label>Technology</label>
            <select id="techFilter">
                <option value="">All Technologies</option>
            </select>
        </div>
        <div class="filter-group">
            <label>Search</label>
            <input type="text" id="searchInput" placeholder="Search projects...">
        </div>
    </div>
    
    <div class="gallery" id="gallery"></div>
    
    <script>
        lucide.createIcons();
    </script>
</body>
</html>'''


async def test_gallery_agent():
    """Test the gallery agent"""
    print("=" * 80)
    print("TESTING CASE STUDY GALLERY AGENT")
    print("=" * 80)
    
    # Create mock LLM client
    llm_client = MockLLMClient()
    
    # Create gallery agent
    print("\n1. Creating CaseStudyGalleryAgent...")
    agent = CaseStudyGalleryAgent(llm_client)
    print("   ✓ Agent created successfully")
    
    # Execute agent
    print("\n2. Executing gallery agent...")
    input_data = {
        "current_project_name": "Test Project",
        "force_regenerate": False
    }
    context = {}
    
    result = await agent.execute(input_data, context)
    
    # Check results
    print("\n3. Checking results...")
    if result.success:
        print("   ✓ Gallery generation successful!")
        print(f"   - Case studies found: {result.data.get('case_study_count', 0)}")
        print(f"   - Gallery path: {result.data.get('gallery_path', 'N/A')}")
        
        # Check if files were created
        import os
        gallery_path = result.data.get('gallery_path', '')
        if os.path.exists(gallery_path):
            print(f"   ✓ Gallery HTML file created: {gallery_path}")
            file_size = os.path.getsize(gallery_path)
            print(f"   - File size: {file_size:,} bytes")
        else:
            print(f"   ✗ Gallery HTML file not found: {gallery_path}")
        
        # Check gallery data
        gallery_data_path = "backend/storage/case-study-gallery/gallery-data.json"
        if os.path.exists(gallery_data_path):
            print(f"   ✓ Gallery data file created: {gallery_data_path}")
            import json
            with open(gallery_data_path, 'r') as f:
                data = json.load(f)
            print(f"   - Projects in gallery: {len(data)}")
            
            # Show first few projects
            if data:
                print("\n4. Sample case studies:")
                for i, (workflow_id, study) in enumerate(list(data.items())[:3]):
                    print(f"\n   Project {i+1}:")
                    print(f"   - Name: {study.get('project_name', 'N/A')}")
                    print(f"   - Industry: {study.get('industry', 'N/A')}")
                    print(f"   - Use Cases: {study.get('use_case_count', 0)}")
                    print(f"   - Tech Stack: {', '.join(study.get('tech_stack', []))}")
                    print(f"   - Has Mockup: {study.get('has_mockup', False)}")
        else:
            print(f"   ✗ Gallery data file not found: {gallery_data_path}")
    else:
        print(f"   ✗ Gallery generation failed: {result.error}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_gallery_agent())

