default:
  @just --list --unsorted

# Run ruff lint & format
tidy:
  @poetry run ruff check --fix
  @poetry run ruff format

# Run all tests
test-all:
  @poetry run pytest -v

# Publish to PyPi
publish:
  @poetry build
  @poetry publish


# Start a postgresql container. MEMENTO_DB_CONNECTION_STRING="postgresql://myuser:mypassword@localhost:5432/mydatabase"
start-postgres:
  @docker run \
    --name mypostgres \
    -e POSTGRES_USER=myuser \
    -e POSTGRES_PASSWORD=mypassword \
    -e POSTGRES_DB=mydatabase \
    -p 5432:5432 \
    -d postgres

# Clean postgresql container.
delete-postgres:
  @docker stop mypostgres > /dev/null
  @echo "Stopped container"
  @docker rm mypostgres > /dev/null
  @echo "Removed container"
