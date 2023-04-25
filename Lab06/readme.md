# Lab06 Valgrind & Asan
### Environment
- Language: C++
- Debugger: gdb
- machine: Ubuntu 11.3.0-1ubuntu1~22.04
- Compiler: g++
- g++ version: 11.3.0
```makefile=
CC = g++
all:test_v test_a
test_v: test.cpp
	$(CC) -o test_v test.cpp

test_a: test.cpp
	$(CC) -fsanitize=address -g -o test_a test.cpp
```
### Heap out-of-bounds read/write
#### Source Code
```cpp=
#include <stdio.h>
int main(int argc, char **argv) {
    int SIZE = 100;
    int *arr = new int[SIZE];
    int res = arr[argc+SIZE]; // boom in read
    arr[argc+SIZE] = 1;  // boom in write

    delete [] arr;
    return res;
}
```
#### ASan report
```
hmnmax@7ffb996a1894:~/lab6$ ./test_a
=================================================================
==106==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xffff81303fd4 at pc 0xaaaad0f80b00 bp 0xffffedd8ebf0 sp 0xffffedd8ec00
READ of size 4 at 0xffff81303fd4 thread T0
    #0 0xaaaad0f80afc in main /home/hmnmax/lab6/test.cpp:5
    #1 0xffff84b673f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffff84b674c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaad0f8096c in _start (/home/hmnmax/lab6/test_a+0x96c)

0xffff81303fd4 is located 4 bytes to the right of 400-byte region [0xffff81303e40,0xffff81303fd0)
allocated by thread T0 here:
    #0 0xffff8509bcec in operator new[](unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:102
    #1 0xaaaad0f80a80 in main /home/hmnmax/lab6/test.cpp:4
    #2 0xffff84b673f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #3 0xffff84b674c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #4 0xaaaad0f8096c in _start (/home/hmnmax/lab6/test_a+0x96c)

SUMMARY: AddressSanitizer: heap-buffer-overflow /home/hmnmax/lab6/test.cpp:5 in main
Shadow bytes around the buggy address:
  0x200ff02607a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff02607b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff02607c0: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
  0x200ff02607d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff02607e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x200ff02607f0: 00 00 00 00 00 00 00 00 00 00[fa]fa fa fa fa fa
  0x200ff0260800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0260810: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0260820: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0260830: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff0260840: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==106==ABORTING
```
#### Valgrind report
```
hmnmax@7ffb996a1894:~/lab6$ make
g++ -o test_v test.cpp
g++ -fsanitize=address -g -o test_a test.cpp
hmnmax@7ffb996a1894:~/lab6$ make
g++ -o test_v test.cpp
g++ -fsanitize=address -g -o test_a test.cpp
hmnmax@7ffb996a1894:~/lab6$ valgrind ./test_a
==102== Memcheck, a memory error detector
==102== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==102== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==102== Command: ./test_a
==102== 
==102==ASan runtime does not come first in initial library list; you should either link runtime to your application or manually preload it with LD_PRELOAD.
==102== 
==102== HEAP SUMMARY:
==102==     in use at exit: 0 bytes in 0 blocks
==102==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==102== 
==102== All heap blocks were freed -- no leaks are possible
==102== 
==102== For lists of detected and suppressed errors, rerun with: -s
==102== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
> ASan能Valgrind能

### Stack out-of-bounds read/write
#### Source Code
```cpp=
#include <stdio.h>
int main(int argc, char** argv) {
    int stack_arr[100];

    stack_arr[100] = 1; // boom in write
    int res = stack_arr[argc+100]; // boom in read
    
    return res;
}
```
#### ASan report
```
hmnmax@7ffb996a1894:~/lab6$ ./test_a
=================================================================
==133==ERROR: AddressSanitizer: stack-buffer-overflow on address 0xffffc2b058f0 at pc 0xaaaabbba0b54 bp 0xffffc2b056d0 sp 0xffffc2b056e0
WRITE of size 4 at 0xffffc2b058f0 thread T0
    #0 0xaaaabbba0b50 in main /home/hmnmax/lab6/test.cpp:5
    #1 0xffff917173f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffff917174c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaabbba096c in _start (/home/hmnmax/lab6/test_a+0x96c)

Address 0xffffc2b058f0 is located in stack of thread T0 at offset 448 in frame
    #0 0xaaaabbba0a60 in main /home/hmnmax/lab6/test.cpp:2

  This frame has 1 object(s):
    [48, 448) 'stack_arr' (line 3) <== Memory access at offset 448 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /home/hmnmax/lab6/test.cpp:5 in main
Shadow bytes around the buggy address:
  0x200ff8560ac0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8560ad0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8560ae0: 00 00 00 00 00 00 f1 f1 f1 f1 f1 f1 00 00 00 00
  0x200ff8560af0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8560b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x200ff8560b10: 00 00 00 00 00 00 00 00 00 00 00 00 00 00[f3]f3
  0x200ff8560b20: f3 f3 f3 f3 f3 f3 00 00 00 00 00 00 00 00 00 00
  0x200ff8560b30: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8560b40: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8560b50: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff8560b60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==133==ABORTING
