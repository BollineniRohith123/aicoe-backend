"""
Agent Communication System
Enables natural inter-agent communication and collaboration
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class Message:
    """Represents a message between agents"""
    def __init__(
        self,
        from_agent: str,
        to_agent: str,
        message_type: str,
        content: Any,
        metadata: Optional[Dict] = None
    ):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message_type = message_type  # request, response, notification, query
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
        self.message_id = f"{from_agent}_{to_agent}_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"


class AgentCommunicationHub:
    """
    Central hub for agent-to-agent communication
    Enables agents to send messages, request data, and collaborate
    """
    
    def __init__(self):
        self.message_history: List[Message] = []
        self.agent_registry: Dict[str, Any] = {}
        self.shared_context: Dict[str, Any] = {}
        self.logger = logging.getLogger("agent_communication")
    
    def register_agent(self, agent_name: str, agent_instance: Any):
        """Register an agent in the communication hub"""
        self.agent_registry[agent_name] = agent_instance
        self.logger.info(f"Registered agent: {agent_name}")
    
    def send_message(self, message: Message) -> Optional[Any]:
        """
        Send a message from one agent to another

        Args:
            message: Message object

        Returns:
            Response from the target agent (if synchronous)
        """
        self.message_history.append(message)

        # Enhanced logging with metadata details
        log_message = (
            f"Message: {message.from_agent} → {message.to_agent} "
            f"[{message.message_type}]: {str(message.content)[:100]}"
        )

        # Add metadata information if available
        if message.metadata:
            metadata_summary = []
            for key, value in message.metadata.items():
                if isinstance(value, (list, dict)):
                    metadata_summary.append(f"{key}={len(value)} items")
                else:
                    metadata_summary.append(f"{key}={value}")
            if metadata_summary:
                log_message += f" | Metadata: {', '.join(metadata_summary)}"

        self.logger.info(log_message)

        # Store in shared context if it's important data
        if message.message_type in ["response", "notification"]:
            key = f"{message.from_agent}_to_{message.to_agent}_{message.message_type}"
            self.shared_context[key] = message.content

        return None
    
    def query_agent(self, from_agent: str, to_agent: str, query: str) -> Optional[str]:
        """
        Send a query from one agent to another
        
        Args:
            from_agent: Name of the querying agent
            to_agent: Name of the target agent
            query: Query string
            
        Returns:
            Response from target agent
        """
        message = Message(
            from_agent=from_agent,
            to_agent=to_agent,
            message_type="query",
            content=query
        )
        self.send_message(message)
        
        # In a real implementation, this would wait for a response
        # For now, we'll return None and let agents communicate asynchronously
        return None
    
    def share_data(self, agent_name: str, data_key: str, data_value: Any):
        """
        Share data in the common context for other agents to access

        Args:
            agent_name: Name of the agent sharing data
            data_key: Key for the data
            data_value: Value to share
        """
        full_key = f"{agent_name}_{data_key}"
        self.shared_context[full_key] = data_value

        # Enhanced logging with data size/type information
        data_info = ""
        if isinstance(data_value, dict):
            data_info = f" (dict with {len(data_value)} keys: {', '.join(list(data_value.keys())[:5])})"
        elif isinstance(data_value, list):
            data_info = f" (list with {len(data_value)} items)"
        elif isinstance(data_value, str):
            data_info = f" (string, {len(data_value)} chars)"
        elif isinstance(data_value, bytes):
            data_info = f" (bytes, {len(data_value)} bytes)"

        self.logger.info(f"{agent_name} shared data: {data_key}{data_info}")

        # Notify other agents
        for other_agent in self.agent_registry.keys():
            if other_agent != agent_name:
                message = Message(
                    from_agent=agent_name,
                    to_agent=other_agent,
                    message_type="notification",
                    content=f"New data available: {data_key}",
                    metadata={"data_key": full_key, "data_type": type(data_value).__name__}
                )
                self.send_message(message)
    
    def get_shared_data(self, data_key: str) -> Optional[Any]:
        """
        Retrieve shared data from the context
        
        Args:
            data_key: Key for the data
            
        Returns:
            Data value if found, None otherwise
        """
        return self.shared_context.get(data_key)
    
    def get_agent_output(self, agent_name: str) -> Optional[Any]:
        """
        Get the latest output from a specific agent
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Latest output from the agent
        """
        # Look for the most recent message from this agent
        for message in reversed(self.message_history):
            if message.from_agent == agent_name and message.message_type == "response":
                return message.content
        return None
    
    def get_conversation_history(
        self,
        agent1: Optional[str] = None,
        agent2: Optional[str] = None
    ) -> List[Message]:
        """
        Get conversation history between agents
        
        Args:
            agent1: First agent name (optional)
            agent2: Second agent name (optional)
            
        Returns:
            List of messages
        """
        if agent1 and agent2:
            return [
                msg for msg in self.message_history
                if (msg.from_agent == agent1 and msg.to_agent == agent2) or
                   (msg.from_agent == agent2 and msg.to_agent == agent1)
            ]
        elif agent1:
            return [
                msg for msg in self.message_history
                if msg.from_agent == agent1 or msg.to_agent == agent1
            ]
        else:
            return self.message_history
    
    def get_communication_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all agent communications

        Returns:
            Summary dict with statistics and recent messages
        """
        return {
            "total_messages": len(self.message_history),
            "registered_agents": list(self.agent_registry.keys()),
            "shared_data_keys": list(self.shared_context.keys()),
            "recent_messages": [
                {
                    "from": msg.from_agent,
                    "to": msg.to_agent,
                    "type": msg.message_type,
                    "timestamp": msg.timestamp
                }
                for msg in self.message_history[-10:]
            ]
        }

    def get_all_agents_status(self) -> List[Dict[str, Any]]:
        """
        Get status information for all registered agents

        Returns:
            List of agent status dictionaries
        """
        agents_status = []
        for agent_name, agent_instance in self.agent_registry.items():
            # Get basic status - in a real implementation, agents would have their own status tracking
            status_info = {
                "agent_name": agent_name,
                "status": "active",  # Default status
                "progress": 0.0,     # Default progress
                "message": f"Agent {agent_name} is registered and active"
            }

            # Try to get more detailed status if the agent has status methods
            if hasattr(agent_instance, 'get_status'):
                try:
                    agent_status = agent_instance.get_status()
                    status_info.update(agent_status)
                except Exception as e:
                    status_info["message"] = f"Error getting status: {str(e)}"
                    status_info["status"] = "error"

            agents_status.append(status_info)

        return agents_status


