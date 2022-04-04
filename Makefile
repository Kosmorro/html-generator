black:
	poetry run black kosmorro_pdf_generator

coverage-doctests:
	python3 -m poetry run coverage run tests.py

coverage-report:
	python3 -m poetry run coverage report

doctests:
	python3 -m poetry run python tests.py

.PHONY: tests
tests: doctests

changelog:
	conventional-changelog -p angular -i CHANGELOG.md -s
