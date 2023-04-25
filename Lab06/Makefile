CC = g++
all:test_v test_a
test_v: test.cpp
	$(CC) -o test_v test.cpp

test_a: test.cpp
	$(CC) -fsanitize=address -g -o test_a test.cpp

clean:
	rm -f test_a
	rm -f test_v	