```
#### Valgrind report
```
hmnmax@7ffb996a1894:~/lab6$ valgrind ./test_v
==132== Memcheck, a memory error detector
==132== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==132== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==132== Command: ./test_v
==132== 
*** stack smashing detected ***: terminated
==132== 
==132== Process terminating with default action of signal 6 (SIGABRT)
==132==    at 0x490F200: __pthread_kill_implementation (pthread_kill.c:44)
==132==    by 0x48CA67B: raise (raise.c:26)
==132==    by 0x48B712F: abort (abort.c:79)
==132==    by 0x4903307: __libc_message (libc_fatal.c:155)
==132==    by 0x4985897: __fortify_fail (fortify_fail.c:26)
==132==    by 0x4985863: __stack_chk_fail (stack_chk_fail.c:24)
==132==    by 0x108883: main (in /home/hmnmax/lab6/test_v)
==132== 
==132== HEAP SUMMARY:
==132==     in use at exit: 0 bytes in 0 blocks
==132==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==132== 
==132== All heap blocks were freed -- no leaks are possible
==132== 
==132== For lists of detected and suppressed errors, rerun with: -s
==132== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
Aborted
```
> ASan能Valgrind不能
### Global out-of-bounds read/write
#### Source Code
```cpp=
#include <stdio.h>
int global_arr[100];

int main(int argv, char** argc) {
    global_arr[100] = 1; // boom in write
    int res = global_arr[100]; // boom in read

    return res;
}
```
#### ASan report
```
hmnmax@7ffb996a1894:~/lab6$ ./test_a
=================================================================
==145==ERROR: AddressSanitizer: global-buffer-overflow on address 0xaaaac5bb1210 at pc 0xaaaac5ba0a70 bp 0xffffcccee010 sp 0xffffcccee020
WRITE of size 4 at 0xaaaac5bb1210 thread T0
    #0 0xaaaac5ba0a6c in main /home/hmnmax/lab6/test.cpp:5
    #1 0xffffae5e73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffffae5e74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaac5ba092c in _start (/home/hmnmax/lab6/test_a+0x92c)

0xaaaac5bb1210 is located 0 bytes to the right of global variable 'global_arr' defined in 'test.cpp:2:5' (0xaaaac5bb1080) of size 400
SUMMARY: AddressSanitizer: global-buffer-overflow /home/hmnmax/lab6/test.cpp:5 in main
Shadow bytes around the buggy address:
  0x156558b761f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x156558b76200: 00 00 00 00 f9 f9 f9 f9 f9 f9 f9 f9 00 00 00 00
  0x156558b76210: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x156558b76220: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x156558b76230: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x156558b76240: 00 00[f9]f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00
  0x156558b76250: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x156558b76260: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x156558b76270: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x156558b76280: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x156558b76290: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==145==ABORTING
```
#### Valgrind report
```
hmnmax@7ffb996a1894:~/lab6$ valgrind ./test_v
==147== Memcheck, a memory error detector
==147== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==147== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==147== Command: ./test_v
==147== 
==147== 
==147== HEAP SUMMARY:
==147==     in use at exit: 0 bytes in 0 blocks
==147==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==147== 
==147== All heap blocks were freed -- no leaks are possible
==147== 
==147== For lists of detected and suppressed errors, rerun with: -s
==147== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
> ASan能Valgrind不能

