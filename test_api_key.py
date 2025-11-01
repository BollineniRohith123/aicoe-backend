#!/usr/bin/env python3
"""
Simple test to validate OpenRouter API key and check available models
"""
import asyncio
import aiohttp
import json
import os

async def test_api_key():
    """Test if the API key is valid by checking available models"""
    api_key = "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"
    
    print(f"🔑 Testing API Key: {api_key[:15]}...{api_key[-10:]}")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "AICOE-Platform/1.0"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test 1: Get available models
            print("\n1. Testing /models endpoint...")
            async with session.get(
                "https://openrouter.ai/api/v1/models",
                headers=headers
            ) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    models = data.get('data', [])
                    print(f"✅ Found {len(models)} available models")
                    
                    # Show some popular models
                    grok_models = [m for m in models if 'grok' in m.get('id', '').lower()]
                    if grok_models:
                        print("🤖 Available Grok models:")
                        for model in grok_models[:3]:
                            print(f"   - {model['id']}")
                    
                else:
                    error_text = await response.text()
                    print(f"❌ Models endpoint failed: {error_text}")
                    return False
            
            # Test 2: Simple chat completion
            print("\n2. Testing chat completion...")
            # Try a free model first
            payload = {
                "model": "meta-llama/llama-3.2-3b-instruct:free",
                "messages": [
                    {"role": "user", "content": "Say 'Hello from OpenRouter!' if this works."}
                ],
                "max_tokens": 50,
                "temperature": 0.1
            }
            
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=payload,
                headers=headers
            ) as response:
                print(f"Status: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    message = data['choices'][0]['message']['content']
                    print(f"✅ Response: {message}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Chat completion failed: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api_key())
    print(f"\n{'✅ API Key is valid!' if success else '❌ API Key validation failed'}")