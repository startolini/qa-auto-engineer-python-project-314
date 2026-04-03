start:
	docker run --rm -p 5173:5173 hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app

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
