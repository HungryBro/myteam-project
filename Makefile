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
