local_up:
	docker compose -f docker-compose-local.yaml up -d

local_down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force

run:
    docker compose -f docker-compose-ci.yaml up -d

stop:
    docker compose -f docker-compose-ci.yaml down && docker network prune --force
