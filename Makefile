.PHONY: install fetch validate inventory test missing-report merge clean-data

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

missing-report:
	python -m src.cleaning.profile_missing

merge:
	python -m src.cleaning.merge

clean-data: missing-report merge
