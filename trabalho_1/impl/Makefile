.PHONY: run

ASSETS_DIR := resources
TEST_FILES := $(wildcard $(ASSETS_DIR)/*.txt)

ifdef POSTFIX
    FILTERED_FILES := $(filter %_$(POSTFIX).txt,$(TEST_FILES))
else
    FILTERED_FILES := $(TEST_FILES)
endif

all: run

install:
	poetry install

run: install
ifdef TEST
	cat $(ASSETS_DIR)/$(TEST) | poetry run py_8pzzl
else
	@for file in $(FILTERED_FILES); do \
		echo "Running $$file..."; \
		cat $$file | poetry run py_8pzzl; \
		echo ""; \
	done
endif
