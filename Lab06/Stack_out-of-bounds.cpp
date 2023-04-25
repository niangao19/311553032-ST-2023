#include <stdio.h>
int main(int argc, char** argv) {
    int stack_arr[100];

    stack_arr[100] = 1; // boom in write
    int res = stack_arr[argc+100]; // boom in read
    
    return res;
}
