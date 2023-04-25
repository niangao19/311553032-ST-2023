#include <stdio.h>

char* x;

void foo() {
    char arr[100];
    x = &arr[15];
}

int main() {

    foo();
    *x = 'a'; // boom

    return 0;
}
