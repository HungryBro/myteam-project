# Discord Bot Wrapper for myteam-project

This service provides a centralized Discord bot wrapper that manages permissions and channel access for all agents in the myteam-project system.

## Overview

The Discord Bot Wrapper handles the following responsibilities:

- **Agent Permission Management:** Defines read/write permissions for each agent across all Discord channels
- **Channel Access Control:** Enforces permission rules to ensure agents can only access channels they are authorized for
- **Configuration Management:** Centralized configuration in `discord_config.json` for easy maintenance
- **Permission Verification:** Provides methods to verify agent permissions before allowing channel operations

## Architecture

### Components

1. **discord_config.json** — Configuration file defining agents, channels, and permissions
2. **discord_bot.py** — Main Python module implementing the permission wrapper
3. **README.md** — This documentation file

### Agent Roles

| Agent | Role | Responsibilities |
|---|---|---|
| **chief** | Chief Executive Officer | Oversees strategy, coordinates agents, makes high-level decisions |
| **analyst** | Market Analyst | Market research, YouTube analysis, technical analysis |
| **forex_executor** | Forex Trading Executor | Executes Forex trades via MT5, manages positions |
| **crypto_executor** | Crypto Trading Executor | Executes Crypto trades via Binance, manages positions |

## Channel Structure

### 🌐 General Channels
- **#openrouter_setting** — OpenRouter API configuration and usage tracking
- **#opensource_github** — GitHub repository updates and open source discussions

### 🏢 Executive Direct
- **#ceo_office** — Chief executive decisions and directives
- **#company_reports** — Company performance reports and summaries

### 💻 Operations & Tech
- **#tech_lab** — Technical development and experimentation
- **#system_logs** — System logs and error tracking

### 📈 Growth & Marketing
- **#marketing_hub** — Marketing initiatives and growth strategies

### 🤝 Team Collaboration
- **#agent_coworking** — Agent collaboration and teamwork
- **#war_room** — Critical market situations and emergency coordination

### 📊 Financial & Trading Hub
- **#trading_terminal** — Trading signals, positions, and execution reports
- **#economic_calendar** — Economic events and market calendar

## Permission Matrix

| Channel | Chief | Analyst | Forex Exec | Crypto Exec |
|---|:---:|:---:|:---:|:---:|
| #openrouter_setting | R | R | R | R |
| #opensource_github | R | R | R | R |
| #ceo_office | RW | R | R | R |
| #company_reports | RW | W | R | R |
| #tech_lab | R | RW | R | R |
| #system_logs | R | R | R | R |
| #marketing_hub | RW | R | R | R |
| #agent_coworking | RW | RW | RW | RW |
| #war_room | RW | R | RW | RW |
| #trading_terminal | R | RW | RW | RW |
| #economic_calendar | R | RW | R | R |

**Legend:** R = Read, W = Write, RW = Read + Write, — = No Access

## Usage

### Python API

```python
from discord_bot import DiscordBotWrapper, PermissionType

# Initialize wrapper
wrapper = DiscordBotWrapper("discord_config.json")

# Check if agent can read channel
if wrapper.can_read_channel("chief", "ceo_office"):
    print("Chief can read #ceo_office")

# Check if agent can write channel
if wrapper.can_write_channel("analyst", "trading_terminal"):
    print("Analyst can write to #trading_terminal")

# Verify specific permission
can_access = wrapper.verify_permission(
    "forex_executor", 
    "trading_terminal", 
    PermissionType.WRITE
)

# Get agent information
agent_info = wrapper.get_agent_info("chief")
print(f"Agent role: {agent_info['role']}")

# List readable channels for an agent
readable = wrapper.list_agent_readable_channels("analyst")
print(f"Analyst can read: {readable}")

# List writable channels for an agent
writable = wrapper.list_agent_writable_channels("analyst")
print(f"Analyst can write: {writable}")

# Generate permission matrix
print(wrapper.generate_permission_matrix())

# Generate channel matrix
print(wrapper.generate_channel_matrix())

# Validate configuration
if wrapper.validate_configuration():
    print("Configuration is valid")
```

### Command Line

```bash
# Test and display permission matrix
python discord_bot.py
```

## Configuration Format

The `discord_config.json` file uses the following structure:

```json
{
  "agents": {
    "agent_name": {
      "name": "Display Name",
      "role": "Role Title",
      "description": "Agent description",
      "permissions": {
        "read": ["channel_key_1", "channel_key_2"],
        "write": ["channel_key_3"]
      }
    }
  },
  "channels": {
    "channel_key": {
      "name": "#channel_name",
      "category": "Category Name",
      "description": "Channel description"
    }
  }
}
```

## Integration with Discord Bots

Each agent runs a separate Discord bot instance (defined in `docker-compose.yml`). The wrapper provides permission verification that should be integrated into each bot's message handling:

```python
# In each agent's Discord bot
from services.discord.discord_bot import DiscordBotWrapper, PermissionType

wrapper = DiscordBotWrapper()

async def on_message(message):
    agent_name = os.getenv("AGENT_NAME")
    channel_key = get_channel_key(message.channel.id)
    
    # Check read permission
    if not wrapper.can_read_channel(agent_name, channel_key):
        return  # Ignore message
    
    # Process message
    response = await process_message(message.content)
    
    # Check write permission before sending
    if wrapper.can_write_channel(agent_name, channel_key):
        await message.channel.send(response)
```

## Environment Variables

The Discord bot wrapper uses the following environment variables from `.env`:

```bash
# Discord Server
DISCORD_SERVER_ID=1479816157203795998

# Channel IDs
DISCORD_CHANNEL_OPENROUTER_SETTING=1490004453707743252
DISCORD_CHANNEL_OPENSOURCE_GITHUB=1490557665036992572
DISCORD_CHANNEL_CEO_OFFICE=1492883839272616056
DISCORD_CHANNEL_COMPANY_REPORTS=1492883813079060600
DISCORD_CHANNEL_TECH_LAB=1492883779919020182
DISCORD_CHANNEL_SYSTEM_LOGS=1492883761455435886
DISCORD_CHANNEL_MARKETING_HUB=1492883730107465799
DISCORD_CHANNEL_AGENT_COWORKING=1492883596854165676
DISCORD_CHANNEL_WAR_ROOM=1492883623106318486
DISCORD_CHANNEL_TRADING_TERMINAL=1492883513790169128
DISCORD_CHANNEL_ECONOMIC_CALENDAR=1492883560036564992

# Bot Tokens (one per agent)
DISCORD_BOT_TOKEN_chief=<token>
DISCORD_BOT_TOKEN_analyst=<token>
DISCORD_BOT_TOKEN_forex_executor=<token>
DISCORD_BOT_TOKEN_crypto_executor=<token>
```

## Testing

To test the Discord bot wrapper:

```bash
cd services/discord
python discord_bot.py
```

This will display:
1. Agent × Channel Permission Matrix
2. Detailed Permissions List
3. Agent Information with readable/writable channels

## Future Enhancements

- Integration with actual Discord bot instances
- Webhook support for automated channel messages
- Audit logging for permission changes
- Dynamic permission updates without restart
- Role-based permission inheritance
- Channel category-based default permissions

## References

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [myteam-project Main Repository](../../README.md)
