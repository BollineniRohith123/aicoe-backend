"""
LLM Client using Emergent Integrations
Supports OpenAI, Anthropic, and Gemini through Universal Key
"""
import os
from typing import Optional
import asyncio
from emergentintegrations.llm.chat import LlmChat, UserMessage
import logging

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Wrapper around emergentintegrations for LLM interactions
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "openai",
        model: str = "gpt-4o"
    ):
        self.api_key = api_key or os.getenv("EMERGENT_LLM_KEY")
        if not self.api_key:
            raise ValueError("API key not provided and EMERGENT_LLM_KEY not found in environment")
        
        self.provider = provider
        self.model = model
        self.logger = logging.getLogger("llm_client")
        
    def _create_chat(self, session_id: str, system_message: str):
        """Create a new chat instance"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=system_message
        )
        chat.with_model(self.provider, self.model)
        return chat
    
    async def send_message_async(
        self,
        user_message: str,
        system_message: str = "You are a helpful AI assistant.",
        session_id: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Send a message to the LLM and get response
        
        Args:
            user_message: The user's message
            system_message: System prompt
            session_id: Session ID for chat context
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            
        Returns:
            LLM response text
        """
        if not session_id:
            session_id = f"session_{os.urandom(8).hex()}"
        
        try:
            self.logger.info(f"Sending message to {self.provider}/{self.model}")
            
            # Create chat instance
            chat = self._create_chat(session_id, system_message)
            
            # Create user message
            message = UserMessage(text=user_message)
            
            # Send message and get response
            response = await chat.send_message(message)
            
            self.logger.info(f"Received response from LLM")
            return response
            
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
