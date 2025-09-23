.PHONY: run

LOGDIR := output
ASSETS_DIR := resources
TEST_FILES := $(wildcard $(ASSETS_DIR)/*.txt)

ifeq (,$(filter undefined,$(origin TEST) $(origin POSTFIX)))
$(error You must specify only one of TEST or POSTFIX, not both)
endif

ifdef POSTFIX
    FILTERED_FILES := $(filter %_$(POSTFIX).txt,$(TEST_FILES))
else
    FILTERED_FILES := $(TEST_FILES)
endif

all: run

clean:
	rm -rf $(LOGDIR)

install: clean
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
