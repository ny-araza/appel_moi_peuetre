GOINFRE = /home/$(USER)/goinfre
UV_CACHE = $(GOINFRE)/uv_cache
HF_CACHE = $(GOINFRE)/home
CALL_DIR = $(GOINFRE)/appel_moi_peuetre
LLM_SDK_DIR = $(CALL_DIR)/llm_sdk
TARGET = installed
TOML = $(CALL_DIR)/pyproject.toml
SET_CACHE = export UV_CACHE_DIR=$(UV_CACHE) && export HF_HOME=$(HF_CACHE)
PY_VENV = .venv/bin/python
FUNCTION_CALLING_JSON = $(CALL_DIR)/data/input/function_calling_tests.json
FUNCTION_DEFINITION_JSON = $(CALL_DIR)/data/input/functions_definition.json

all: $(TARGET)

$(TARGET): $(TOML)
	touch $(TARGET)

$(TOML):
	uv init
	rm -rf $(CALL_DIR)/main.py
	mkdir -p $(CALL_DIR)/src
	touch $(CALL_DIR)/src/__main__.py

install: $(TOML)
	$(PY_VENV) -m pip install uv pip

sync:
	$(SET_CACHE) && uv add --editable $(LLM_SDK_DIR)
	uv sync

run:
	@uv run python -m src $(ARGUMENTS)

clean:
	$(SET_CACHE) && uv cache clean && rm -rf $(HF_CACHE)

fclean: clean
	rm -rf $(TARGET)
	rm -rf $(CALL_DIR)/src/__pycache*
	rm -rf $(CALL_DIR)/.venv
	rm -rf $(TARGET)

re: fclean all
