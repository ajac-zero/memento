default:
  @just --list --unsorted

test-all:
  @poetry run pytest -v

publish:
  @poetry build
  @poetry publish
