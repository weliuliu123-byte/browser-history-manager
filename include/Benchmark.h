#ifndef BENCHMARK_H
#define BENCHMARK_H

#include "BrowserHistory.h"
#include "CacheStack.h"
#include <stack>
#include <string>

class TwoStackSimulator {
private:
    std::stack<Page> backStack;
    std::stack<Page> forwardStack;
    Page* current;
public:
    TwoStackSimulator();
    ~TwoStackSimulator();
    void visit(Page p);
    bool searchHistory(std::string keyword);
    bool deleteByUrl(std::string url);
    bool back();
    bool forward();
};

void runPerformanceBenchmark();

#endif

