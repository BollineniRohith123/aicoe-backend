"""
Base Agent Class for AICOE Multi-Agent System
Inspired by Google ADK architecture
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)


class AgentConfig:
    """Configuration for an agent"""

    def __init__(
        self,
        name: str,
        description: str,
        model: str = "x-ai/grok-code-fast-1",  # GLM-4.6 via OpenRouter
        temperature: float = 0.7,
        max_tokens: int = 4000,
        timeout: int = 120,
    ):
        self.name = name
        self.description = description
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout


class AgentResult:
    """Result from an agent execution"""

    def __init__(
        self,
        success: bool,
        data: Any,
        error: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ):
        self.success = success
        self.data = data
        self.error = error
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()


class BaseAgent(ABC):
    """
    Base class for all agents in the AICOE platform
    Follows Google ADK principles for agent design
    """

    def __init__(self, config: AgentConfig, llm_client, workflow_context=None):
        self.config = config
        self.llm_client = llm_client
        self.workflow_context = workflow_context  # NEW: Shared workflow context
        self.logger = logging.getLogger(f"agent.{config.name}")

    @abstractmethod
    async def execute(
        self, input_data: Dict[str, Any], context: Dict[str, Any]
    ) -> AgentResult:
        """
        Execute the agent's main logic

        Args:
            input_data: Input data for the agent
            context: Shared context across agents (project info, previous results, etc.)

        Returns:
            AgentResult with success status and output data
        """
        pass

    async def _call_llm(
        self,
        system_message: str,
        user_message: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 3,
    ) -> str:
        """
        Call the LLM with given messages with automatic retry logic

        Args:
            system_message: System prompt
            user_message: User message
            temperature: Temperature for generation (defaults to agent config)
            max_tokens: Maximum tokens to generate (defaults to agent config)
            max_retries: Maximum number of retry attempts

        Returns:
            LLM response text
        """
        temp = temperature if temperature is not None else self.config.temperature
        tokens = max_tokens if max_tokens is not None else self.config.max_tokens

        # Set current agent for model selection
        self.llm_client.set_current_agent(
            self.config.name.lower().replace("agent", "").strip()
        )

        last_error = None
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    # Exponential backoff: 2^attempt seconds
                    wait_time = 2**attempt
                    self.logger.info(
                        f"Retry attempt {attempt + 1}/{max_retries} after {wait_time}s delay"
                    )
                    await asyncio.sleep(wait_time)

                response = await self.llm_client.send_message_async(
                    user_message=user_message,
                    system_message=system_message,
                    temperature=temp,
                    max_tokens=tokens,
                )
                return response

            except Exception as e:
                last_error = e
                self.logger.warning(
                    f"LLM call attempt {attempt + 1}/{max_retries} failed: {str(e)}"
                )

                # Don't retry on certain errors
                error_str = str(e).lower()
                if any(
                    term in error_str
                    for term in [
                        "authentication",
                        "api key",
                        "unauthorized",
                        "forbidden",
                    ]
                ):
                    self.logger.error(f"Non-retryable error: {str(e)}")
                    raise

        # All retries exhausted
        self.logger.error(
            f"LLM call failed after {max_retries} attempts: {str(last_error)}"
        )
        raise Exception(
            f"LLM call failed after {max_retries} retries: {str(last_error)}"
        )

    def validate_input(
        self, input_data: Dict[str, Any], required_keys: List[str]
    ) -> bool:
        """
        Validate that input data contains all required keys

        Args:
            input_data: Input data to validate
            required_keys: List of required keys

        Returns:
            True if valid, raises ValueError otherwise
        """
        missing = [key for key in required_keys if key not in input_data]
        if missing:
            raise ValueError(f"Missing required keys: {', '.join(missing)}")
        return True

    def log_execution(self, step: str, details: str):
        """Log execution steps"""
        self.logger.info(f"[{self.config.name}] {step}: {details}")

    def _merge_workflow_context(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge workflow context into input data for agents to access

        Args:
            input_data: Original input data

        Returns:
            Input data enriched with workflow context
        """
        if self.workflow_context:
            # Get full context for this agent
            full_context = self.workflow_context.get_full_context(
                current_agent=self.config.name
            )

            # Add workflow context to input
            input_data["workflow_context"] = full_context

            # Also add commonly used fields at top level for convenience
            input_data["design_system"] = full_context.get("design_guidelines", "")
            input_data["html_prompt_template"] = full_context.get(
                "html_generation_prompt", ""
            )
            input_data["all_agent_outputs"] = full_context.get("all_agent_outputs", {})

            self.logger.info(
                f"Merged workflow context with {len(full_context.get('all_agent_outputs', {}))} previous agent outputs"
            )

        return input_data

    def parse_json_response(
        self, response: str, fallback_key: str = "raw_response"
    ) -> Dict[str, Any]:
        """
        Parse JSON response from LLM with robust error handling

        Args:
            response: LLM response text
            fallback_key: Key to use if JSON parsing fails

        Returns:
            Parsed JSON dict or fallback dict with raw response
        """
        import json
        import re

        try:
            # Clean response
            response = response.strip()

            # Remove markdown code blocks
            if response.startswith("```json"):
                response = response.split("```json")[1].split("```")[0].strip()
            elif response.startswith("```"):
                response = response.split("```")[1].split("```")[0].strip()

            # Try to parse directly
            parsed = json.loads(response)

            # Validate that we got a dictionary
            if not isinstance(parsed, dict):
                raise json.JSONDecodeError("Response is not a JSON object", response, 0)

            return parsed

        except json.JSONDecodeError as e:
            self.logger.warning(f"Initial JSON parse failed: {str(e)}")

            # Try to extract JSON from text with better control character handling
            try:
                # Look for JSON object pattern
                json_match = re.search(r"\{(?:[^{}]|(?R))*\}", response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    # Fix common control character issues in HTML responses
                    json_str = self._fix_control_characters(json_str)
                    parsed = json.loads(json_str)

                    # Validate that we got a dictionary
                    if not isinstance(parsed, dict):
                        raise json.JSONDecodeError(
                            "Response is not a JSON object", json_str, 0
                        )

                    return parsed

                # Look for JSON array pattern (less common for our use case)
                json_match = re.search(r"\[(?:[^\[\]]|(?R))*\]", response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    # Fix common control character issues in HTML responses
                    json_str = self._fix_control_characters(json_str)
                    parsed = json.loads(json_str)
                    return parsed

            except json.JSONDecodeError:
                pass

            # Return fallback
            self.logger.error(
                f"Could not parse JSON from response (length: {len(response)})"
            )
            self.logger.error(f"Response preview: {response[:500]}")
            return {fallback_key: response, "parse_error": str(e)}

    def _fix_control_characters(self, json_str: str) -> str:
        """
        Fix common control character issues in JSON strings, especially in HTML content

        Args:
            json_str: JSON string that may contain control characters

        Returns:
            Fixed JSON string with control characters properly escaped
        """
        import re

        # Replace common problematic control characters
        # But preserve valid escape sequences
        fixed_str = json_str

        # Handle unescaped quotes within HTML attributes
        # This is a common issue with LLM-generated HTML in JSON
        # But be careful not to double-escape already escaped quotes
        fixed_str = re.sub(r'([^\\])"', r'\1\\"', fixed_str)

        # Handle quotes that are already escaped but missing the backslash
        fixed_str = re.sub(r'\\\\"', r'\\\\"', fixed_str)

        # Handle common control characters that cause JSON parsing issues
        control_chars = {
            "\x00": "\\u0000",
            "\x01": "\\u0001",
            "\x02": "\\u0002",
            "\x03": "\\u0003",
            "\x04": "\\u0004",
            "\x05": "\\u0005",
            "\x06": "\\u0006",
            "\x07": "\\u0007",
            "\x08": "\\b",
            "\x0b": "\\u000b",
            "\x0c": "\\f",
            "\x0e": "\\u000e",
            "\x0f": "\\u000f",
            "\x10": "\\u0010",
            "\x11": "\\u0011",
            "\x12": "\\u0012",
            "\x13": "\\u0013",
            "\x14": "\\u0014",
            "\x15": "\\u0015",
            "\x16": "\\u0016",
            "\x17": "\\u0017",
            "\x18": "\\u0018",
            "\x19": "\\u0019",
            "\x1a": "\\u001a",
            "\x1b": "\\u001b",
            "\x1c": "\\u001c",
            "\x1d": "\\u001d",
            "\x1e": "\\u001e",
            "\x1f": "\\u001f",
            # Also handle common issues with newlines and tabs in strings
            "\n": "\\n",
            "\r": "\\r",
            "\t": "\\t",
        }

        for char, replacement in control_chars.items():
            fixed_str = fixed_str.replace(char, replacement)

        return fixed_str
