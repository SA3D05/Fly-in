

run:
	@python3 main.py 
install:
	pip install pygame



debug:
	@ echo "Later"

clean:
	@ rm -rf .mypy_cache
	@ rm -rf __pycache__


lint:
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	flake8 .
