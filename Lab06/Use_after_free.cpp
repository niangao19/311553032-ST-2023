#include <stdio.h>

int main(int argc, char** argv) {
    int *arr = new int[50];
    delete [] arr;
    
    int res = arr[1]; // boom
    return res;
}
