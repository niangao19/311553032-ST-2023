#include <stdio.h>
int main(int argc, char **argv) {
    int SIZE = 100;
    int *arr = new int[SIZE];
    int res = arr[argc+SIZE]; // boom in read
    arr[argc+SIZE] = 1;  // boom in write

    delete [] arr;
    return res;
}
