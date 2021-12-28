bin/GA_color:src/shape.o src/main.o src/genetic.o
	g++ -std=c++11 shape.o main.o genetic.o -o bin/GA_color 
src/main.o:src/shape.h src/genetic.h src/main.cpp
	g++ -std=c++11 -c src/main.cpp
src/shape.o:src/shape.h src/shape.cpp
	g++ -std=c++11 -c src/shape.cpp
src/genetic.o:src/shape.h src/genetic.h src/genetic.cpp 
	g++ -std=c++11 -c src/genetic.cpp

clean:
	rm -rf *.o bin/GA_color
