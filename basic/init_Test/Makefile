CXXFLAGS = `pkg-config --cflags opencv` -g -O2
LDLIBS   = `pkg-config --libs opencv`

CC  = gcc
CXX = g++
LD  = g++

EXE  = main

SRCS = $(wildcard *.cpp)
OBJS = $(SRCS: .cpp=.o)

all: $(EXE)

$(EXE): $(OBJS)

%.cpp : %.h

.PHONY: clean

clean:
	rm -rf $(EXE) *.o
