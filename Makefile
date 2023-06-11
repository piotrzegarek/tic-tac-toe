build:
	docker-compose build

up:
	docker-compose up -d

db:
	docker-compose exec app python manage.py create_db

down:
	docker-compose down

logs:
	docker-compose logs -f

destroy:
	docker-compose stop
	docker-compose rm -f
	docker volume rm postgres_data