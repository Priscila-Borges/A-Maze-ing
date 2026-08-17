ENTRY = a_maze_ing.py
CONFIG = config.txt
DISPLAY = display.py

install:
	pip install flake8 mypy

run:
	python3 $(ENTRY) $(CONFIG)

venv:
	python3 -m venv .venv
	source .venv/bin/activate

debug:
	python3 -m pdb $(ENTRY) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf __pycache__ .mypy_cache
	rm -rf */__pycache__ */.mypy_cache
	rm -f output_maze.txt
	rm -rf .venv

# Run flake8 and mypy, while ensuring both execute even if one fails.
# Start with status=0 (no errors); set it to 1 if flake8 or mypy finds errors; exit tells make whether the checks passed or failed.
lint:
	@status=0; \
	echo "=== flake8 ==="; \
	python3 -m flake8 . || status=1; \
	echo "\n=== mypy ==="; \
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	exit $$status

lint-strict:
	@status=0; \
	echo "=== flake8 ==="; \
	python3 -m flake8 . || status=1; \
	echo "\n=== mypy ==="; \
	python3 -m mypy --strict . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	exit $$status

.PHONY: install, run, venv, debug, clean, lint, lint-strict, display
