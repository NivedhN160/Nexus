.PHONY: up down verify logs shell

# Boot the entire Nexus stack
up:
	docker-compose up --build -d

# Spin down the stack
down:
	docker-compose down

# Verify the stack is running and healthy
verify:
	@echo "Verifying Nexus API is reachable..."
	@curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs | grep 200 > /dev/null && echo "API: OK" || echo "API: FAILED"
	@echo "Verifying Nexus UI is reachable..."
	@curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 | grep 200 > /dev/null && echo "UI: OK" || echo "UI: FAILED"
	@echo "Verification Complete."

# View all logs
logs:
	docker-compose logs -f

# Drop into API shell for debugging
shell:
	docker exec -it nexus-api-1 /bin/bash
