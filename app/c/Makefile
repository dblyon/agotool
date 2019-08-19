CFLAGS=-Wall -g

all: clean compile

clean: 
	rm -f compute_global_enrichment_DBL

compile:
	cc -O3 -pthread -lm compute_global_enrichment_DBL.c -o compute_global_enrichment_DBL
