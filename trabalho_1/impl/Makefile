.PHONY: run

ASSETS_DIR := resources
TEST_FILES := $(wildcard $(ASSETS_DIR)/*.txt)

all: run

install:
	poetry install

run: install
ifdef TEST
	cat $(ASSETS_DIR)/$(TEST) | poetry run py_8pzzl
else
	@for file in $(TEST_FILES); do \
		echo "Running $$file..."; \
		cat $$file | poetry run py_8pzzl; \
		echo ""; \
	done
endif
