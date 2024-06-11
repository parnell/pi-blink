# Test Project
test:: 
	pytest tests/*test_*.py

format::
	toml-sort pyproject.toml
	mypy --python-version=3.10

# Build the project
build:: 
	poetry install --with dev
	toml-sort pyproject.toml
	poetry build

# Publish the project
publish:: build
	poetry publish
