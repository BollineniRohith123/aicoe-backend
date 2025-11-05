"""
Gemini LLM Client for Research Agent
Uses Google Gemini API for research and web search capabilities
"""

import os
import json
import asyncio
import aiohttp
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class GeminiLLMClient:
    """
    Gemini LLM Client specifically for research agent
    Provides web search and research capabilities using Google Gemini API
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not provided and GEMINI_API_KEY not found in environment")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-1.5-flash"  # Using Flash for faster responses
        self.logger = logging.getLogger("gemini_llm_client")
        self.logger.info(f"🔧 Gemini LLM Client initialized with API key: {self.api_key[:10]}...")

    async def send_message_async(
        self,
        user_message: str,
        system_message: str = "You are a helpful research assistant.",
        session_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Send a message to Gemini API and get response
        """
        try:
            self.logger.info(f"🔵 GEMINI API CALL | msg_length={len(user_message)}")
            
            # Prepare the request
            url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
            
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"{system_message}\n\n{user_message}"
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                    "topP": 0.8,
                    "topK": 40
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Extract the response text
                        if "candidates" in result and len(result["candidates"]) > 0:
                            candidate = result["candidates"][0]
                            if "content" in candidate and "parts" in candidate["content"]:
                                response_text = candidate["content"]["parts"][0]["text"]
                                self.logger.info(f"🟢 GEMINI API SUCCESS | Response: {len(response_text)} chars")
                                return response_text
                            else:
                                raise Exception("Invalid response structure from Gemini API")
                        else:
                            raise Exception("No candidates in response from Gemini API")
                    else:
                        error_text = await response.text()
                        self.logger.error(f"🔴 GEMINI API FAILED | Status: {response.status} | Error: {error_text}")
                        raise Exception(f"Gemini API call failed with status {response.status}: {error_text}")
                        
        except Exception as e:
            self.logger.error(f"🔴 GEMINI API ERROR | {str(e)}")
            raise Exception(f"Gemini LLM call failed: {str(e)}")

    def set_current_agent(self, agent_name: str):
        """Set the current agent for context-aware responses"""
        self.logger.info(f"🔧 GEMINI: Set current agent to: {agent_name}")

    def send_message(
        self,
        user_message: str,
        system_message: str = "You are a helpful research assistant.",
        session_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Synchronous wrapper for send_message_async
        """
        return asyncio.run(
            self.send_message_async(
                user_message=user_message,
                system_message=system_message,
                session_id=session_id,
                temperature=temperature,
                max_tokens=max_tokens
            )
        )

    async def research_web_search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Perform web research using Gemini's capabilities
        This simulates web search by asking Gemini to research the topic
        """
        research_prompt = f"""
        Research the following topic comprehensively: "{query}"
        
        Please provide:
        1. Key industry trends and insights
        2. Competitor analysis and best practices
        3. Technical standards and requirements
        4. User expectations and market demands
        5. Regulatory considerations
        6. Implementation recommendations
        
        Format your response as structured JSON with the following keys:
        - industry_trends: array of trend descriptions
        - competitor_insights: array of competitor analysis
        - technical_standards: array of technical requirements
        - user_expectations: array of user needs
        - regulatory_requirements: array of compliance needs
        - implementation_recommendations: array of recommendations
        """
        
        try:
            response = await self.send_message_async(
                user_message=research_prompt,
                system_message="You are an expert research analyst. Provide comprehensive, accurate research findings in JSON format.",
                temperature=0.3,  # Lower temperature for more factual responses
                max_tokens=8000
            )
            
            # Try to parse as JSON
            try:
                research_data = json.loads(response)
                self.logger.info(f"🟢 RESEARCH SUCCESS | Query: {query} | Data keys: {list(research_data.keys())}")
                return research_data
            except json.JSONDecodeError:
                # If not valid JSON, wrap in a structured format
                self.logger.warning("Research response not valid JSON, wrapping in structure")
                return {
                    "research_summary": response,
                    "query": query,
                    "raw_response": response
                }
                
        except Exception as e:
            self.logger.error(f"🔴 RESEARCH FAILED | Query: {query} | Error: {str(e)}")
            return {
                "error": str(e),
                "query": query,
                "research_summary": f"Research failed for query: {query}"
            }

    def generate_content(self, prompt: str) -> 'GeminiResponse':
        """
        Generate content using Gemini (for compatibility with other agents)
        """
        class GeminiResponse:
            def __init__(self, text):
                self.text = text
        
        response_text = self.send_message(prompt)
        return GeminiResponse(response_text)


# Global instance for research agent
gemini_client = GeminiLLMClient()