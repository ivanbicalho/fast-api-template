# DEVELOPMENT

install:
	@pip install -r requirements/dev.txt

black:
	@black --line-length 120 .

ruff:
	@ruff check . --fix

mypy:
	@mypy .

lint:
	$(MAKE) black
	$(MAKE) ruff
	$(MAKE) mypy

requirements_files:= $(shell find requirements -type f)
update-requirements:
	@for file in $(requirements_files); do \
		echo "Analizing $$file"; \
		pur -r $$file; \
	done

# --------------------------------------------------

# SQL

migrations:
	@docker compose run --build make-migrations

migrate:
	@docker compose run --build migrate
