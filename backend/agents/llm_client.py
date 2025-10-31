"""
LLM Client using OpenAI SDK
Supports OpenRouter API with GLM-4.6 model
"""
import os
from typing import Optional
import asyncio
from openai import AsyncOpenAI
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Wrapper around OpenAI SDK for LLM interactions via OpenRouter
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "openrouter",
        model: str = "z-ai/glm-4.6"
    ):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided and OPENROUTER_API_KEY not found in environment")

        self.provider = provider
        self.model = model
        self.logger = logging.getLogger("llm_client")

        # Initialize OpenAI client with OpenRouter base URL
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1"
        )
    
    async def send_message_async(
        self,
        user_message: str,
        system_message: str = "You are a helpful AI assistant.",
        session_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Send a message to the LLM and get response via OpenRouter

        Args:
            user_message: The user's message
            system_message: System prompt
            session_id: Session ID for chat context (not used)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate

        Returns:
            LLM response text
        """
        try:
            self.logger.info(f"Sending message to {self.provider}/{self.model}")

            # Create messages for OpenRouter API
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]

            # Call OpenRouter API with extra headers
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                extra_headers={
                    "HTTP-Referer": "https://aicoe-platform.local",
                    "X-Title": "AICOE Automation Platform"
                }
            )

            # Extract response text
            response_text = response.choices[0].message.content

            self.logger.info(f"Received response from LLM (length: {len(response_text)} chars)")
            return response_text

        except Exception as e:
            self.logger.error(f"Error calling LLM: {str(e)}")
            raise Exception(f"LLM call failed: {str(e)}")
    
    def send_message(
        self,
        user_message: str,
        system_message: str = "You are a helpful AI assistant.",
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
