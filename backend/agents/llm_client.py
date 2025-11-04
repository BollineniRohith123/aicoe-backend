"""
LLM Client using OpenAI SDK
Supports Synthetic API with agent-specific models
"""

import os
from typing import Optional
import asyncio
from openai import AsyncOpenAI
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Wrapper around OpenAI SDK for LLM interactions via Synthetic API
    Supports agent-specific model configuration
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "synthetic",
        model: str = "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct",
    ):
        self.api_key = (
            api_key or os.getenv("SYNTHETIC_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        )
        if not self.api_key:
            raise ValueError(
                "API key not provided and SYNTHETIC_API_KEY or OPENROUTER_API_KEY not found in environment"
            )

        self.provider = provider
        self.model = model
        self.logger = logging.getLogger("llm_client")

        # Initialize OpenAI client with Synthetic base URL
        self.client = AsyncOpenAI(
            api_key=self.api_key, base_url="https://api.synthetic.new/openai/v1"
        )

        # Load agent-specific models from environment variables
        self.agent_models = {
            "storage": os.getenv(
                "STORAGE_AGENT_MODEL", "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
            ),
            "transcript": os.getenv(
                "TRANSCRIPT_AGENT_MODEL", "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
            ),
            "researcher": os.getenv(
                "RESEARCHER_AGENT_MODEL", "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
            ),
            "requirements": os.getenv(
                "REQUIREMENTS_AGENT_MODEL", "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
            ),
            "knowledge_base": os.getenv(
                "KNOWLEDGE_BASE_AGENT_MODEL", "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
            ),
            "prd": os.getenv(
                "PRD_AGENT_MODEL", "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
            ),
            "mockup": os.getenv(
                "MOCKUP_AGENT_MODEL", "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
            ),
            "synthetic_data": os.getenv(
                "SYNTHETIC_DATA_AGENT_MODEL", "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
            ),
            "commercial_proposal": os.getenv(
                "COMMERCIAL_PROPOSAL_AGENT_MODEL",
                "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct",
            ),
            "bom": os.getenv(
                "BOM_AGENT_MODEL", "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
            ),
            "architecture_diagram": os.getenv(
                "ARCHITECTURE_DIAGRAM_AGENT_MODEL",
                "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct",
            ),
            "reviewer": os.getenv(
                "REVIEWER_AGENT_MODEL", "hf:Qwen/Qwen3-Coder-480B-A35B-Instruct"
            ),
        }

    async def send_message_async(
        self,
        user_message: str,
        system_message: str = "You are a helpful AI assistant.",
        session_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
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
            # ENHANCED LOGGING: Track every API call with detailed context
            import traceback
            import inspect

            # Get caller information for debugging
            frame = inspect.currentframe()
            caller_frame = frame.f_back
            caller_info = f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno}"

            self.logger.info(
                f"🔵 API CALL START | Model: {self.provider}/{self.model} | Caller: {caller_info}"
            )
            self.logger.info(
                f"   Request: temp={temperature}, max_tokens={max_tokens}, msg_length={len(user_message)}"
            )

            # Create messages for OpenRouter API
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]

            # Determine model to use (agent-specific or default)
            agent_name = getattr(self, "_current_agent", None)
            model_to_use = (
                self.agent_models.get(agent_name, self.model)
                if agent_name
                else self.model
            )

            self.logger.info(
                f"🔵 API CALL START | Model: {self.provider}/{model_to_use} | Agent: {agent_name or 'default'}"
            )

            # Call Synthetic API
            response = await self.client.chat.completions.create(
                model=model_to_use,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
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
                    f"🟢 API CALL SUCCESS | Response: {len(response_text)} chars | Tokens: {prompt_tokens}+{completion_tokens}={total_tokens}"
                )
            else:
                self.logger.info(
                    f"🟢 API CALL SUCCESS | Response: {len(response_text)} chars"
                )

            return response_text

        except Exception as e:
            self.logger.error(f"🔴 API CALL FAILED | Error: {str(e)}")
            raise Exception(f"LLM call failed: {str(e)}")

    def set_current_agent(self, agent_name: str):
        """
        Set the current agent name to use agent-specific model
        """
        self._current_agent = agent_name

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
