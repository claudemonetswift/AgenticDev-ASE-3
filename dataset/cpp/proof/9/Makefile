CC = g++
SOURCES = test.cpp
FILES := $(subst .cpp,,$(SOURCES))

all: $(FILES)

% :: %.cpp ie_ir_parser.cpp
	$(CC) -g -Wall -Wvla $< ie_ir_parser.cpp -o $@

clean:
	rm -rf $(FILES)
