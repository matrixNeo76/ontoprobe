PYTHON ?= python3

.PHONY: help test build check mock estimate

help:
	@echo "make test      run the offline unit tests"
	@echo "make build     regenerate the Colab notebook and the task list"
	@echo "make check     test + verify generated files are up to date"
	@echo "make mock      offline dry run of the black-box pipeline (random numbers)"
	@echo "make estimate  estimate calls and cost of the 6-task pilot"

test:
	$(PYTHON) -m unittest discover -s code/tests

build:
	$(PYTHON) tools/build_notebook.py
	$(PYTHON) tools/build_tasks.py

check: test build
	@changes="$$(git status --porcelain -- code/notebook_caa_smoke_test_v0_3_2.ipynb code/blackbox/data/tasks_b.json)"; \
	if [ -n "$$changes" ]; then echo "$$changes"; echo "Generated files are stale or not committed. Commit the result of 'make build'."; exit 1; fi

mock:
	$(PYTHON) code/run_blackbox.py all --run-id mock --limit 6 --mock

estimate:
	$(PYTHON) code/run_blackbox.py estimate --limit 6
