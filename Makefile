
run:
	python3 main.py maps/challenger/01_the_impossible_dream.txt

install:
	pip install pygame
	pip install mypy
	pip install flake8

debug:
	python3 -m pdb main.py

clean:
	rm -rf .mypy_cache
	rm -rf __pycache__


lint:
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	flake8 .
