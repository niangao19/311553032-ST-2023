#include <stdio.h>
int global_arr[100];

int main(int argv, char** argc) {
    global_arr[100] = 1; // boom in write
    int res = global_arr[100]; // boom in read

    return res;
}
