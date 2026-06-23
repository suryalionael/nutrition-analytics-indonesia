.PHONY: install fetch validate inventory test

install:
	pip install -r requirements.txt

fetch:
	python -m src.ingestion.run_all

validate:
	python -m src.validation.run_validation

inventory:
	python -m src.ingestion.build_inventory

test:
	pytest -v
