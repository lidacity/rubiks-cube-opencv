
init:
	python3 -m venv venv
	@./venv/bin/python3 -m pip install -e .

install:
	python3 setup.py install

clean:
	sudo rm -rf build dist venv
	sudo rm -rf rubiks_cube_opencv.egg-info rubiks_cube_opencv/*.pyc rubiks_cube_opencv/__pycache__

test:
	python3 ./tests/test.py

checks: black-check lint-check   ## Run all checks (black, lint)

black-check:  ## Check code formatter.
	black --check rubiks_cube_opencv/ utils/ usr/

black-format:
	black rubiks_cube_opencv/ utils/ usr/

lint-check:  ## Check linter.
	flake8 --config .flake8 --statistics rubiks_cube_opencv/ utils/ usr/
