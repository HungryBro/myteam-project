up:
	docker-compose up -d
down:
	docker-compose down
logs:
	docker-compose logs -f
restart:
	docker-compose restart
invite-bots:
	@echo "Chief Bot: https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot"
config:
	docker-compose up -d --build
status:
	docker-compose ps

setup:
	@echo "1. Copy .env.example to .env"
	@echo "2. Fill in your API keys"
	@echo "3. Run: make up"
	cp -n .env.example .env || true

trading-mcp:
	cd services/trading-mcp && pip install -r requirements.txt && uvicorn server:app --host 0.0.0.0 --port 3003

test:
	@echo "Testing Docker services..."
	docker-compose ps
	@echo ""
	@echo "Testing Trading MCP..."
	curl -s http://localhost:3003/health || echo "Trading MCP not running"
	@echo ""
	@echo "Testing TradingView MCP..."
	curl -s http://localhost:3001/health || echo "TradingView MCP not running"

health:
	docker-compose ps
	@echo "---"
	@curl -s http://localhost:3003/health 2>/dev/null || echo "Trading MCP: offline"
	@curl -s http://localhost:3001/health 2>/dev/null || echo "TradingView MCP: offline"
