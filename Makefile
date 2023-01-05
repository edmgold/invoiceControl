
.PHONY: test

docker:
	docker_compose up --build

test:
	pytest

test-coverage:
	pytest -vv --cov=. --cov-report=term-missing
	
run:
	uvicorn main:app --reload	

install:
	pip install pipenv
	pipenv install

uninstall:
	pipenv clean

alembic-start: # apenas no inicio do projeto, este comando apaga todos os migrations
	alembic init migrations

make-migrations: # analisa e gera as migrações
	alembic revision --autogenerate -m "$(M)"

migrate: # executa a migração
	alembic upgrade head


