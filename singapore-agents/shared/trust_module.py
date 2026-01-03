"""Trust module for inter-agent communication and verification.

This module provides utilities for verifying agent trust and managing
agent information in the multi-agent system.
"""

import logging
from typing import Dict, Optional

# Define trusted agents in the system
TRUSTED_AGENTS = {
    "hawker": {
        "name": "Hawker Agent",
        "description": "Provides information about hawker centers in Singapore",
        "trust_level": "high",
        "capabilities": ["hawker_search", "food_recommendations"]
    },
    "psi": {
        "name": "PSI Agent",
        "description": "Provides Pollutant Standards Index information",
        "trust_level": "high",
        "capabilities": ["psi_reading", "air_quality_advisory"]
    },
    "merlion": {
        "name": "Merlion Agent",
        "description": "Provides tourist attractions and information",
        "trust_level": "high",
        "capabilities": ["attraction_search", "tourist_information"]
    }
}


def verify_agent_trust(agent_id: str) -> bool:
    """Verify if an agent is trusted in the system.
    
    Args:
        agent_id: The identifier of the agent to verify
        
    Returns:
        True if the agent is trusted, False otherwise
    """
    is_trusted = agent_id in TRUSTED_AGENTS
    
    if is_trusted:
        logging.info(f"Agent '{agent_id}' verified as trusted")
    else:
        logging.warning(f"Agent '{agent_id}' is not in trusted agents list")
    
    return is_trusted


def get_agent_info(agent_id: str) -> Optional[Dict]:
    """Get information about a specific agent.
    
    Args:
        agent_id: The identifier of the agent
        
    Returns:
        Dictionary containing agent information, or None if not found
    """
    agent_info = TRUSTED_AGENTS.get(agent_id)
    
    if agent_info:
        return {
            "id": agent_id,
            **agent_info
        }
    else:
        logging.warning(f"No information found for agent '{agent_id}'")
        return None


def get_all_agents() -> Dict:
    """Get information about all registered agents.
    
    Returns:
        Dictionary of all agents and their information
    """
    return TRUSTED_AGENTS.copy()


def validate_agent_capability(agent_id: str, capability: str) -> bool:
    """Check if an agent has a specific capability.
    
    Args:
        agent_id: The identifier of the agent
        capability: The capability to check for
        
    Returns:
        True if the agent has the capability, False otherwise
    """
    agent_info = TRUSTED_AGENTS.get(agent_id)
    
    if not agent_info:
        return False
    
    return capability in agent_info.get("capabilities", [])


def get_trust_level(agent_id: str) -> Optional[str]:
    """Get the trust level of an agent.
    
    Args:
        agent_id: The identifier of the agent
        
    Returns:
        Trust level string, or None if agent not found
    """
    agent_info = TRUSTED_AGENTS.get(agent_id)
    
    if agent_info:
        return agent_info.get("trust_level")
    
    return None
