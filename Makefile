CXX      := g++
CXXFLAGS := -std=c++11 -O2 -Wall -Wextra -Iinclude
LDFLAGS  := -lpsapi

SRCS := src/main.cpp \
        src/BrowserHistory.cpp \
        src/CacheStack.cpp \
        src/Utils.cpp \
        benchmarks/Benchmark.cpp

TARGET := browser_history.exe

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) $(LDFLAGS) -o $(TARGET)

clean:
	del /Q $(TARGET) 2>nul || rm -f $(TARGET)

.PHONY: all clean
