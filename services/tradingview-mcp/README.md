# TradingView MCP Service

This service integrates the TradingView Market-Context Protocol (MCP) into the `myteam-project`.

## Installation

To run this service, ensure you have Docker and Docker Compose installed. The service is defined in the `docker-compose.yml` file.

## Usage

The `tradingview-mcp` service can be started using Docker Compose:

```bash
docker-compose up -d tradingview-mcp
```

This will pull the `atilaahmet/tradingview-mcp:latest` image and start the container, exposing port `8080` on the host, which maps to port `8000` inside the container. The service will automatically restart unless stopped.

## Configuration

The service is configured with the following environment variables in `docker-compose.yml`:

- `PORT=8000`: The internal port the application listens on.
- `HOST=0.0.0.0`: The host address the application binds to, allowing external access within the Docker network.

For more detailed usage and available tools, refer to the `skills/tradingview-mcp/SKILL.md` and `tools/trading.py` files.
