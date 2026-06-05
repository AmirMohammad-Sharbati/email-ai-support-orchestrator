.PHONY: install run test clean

install:
	pip install -r requirements.txt

run:
	export PYTHONPATH=$(PWD)/src && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +