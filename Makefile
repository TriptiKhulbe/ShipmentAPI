start:
	docker compose up -d 

bash:
	docker compose exec api bash  

stop:
	docker compose stop 

clean:
	docker compose down --rmi local --volumes

lint:
	docker compose exec api black .
	docker compose exec api isort .
	docker compose exec api flake8 .

requirements:
	docker compose exec api poetry export -f requirements.txt -o requirements.txt --without-hashes

init_db:
	docker compose exec api python setup.py init_db

clean_db:
	docker compose exec api python setup.py clean_db 

load_csv:
	docker compose exec api python setup.py load_csv --filename=data/$(FILENAME)

serve:
	docker compose exec api python app.py 

test:
	docker compose exec api pytest 

test-cov:
	docker compose exec api pytest --cov=. --cov-report html
	