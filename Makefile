start:
	docker run --rm -p 5173:5173 -e VITE_ALLOWED_HOSTS=host.docker.internal hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app

docker-build:
	docker build -t qa-tests .

docker-test:
	docker compose run --rm tests

allure-report:
	allure serve $$(ls -td reports/allure-results-* | head -1)

test:
	uv run pytest && allure serve $$(ls -td reports/allure-results-* | head -1)

smoke:
	uv run pytest -k smoke

ty:
	uv run ty check .

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

format:
	uv run ruff format .

install:
	uv sync
