"""
Discord Bot Wrapper for myteam-project
Manages agent permissions and channel access for Discord integration.
"""

import os
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PermissionType(Enum):
    """Permission types for Discord channels."""
    READ = "read"
    WRITE = "write"


@dataclass
class AgentPermission:
    """Agent permission configuration."""
    agent_name: str
    channel_name: str
    can_read: bool
    can_write: bool

    def __str__(self) -> str:
        perms = []
        if self.can_read:
            perms.append("R")
        if self.can_write:
            perms.append("W")
        perm_str = "/".join(perms) if perms else "—"
        return f"{self.agent_name:20} → {self.channel_name:25} [{perm_str}]"


class DiscordBotWrapper:
    """Discord bot wrapper for managing agent permissions and channel access."""

    def __init__(self, config_path: str = "discord_config.json"):
        """Initialize Discord bot wrapper with configuration."""
        self.config_path = config_path
        self.config = self._load_config()
        self.agents = self.config.get("agents", {})
        self.channels = self.config.get("channels", {})
        self.permissions_cache: Dict[str, List[AgentPermission]] = {}
        logger.info(f"Initialized DiscordBotWrapper with {len(self.agents)} agents")

    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
                return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise

    def get_agent_permissions(self, agent_name: str) -> Dict[str, List[str]]:
        """Get permissions for a specific agent."""
        if agent_name not in self.agents:
            logger.warning(f"Agent '{agent_name}' not found in configuration")
            return {"read": [], "write": []}
        
        return self.agents[agent_name].get("permissions", {"read": [], "write": []})

    def can_read_channel(self, agent_name: str, channel_key: str) -> bool:
        """Check if an agent can read from a channel."""
        permissions = self.get_agent_permissions(agent_name)
        return channel_key in permissions.get("read", [])

    def can_write_channel(self, agent_name: str, channel_key: str) -> bool:
        """Check if an agent can write to a channel."""
        permissions = self.get_agent_permissions(agent_name)
        return channel_key in permissions.get("write", [])

    def verify_permission(self, agent_name: str, channel_key: str, 
                         permission_type: PermissionType) -> bool:
        """Verify if an agent has specific permission for a channel."""
        if agent_name not in self.agents:
            logger.warning(f"Agent '{agent_name}' not found")
            return False
        
        if channel_key not in self.channels:
            logger.warning(f"Channel '{channel_key}' not found")
            return False
        
        if permission_type == PermissionType.READ:
            return self.can_read_channel(agent_name, channel_key)
        elif permission_type == PermissionType.WRITE:
            return self.can_write_channel(agent_name, channel_key)
        
        return False

    def get_channel_info(self, channel_key: str) -> Optional[Dict]:
        """Get information about a specific channel."""
        if channel_key not in self.channels:
            logger.warning(f"Channel '{channel_key}' not found")
            return None
        
        return self.channels[channel_key]

    def get_agent_info(self, agent_name: str) -> Optional[Dict]:
        """Get information about a specific agent."""
        if agent_name not in self.agents:
            logger.warning(f"Agent '{agent_name}' not found")
            return None
        
        return self.agents[agent_name]

    def list_agent_readable_channels(self, agent_name: str) -> List[str]:
        """List all channels an agent can read."""
        permissions = self.get_agent_permissions(agent_name)
        return permissions.get("read", [])

    def list_agent_writable_channels(self, agent_name: str) -> List[str]:
        """List all channels an agent can write to."""
        permissions = self.get_agent_permissions(agent_name)
        return permissions.get("write", [])

    def generate_permission_matrix(self) -> str:
        """Generate a human-readable permission matrix."""
        # Collect all permissions
        all_permissions = []
        for agent_name in sorted(self.agents.keys()):
            for channel_key in sorted(self.channels.keys()):
                can_read = self.can_read_channel(agent_name, channel_key)
                can_write = self.can_write_channel(agent_name, channel_key)
                
                if can_read or can_write:
                    perm = AgentPermission(
                        agent_name=agent_name,
                        channel_name=channel_key,
                        can_read=can_read,
                        can_write=can_write
                    )
                    all_permissions.append(perm)
        
        # Generate table
        header = f"{'Agent':<20} | {'Channel':<25} | {'Permission':<12}"
        separator = "-" * len(header)
        
        lines = [header, separator]
        for perm in all_permissions:
            lines.append(str(perm))
        
        return "\n".join(lines)

    def generate_channel_matrix(self) -> str:
        """Generate a channel × agent permission matrix."""
        agents = sorted(self.agents.keys())
        channels = sorted(self.channels.keys())
        
        # Build header
        header = f"{'Channel':<25} | " + " | ".join(f"{agent:<15}" for agent in agents)
        separator = "-" * len(header)
        
        lines = [header, separator]
        
        # Build rows
        for channel_key in channels:
            row = f"{channel_key:<25} | "
            perms = []
            for agent_name in agents:
                can_read = self.can_read_channel(agent_name, channel_key)
                can_write = self.can_write_channel(agent_name, channel_key)
                
                if can_read and can_write:
                    perm = "RW"
                elif can_read:
                    perm = "R"
                elif can_write:
                    perm = "W"
                else:
                    perm = "—"
                
                perms.append(f"{perm:<15}")
            
            row += " | ".join(perms)
            lines.append(row)
        
        return "\n".join(lines)

    def validate_configuration(self) -> bool:
        """Validate configuration integrity."""
        logger.info("Validating configuration...")
        
        # Check agents
        if not self.agents:
            logger.error("No agents defined in configuration")
            return False
        
        # Check channels
        if not self.channels:
            logger.error("No channels defined in configuration")
            return False
        
        # Validate agent permissions reference valid channels
        for agent_name, agent_config in self.agents.items():
            permissions = agent_config.get("permissions", {})
            
            for channel_key in permissions.get("read", []):
                if channel_key not in self.channels:
                    logger.error(f"Agent '{agent_name}' references unknown channel '{channel_key}' in read permissions")
                    return False
            
            for channel_key in permissions.get("write", []):
                if channel_key not in self.channels:
                    logger.error(f"Agent '{agent_name}' references unknown channel '{channel_key}' in write permissions")
                    return False
        
        logger.info("Configuration validation passed")
        return True


def main():
    """Main entry point for testing."""
    # Load configuration
    wrapper = DiscordBotWrapper("discord_config.json")
    
    # Validate configuration
    if not wrapper.validate_configuration():
        logger.error("Configuration validation failed")
        return 1
    
    # Display permission matrix
    print("\n" + "=" * 80)
    print("AGENT × CHANNEL PERMISSION MATRIX")
    print("=" * 80)
    print(wrapper.generate_channel_matrix())
    
    print("\n" + "=" * 80)
    print("DETAILED PERMISSIONS")
    print("=" * 80)
    print(wrapper.generate_permission_matrix())
    
    # Display agent information
    print("\n" + "=" * 80)
    print("AGENT INFORMATION")
    print("=" * 80)
    for agent_name in sorted(wrapper.agents.keys()):
        agent_info = wrapper.get_agent_info(agent_name)
        print(f"\n{agent_name.upper()}")
        print(f"  Role: {agent_info.get('role', 'N/A')}")
        print(f"  Description: {agent_info.get('description', 'N/A')}")
        
        readable = wrapper.list_agent_readable_channels(agent_name)
        writable = wrapper.list_agent_writable_channels(agent_name)
        
        print(f"  Readable channels ({len(readable)}): {', '.join(readable)}")
        print(f"  Writable channels ({len(writable)}): {', '.join(writable)}")
    
    return 0


if __name__ == "__main__":
    exit(main())
