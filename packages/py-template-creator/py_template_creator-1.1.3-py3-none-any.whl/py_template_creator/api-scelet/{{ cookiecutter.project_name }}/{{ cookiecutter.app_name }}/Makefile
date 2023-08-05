SHELL := /bin/bash
include ../.env
export

env:
	pip install -r requirements/local.txt  > /dev/null

run:
	@echo "Running service..."
	python package/run.py

test:
	@echo "Running unit tests..."
	env TEST_DB=True coverage run --source=package setup.py test ${module} && \
	coverage html && \
	coverage report
	@echo
	@echo "Flake8 errors in code ----------------"
	@echo
	@echo "--------------------------------------"
	@python -m flake8 --max-line-length=180 --exclude .git,__pycache__,.eggs,build
	@echo "OK, no flake8 errors in code"
	@echo "--------------------------------------"

lint:
	@python -m flake8 --max-line-length=180 --exclude .git,__pycache__,.eggs,build

generate-migrations:
	@echo "Generating migrations ..."
	alembic revision --autogenerate -m "${message}"

migrate:
	@echo "Running migrations ..."
	alembic upgrade head
	@echo "Migrations finished."

downgrade:
	@echo "Running downgrade ..."
	alembic downgrade ${level}
	@echo "Migrations finished."

init_db:
	@echo "Initing database ..."
	alembic ensure_version
	@echo "Migrations finished."

check_db:
	@echo "Checking migrations ..."
	alembic check
	@echo "Migrations finished."
