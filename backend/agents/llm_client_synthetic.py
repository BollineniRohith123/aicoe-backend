"""
Synthetic LLM Client using GLM-4.6 via Synthetic API
For production use with MiniMax M2 model
"""

import os
from typing import Optional
import asyncio
import openai
import logging

logger = logging.getLogger(__name__)


class SyntheticLLMClient:
    """
    Wrapper around OpenAI SDK for Synthetic API interactions
    Uses GLM-4.6 model via Synthetic API
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "hf:zai-org/GLM-4.6",
    ):
        self.api_key = api_key or os.getenv("SYNTHETIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not provided and SYNTHETIC_API_KEY not found in environment"
            )

        self.model = model
        self.logger = logging.getLogger("synthetic_llm_client")

        # Initialize OpenAI client with Synthetic API base URL
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://api.glhf.chat/v1/",
        )

    async def send_message_async(
        self,
        user_message: str,
        system_message: str = "You are a helpful AI assistant.",
        session_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = None,
    ) -> str:
        """
        Send a message to the LLM and get response via Synthetic API

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
            # Apply default token limit if not provided
            effective_max_tokens = max_tokens or int(os.getenv("SYNTHETIC_MAX_TOKENS", "16000"))
            
            self.logger.info(
                f"🔵 SYNTHETIC API CALL START | Model: {self.model} | Temp: {temperature} | Max tokens: {effective_max_tokens}"
            )

            # Create messages for Synthetic API
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]

            # Call Synthetic API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=effective_max_tokens,
            )

            # Extract response text
            response_text = response.choices[0].message.content

            # Calculate token usage if available
            usage = getattr(response, "usage", None)
            if usage:
                prompt_tokens = getattr(usage, "prompt_tokens", 0)
                completion_tokens = getattr(usage, "completion_tokens", 0)
                total_tokens = getattr(usage, "total_tokens", 0)
                self.logger.info(
                    f"🟢 SYNTHETIC API CALL SUCCESS | Response: {len(response_text)} chars | Tokens: {prompt_tokens}+{completion_tokens}={total_tokens}"
                )
            else:
                self.logger.info(
                    f"🟢 SYNTHETIC API CALL SUCCESS | Response: {len(response_text)} chars"
                )

            return response_text

        except Exception as e:
            self.logger.error(f"🔴 SYNTHETIC API CALL FAILED | Error: {str(e)}")
            raise Exception(f"Synthetic LLM call failed: {str(e)}")

    def send_message(
        self,
        user_message: str,
        system_message: str = "You are a helpful AI assistant.",
        session_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
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
                max_tokens=max_tokens,
            )
        )

    def set_current_agent(self, agent_name: str):
        """
        Set the current agent name (for compatibility with base agent)
        """
        self._current_agent = agent_name