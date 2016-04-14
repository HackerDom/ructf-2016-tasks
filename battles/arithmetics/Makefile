CC=gcc
CFLAGS=-m32

ODIR=out

_OBJ = gen.o arithmetics.o 
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))


$(ODIR)/%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

all: gen arithmetics

gen: $(ODIR)/gen.o
	$(CC) -o $(ODIR)/$@ $^ $(CFLAGS)

arithmetics: $(ODIR)/arithmetics.o
	$(CC) -o $(ODIR)/$@ $^ $(CFLAGS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*
