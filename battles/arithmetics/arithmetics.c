#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char secret[] = "\x67\x8b\xf9\xad\xf9\xe5\xe8\xad\xef\xe8\xfe\xf9\xad\xff\xe8\xfb\xe8\xff\xfe\xe8\xff\xac\xad\x99\x71\x13";
int secret_number = 423133742;

int main(int argc, char **argv) {
	if (argc < 2) {
		fprintf(stderr, "Missing argument, usage: %s <number>\n", argv[0]);
		return 1;
	}
	int number = atoi(argv[1]);
	if (number != secret_number) {
		printf("Sorry, wrong number :C\n");
	} else {
		int secret_len = strlen(secret);
		for (size_t i = 0; i <= secret_len - sizeof(number); ++i) {
			unsigned int *ptr = (unsigned int *)(secret + i);
			*ptr = (*ptr) ^ number;
		}
		printf("Yay! Here's your flag: %s", secret);
	}
}
