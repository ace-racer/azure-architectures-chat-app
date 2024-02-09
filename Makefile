code_paths=az_architectures_chat_app

lint-check: 
	@poetry run ruff check $(code_paths)

lint-fix:
	@poetry run ruff --fix $(code_paths)

format-check:
	@poetry run black --check --diff $(code_paths)

format-fix:
	@poetry run black $(code_paths)

complete-check: lint-check format-check
complete-fix: lint-fix format-fix

run-app:
	@poetry run streamlit run az_architectures_chat_app/main.py
