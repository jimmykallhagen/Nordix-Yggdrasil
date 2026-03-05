# Nordix Tools - Makefile
CC      = clang
CFLAGS  = -march=native -mtune=native -O3 -flto=full -Wall
PREFIX  = /usr/local/bin

TARGETS = scroll-bottom scroll-top

all: $(TARGETS)

scroll-top: scroll-top.c
	$(CC) $(CFLAGS) -o $@ $

scroll-bottom: scroll-bottom.c
	$(CC) $(CFLAGS) -o $@ $

install: all
	install -Dm755 $(TARGETS) -t $(PREFIX)

clean:
	rm -f $(TARGETS)

.PHONY: all install clean