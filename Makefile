ENTRY = a_maze_ing.py 
CONFIG = config.txt

install:
	pip install flake8 mypy
run:
	python3 $(ENTRY) $(CONFIG)
venv:
	python3 -m venv .venv
debug: 
	python3 -m pdb $(ENTRY) $(CONFIG)
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 
	rm -rf .mypy_cache
lint: 
	flake8 . --exclude=.venv
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint-strict: 
	flake8 . --exclude=.venv 
	mypy . --strict
.PHONY: install, run, venv, debug, clean, lint, lint strict