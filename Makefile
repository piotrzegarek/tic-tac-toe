build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

destroy:
	docker-compose stop
	docker-compose rm -f
	docker volume rm postgres_data