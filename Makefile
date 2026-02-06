.PHONY: install install-dev test clean help run

help:
	@echo pulse - network diagnostics tool
	@echo.
	@echo Available commands:
	@echo   make install       - Install pulse package
	@echo   make install-dev   - Install in development mode
	@echo   make test          - Run unit tests
	@echo   make clean         - Remove build artifacts
	@echo   make run           - Run pulse on api.github.com

install:
	pip install .

install-dev:
	pip install -e .

test:
	python -m pytest test_pulse.py -v || python test_pulse.py

clean:
	powershell -Command "Remove-Item -Path build, dist -Recurse -ErrorAction SilentlyContinue; Remove-Item -Path *.egg-info -Recurse -ErrorAction SilentlyContinue; Get-ChildItem -Path . -Filter __pycache__ -Recurse | Remove-Item -Recurse -ErrorAction SilentlyContinue; Get-ChildItem -Path . -Filter *.pyc -Recurse | Remove-Item -ErrorAction SilentlyContinue"

run:
	python pulse.py api.github.com

run-json:
	python pulse.py api.github.com --json

run-deep:
	python pulse.py api.github.com --deep
