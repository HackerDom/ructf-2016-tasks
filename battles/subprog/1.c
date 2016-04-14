#include <stdio.h>

#define LENGTH(X) (sizeof(X)/sizeof(*X))

void main() {
    char answer[] = {
        77, 45, 4, 13,
        14, 70, 73, 6,
        70, 123, 45, 61,
        27, 31
    };

    size_t N = LENGTH(answer);

    for (size_t i = 0; i < N; ++i) {
        char tmp = answer[i];
        answer[i] = answer[(N - 1) - i];
        answer[(N - 1) - i] = tmp;
    }

    for (size_t i = 0; i < N; ++i) {
        if (i > 0)
            answer[i] = answer[i - 1] ^ i ^ answer[i];

        printf("%c", answer[i]);
    }
}
