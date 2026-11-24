GOINFRE = /home/$(USER)/goinfre
UV_CACHE = $(GOINFRE)/uv_cache
HF_CACHE = $(GOINFRE)/home
CALL_DIR = $(CURDIR)
LLM_SDK_DIR = $(CALL_DIR)/llm_sdk
TARGET = installed
export UV_CACHE_DIR=$(UV_CACHE)
export HF_HOME=$(HF_CACHE)
PY_VENV = .venv/bin/python

all: install

install:
	@uv sync

lint:
	@uv run flake8 . --exclude=.venv/,./llm_sdk/  && uv run mypy .  --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs --exclude .llm_sdk/

lint-strict:
	@uv run flake8 . --exclude=.venv/,./llm_sdk/  && uv run mypy . --strict --exclude .llm_sdk/

run:
	@uv run python -m src

clean:
	@uv cache clean && rm -rf $(HF_CACHE)

debug: install
	uv run python -m pdb $(CALL_DIR)/src/__main__.py

fclean: clean
	rm -rf $(CALL_DIR)/src/__pycache*
	rm -rf $(CALL_DIR)/.venv
	rm -rf $(CALL_DIR)/.mypy_cache
	rm -rf $(CALL_DIR)/data/output

re: fclean all