### Use-after-free
#### Source Code
```cpp=
#include <stdio.h>

int main(int argc, char** argv) {
    int *arr = new int[50];
    delete [] arr;
    
    int res = arr[1]; // boom
    return res;
}
```
#### ASan report
```
hmnmax@7ffb996a1894:~/lab6$ ./test_a
=================================================================
==160==ERROR: AddressSanitizer: heap-use-after-free on address 0xffffa8b03ec4 at pc 0xaaaad9450998 bp 0xffffc1bbcc20 sp 0xffffc1bbcc30
READ of size 4 at 0xffffa8b03ec4 thread T0
    #0 0xaaaad9450994 in main /home/hmnmax/lab6/test.cpp:7
    #1 0xffffaccb73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffffaccb74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaad945082c in _start (/home/hmnmax/lab6/test_a+0x82c)

0xffffa8b03ec4 is located 4 bytes inside of 200-byte region [0xffffa8b03ec0,0xffffa8b03f88)
freed by thread T0 here:
    #0 0xffffad1ec734 in operator delete[](void*) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:163
    #1 0xaaaad9450940 in main /home/hmnmax/lab6/test.cpp:5
    #2 0xffffaccb73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #3 0xffffaccb74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #4 0xaaaad945082c in _start (/home/hmnmax/lab6/test_a+0x82c)

previously allocated by thread T0 here:
    #0 0xffffad1ebcec in operator new[](unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:102
    #1 0xaaaad9450928 in main /home/hmnmax/lab6/test.cpp:4
    #2 0xffffaccb73f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #3 0xffffaccb74c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #4 0xaaaad945082c in _start (/home/hmnmax/lab6/test_a+0x82c)

SUMMARY: AddressSanitizer: heap-use-after-free /home/hmnmax/lab6/test.cpp:7 in main
Shadow bytes around the buggy address:
  0x200ff5160780: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff5160790: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff51607a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff51607b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff51607c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
=>0x200ff51607d0: fa fa fa fa fa fa fa fa[fd]fd fd fd fd fd fd fd
  0x200ff51607e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x200ff51607f0: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff5160800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff5160810: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x200ff5160820: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==160==ABORTING
```
#### Valgrind report
```
hmnmax@7ffb996a1894:~/lab6$ valgrind ./test_v
==161== Memcheck, a memory error detector
==161== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==161== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==161== Command: ./test_v
==161== 
==161== Invalid read of size 4
==161==    at 0x108848: main (in /home/hmnmax/lab6/test_v)
==161==  Address 0x4d46c84 is 4 bytes inside a block of size 200 free'd
==161==    at 0x48690B0: operator delete[](void*) (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==161==    by 0x108843: main (in /home/hmnmax/lab6/test_v)
==161==  Block was alloc'd at
==161==    at 0x4866AE8: operator new[](unsigned long) (in /usr/libexec/valgrind/vgpreload_memcheck-arm64-linux.so)
==161==    by 0x10882B: main (in /home/hmnmax/lab6/test_v)
==161== 
==161== 
==161== HEAP SUMMARY:
==161==     in use at exit: 0 bytes in 0 blocks
==161==   total heap usage: 2 allocs, 2 frees, 72,904 bytes allocated
==161== 
==161== All heap blocks were freed -- no leaks are possible
==161== 
==161== For lists of detected and suppressed errors, rerun with: -s
==161== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```
> ASan能Valgrind能
### Use-after-return
#### Source Code
```cpp=
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
```
#### ASan report
**執行指令要改成ASAN_OPTIONS=detect_stack_use_after_return=1 ./test_a**
```
hmnmax@7ffb996a1894:~/lab6$ ASAN_OPTIONS=detect_stack_use_after_return=1 ./test_a
=================================================================
==211==ERROR: AddressSanitizer: stack-use-after-return on address 0xffffad4dc03f at pc 0xaaaac3100d24 bp 0xffffd2696a50 sp 0xffffd2696a60
WRITE of size 1 at 0xffffad4dc03f thread T0
    #0 0xaaaac3100d20 in main /home/hmnmax/lab6/test.cpp:13
    #1 0xffffb09773f8 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0xffffb09774c8 in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0xaaaac3100aac in _start (/home/hmnmax/lab6/test_a+0xaac)

Address 0xffffad4dc03f is located in stack of thread T0 at offset 63 in frame
    #0 0xaaaac3100ba0 in foo() /home/hmnmax/lab6/test.cpp:5

  This frame has 1 object(s):
    [48, 148) 'arr' (line 6) <== Memory access at offset 63 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return /home/hmnmax/lab6/test.cpp:13 in main
Shadow bytes around the buggy address:
  0x200ff5a9b7b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff5a9b7c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff5a9b7d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff5a9b7e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff5a9b7f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x200ff5a9b800: f5 f5 f5 f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5 f5 f5
  0x200ff5a9b810: f5 f5 f5 f5 f5 f5 f5 f5 00 00 00 00 00 00 00 00
  0x200ff5a9b820: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff5a9b830: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff5a9b840: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x200ff5a9b850: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==211==ABORTING
```
#### Valgrind report
```
hmnmax@7ffb996a1894:~/lab6$ valgrind ./test_v
==176== Memcheck, a memory error detector
==176== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==176== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==176== Command: ./test_v
==176== 
==176== Invalid write of size 1
==176==    at 0x10888C: main (in /home/hmnmax/lab6/test_v)
==176==  Address 0x1fff00097f is on thread 1's stack
==176==  97 bytes below stack pointer
==176== 
==176== 
==176== HEAP SUMMARY:
==176==     in use at exit: 0 bytes in 0 blocks
==176==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==176== 
==176== All heap blocks were freed -- no leaks are possible
==176== 
==176== For lists of detected and suppressed errors, rerun with: -s
==176== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```
> ASan能Valgrind不能




### Outcome
|  | Valgrind | ASan |
| -------- | -------- | -------- |
| Heap out-of-bounds read/write     | V     | V   |
| Stack out-of-bounds read/write     |  X   |   V |
| Global out-of-bounds read/write     |   X   |   V |
| Use-after-free     |V    | V   |
| Use-after-return  | X    | V     |
### redzone
#### Source Code
```cpp=
#include <stdio.h>

int main(int argc, char** argv) {
    int *a = new int[8];
    int *b = new int[8];

    int res = a[argc+12];

    delete [] a;
    delete [] b;
    return 0;
}

```
#### ASan report
```
hmnmax@7ffb996a1894:~/lab6$ ./test_a
無
```
