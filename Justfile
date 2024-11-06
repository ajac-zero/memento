default:
  @just --list --unsorted

tidy:
  @poetry run ruff check --fix
  @poetry run ruff format

test-all:
  @poetry run pytest -v

publish:
  @poetry build
  @poetry publish
