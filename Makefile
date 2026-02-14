SHELL := /bin/bash

.PHONY: help up down logs ps

help:
	@echo "Common commands:"
	@echo "  make up    - start dev stack (infra/docker compose)"
	@echo "  make down  - stop dev stack"
	@echo "  make logs  - follow logs"
	@echo "  make ps    - list containers"

up:
	cd infra && docker compose up -d

down:
	cd infra && docker compose down

logs:
	cd infra && docker compose logs -f --tail=200

ps:
	cd infra && docker compose ps
