GOINFRE = /home/ny-araza/goinfre
UV_CACHE = $(GOINFRE)/uv_cache
HF_CACHE = $(GOINFRE)/home
CALL_DIR = $(GOINFRE)/appel_moi_peuetre
LLM_SDK_DIR = $(CALL_DIR)/llm_sdk
TARGET = installed

all: $(TARGET)

init: $(CALL_DIR)/pyproject.toml
	uv init

install:
	export UV_CACHE_DIR=$(UV_CACHE)
	export HF_CACHE_DIR=$(HF_CACHE)
	uv add $(LLM_SDK_DIR)
	mkdir $(CALL_DIR)/$(TARGET)