class CommunicatingAgent:
    """
    Mixin class to add communication capabilities to agents
    """
    
    def __init__(self, communication_hub: AgentCommunicationHub):
        self.comm_hub = communication_hub
        self.agent_name = getattr(self, 'config', None).name if hasattr(self, 'config') else "UnknownAgent"
        self.comm_hub.register_agent(self.agent_name, self)
    
    def send_to_agent(self, to_agent: str, message_type: str, content: Any, metadata: Optional[Dict] = None):
        """Send a message to another agent"""
        message = Message(
            from_agent=self.agent_name,
            to_agent=to_agent,
            message_type=message_type,
            content=content,
            metadata=metadata
        )
        self.comm_hub.send_message(message)
    
    def query_agent(self, to_agent: str, query: str) -> Optional[str]:
        """Query another agent"""
        return self.comm_hub.query_agent(self.agent_name, to_agent, query)
    
    def share_output(self, data_key: str, data_value: Any):
        """Share output data with other agents"""
        self.comm_hub.share_data(self.agent_name, data_key, data_value)
    
    def get_agent_data(self, agent_name: str, data_key: str) -> Optional[Any]:
        """Get data shared by another agent"""
        full_key = f"{agent_name}_{data_key}"
        return self.comm_hub.get_shared_data(full_key)
    
    def get_previous_agent_output(self, agent_name: str) -> Optional[Any]:
        """Get the output from a previous agent in the workflow"""
        return self.comm_hub.get_agent_output(agent_name)

