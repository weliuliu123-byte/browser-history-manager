CXX      := g++
CXXFLAGS := -std=c++11 -O2 -Wall -Wextra -Iinclude
LDFLAGS  := -lpsapi

SRCS := src/main.cpp \
        src/BrowserHistory.cpp \
        src/CacheStack.cpp \
        src/Utils.cpp \
        benchmarks/Benchmark.cpp

TARGET      := browser_history.exe
TEST_TARGET := test_suite.exe

TEST_SRCS := tests/test_history_and_cache.cpp \
             src/BrowserHistory.cpp \
             src/CacheStack.cpp \
             src/Utils.cpp \
             benchmarks/Benchmark.cpp

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) $(LDFLAGS) -o $(TARGET)

test: $(TEST_SRCS)
	$(CXX) $(CXXFLAGS) $(TEST_SRCS) $(LDFLAGS) -o $(TEST_TARGET)
	./$(TEST_TARGET)

clean:
	del /Q $(TARGET) $(TEST_TARGET) 2>nul || rm -f $(TARGET) $(TEST_TARGET)

.PHONY: all test clean
