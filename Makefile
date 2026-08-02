start:
	docker run --rm -p 5173:5173 hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app

allure-report:
	allure serve $$(ls -td reports/allure-results-* | head -1)

test:
	uv run pytest

smoke:
	uv run pytest -m smoke

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
