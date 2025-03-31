all: TSP

algs.o: algs/algs.cpp
	g++ -c -o algs.o algs/algs.cpp

TSP: main.cpp algs.o
	g++ -o TSP main.cpp algs/algs.h algs.o
	rm -f *.o

clear:
	rm TSP