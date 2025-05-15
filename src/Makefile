BUILD = build
BOOKNAME = opinion_pieces
TITLE = title.txt
METADATA = metadata.xml
CHAPTERS = $(shell find ./md -name '*.md' | sort)
TOC = --toc --toc-depth=2

all: epub mobi

clean:
	rm -rf $(BUILD)

epub: $(BUILD)/$(BOOKNAME).epub

mobi: $(BUILD)/$(BOOKNAME).mobi

$(BUILD)/$(BOOKNAME).epub: $(TITLE) $(CHAPTERS)
	mkdir -p $(BUILD)
	pandoc $(TOC) --epub-metadata=$(METADATA) -o $@ $^

$(BUILD)/$(BOOKNAME).mobi: epub
	mkdir -p $(BUILD)
	ebook-convert $(BUILD)/$(BOOKNAME).epub $@

.PHONY: all
