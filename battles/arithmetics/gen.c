#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
	if (argc < 2) {
		fprintf(stderr, "Missing argument, usage: %s <number>\n", argv[0]);
		return 1;
	}

	char *str = NULL;
	size_t buf_size = 0;
	getline(&str, &buf_size, stdin);
	
	int number = atoi(argv[1]);
	int str_len = strlen(str);

	printf("str_len: %d\n", str_len);
	printf("number: %d\n", number);

	for (int i = 0; i <= str_len - sizeof(number); ++i) {
		printf("%d\n", i);
		*(unsigned int *)(str + i) = (*(unsigned int *)(str + i)) ^ number;
	}

	printf("encrypted\n");

	for (int i = 0; i < str_len; ++i) {
		printf("\\x%02x", *(unsigned char *)(str + i));
	}
	printf("\n");
	printf("%s\n", str);
}
