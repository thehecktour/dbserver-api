IMAGE_NAME = dbserver-api

PORT = 8000

.PHONY: help build run stop clean test shell install local migrate pre-commit

help:
	@echo "Available commands:"
	@echo "  make build        -> Build the Docker image"
	@echo "  make run          -> Run the Docker container"
	@echo "  make stop         -> Stop and remove the container"
	@echo "  make clean        -> Remove containers and Docker images"
	@echo "  make test         -> Run tests with pytest"
	@echo "  make shell        -> Start poetry shell"
	@echo "  make install      -> Install dependencies with Poetry"
	@echo "  make local        -> Run Django local development server"
	@echo "  make migrate      -> Run Django migrations inside the container"
	@echo "  make pre-commit   -> Run all pre-commit hooks manually"

build:
	podman build -t $(IMAGE_NAME) .

run:
	podman run -d -p $(PORT):$(PORT) --name $(IMAGE_NAME) $(IMAGE_NAME)

stop:
	podman stop $(IMAGE_NAME) || true
	podman rm $(IMAGE_NAME) || true

clean:
	podman stop $(IMAGE_NAME) || true
	podman rm $(IMAGE_NAME) || true
	podman rmi -f $(IMAGE_NAME) || true

shell:
	poetry shell

install:
	poetry install

local:
	poetry run python manage.py runserver 0.0.0.0:$(PORT)

migrate:
	podman exec -it $(IMAGE_NAME) poetry run python manage.py migrate

test:
	poetry run pytest -v --cov=src tests/

pre-commit:
	poetry run pre-commit run --all-files
