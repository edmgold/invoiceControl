
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

