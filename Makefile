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

# set -a = Marks all variables which are modified or created for export to the environment of subsequent commands
# source local.env = Loads the environment variables from the local.env file
# set +a = Turns off the export of variables
# export PYTHONPATH=$(shell pwd) = Sets the PYTHONPATH variable to the current directory
# cd ./db = Changes the directory to the db directory
# alembic revision --autogenerate = Generates a new migration
migrations:
	@set -a && \
	source local.env && \
	set +a && \
	export PYTHONPATH=$(shell pwd) && \
	cd ./db && \
	alembic revision --autogenerate

migrate:
	@set -a && \
	source local.env && \
	set +a && \
	export PYTHONPATH=$(shell pwd) && \
	cd ./db && \
	alembic upgrade head

# migrations:
# 	@set -a && \
# 	source local.env && \
# 	set +a && \
# 	export PYTHONPATH=$(shell pwd) && \
# 	cd ./db && \
# 	alembic revision --autogenerate

# migrate:
# 	@docker compose run --build migrate

