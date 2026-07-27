#include "../include/BrowserHistory.h"
#include "../include/CacheStack.h"
#include "../include/Benchmark.h"
#include <cassert>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>

using namespace std;

static void testHistoryNavigationAndTruncation() {
    BrowserHistory history;
    assert(history.isEmpty());
    assert(history.getSize() == 0);
    assert(!history.back());
    assert(!history.forward());

    history.visit(Page("https://a.com", "Page A", "10:00:00"));
    history.visit(Page("https://b.com", "Page B", "10:01:00"));
    history.visit(Page("https://c.com", "Page C", "10:02:00"));
    assert(history.getSize() == 3);
    assert(history.getCurrentPage()->url == "https://c.com");
    assert(history.canGoBack());
    assert(!history.canGoForward());

    assert(history.back());
    assert(history.getCurrentPage()->url == "https://b.com");
    assert(history.canGoForward());

    // Visiting from mid-history truncates forward branch (Page C)
    history.visit(Page("https://d.com", "Page D", "10:03:00"));
    assert(history.getSize() == 3);
    assert(!history.canGoForward());
    assert(history.getCurrentPage()->url == "https://d.com");
    assert(!history.searchHistorySilent("c.com"));
    cout << "[PASS] UT-01: BrowserHistory navigation and mid-history truncation\n";
}

static void testHistorySearchDeleteAndClear() {
    BrowserHistory history;
    history.visit(Page("https://one.dev", "One", "10:00:00"));
    history.visit(Page("https://two.dev", "Two", "10:01:00"));
    history.visit(Page("https://three.dev", "Three", "10:02:00"));

    assert(history.searchHistorySilent("TWO.DEV"));
    assert(!history.searchHistorySilent("missing.org"));

    // Delete middle node
    assert(history.deleteByUrl("https://two.dev"));
    assert(history.getSize() == 2);
    assert(!history.deleteByUrl("https://two.dev"));

    // Delete current tail node
    assert(history.deleteByUrl("https://three.dev"));
    assert(history.getSize() == 1);
    assert(history.getCurrentPage()->url == "https://one.dev");

    // Delete remaining head node
    assert(history.deleteByUrl("https://one.dev"));
    assert(history.isEmpty());

    history.visit(Page("https://reset.dev", "Reset", "10:05:00"));
    history.clearHistory();
    assert(history.isEmpty());
    cout << "[PASS] UT-02: BrowserHistory search, relink deletion, and clear\n";
}

static void testCacheStackDeduplicationAndEviction() {
    CacheStack cache(3);
    assert(cache.isEmpty());

    cache.push(Page("https://u1.com", "U1", "10:00:00"));
    cache.push(Page("https://u2.com", "U2", "10:01:00"));
    cache.push(Page("https://u1.com", "U1 Duplicate", "10:02:00")); // skipped
    assert(cache.getSize() == 2);
    assert(cache.peek()->url == "https://u2.com");

    cache.push(Page("https://u3.com", "U3", "10:03:00"));
    assert(cache.getSize() == 3);

    // Overflow capacity (3): bottom node (u1.com) must be evicted
    cache.push(Page("https://u4.com", "U4", "10:04:00"));
    assert(cache.getSize() == 3);
    assert(cache.pop().url == "https://u4.com");
    assert(cache.pop().url == "https://u3.com");
    assert(cache.pop().url == "https://u2.com");
    assert(cache.isEmpty());
    cout << "[PASS] UT-03: CacheStack deduplication and bottom eviction\n";
}

static void testTwoStackParity() {
    TwoStackSimulator sim;
    assert(!sim.back());
    assert(!sim.forward());

    sim.visit(Page("https://p1.org", "P1", "10:00:00"));
    sim.visit(Page("https://p2.org", "P2", "10:01:00"));
    sim.visit(Page("https://p3.org", "P3", "10:02:00"));
    assert(sim.back());
    assert(sim.back());
    assert(!sim.back());
    assert(sim.forward());
    assert(sim.searchHistory("https://p3.org"));
    assert(sim.deleteByUrl("https://p3.org"));
    assert(!sim.searchHistory("https://p3.org"));
    cout << "[PASS] UT-04: TwoStackSimulator navigation, search, and delete parity\n";
}

static void loadDatasetInto(const string& path, BrowserHistory& history, CacheStack& cache, int expectedRows) {
    ifstream file(path.c_str());
    assert(file.is_open());
    string line;
    int loaded = 0;
    while (getline(file, line)) {
        size_t comma = line.find(',');
        if (comma == string::npos) continue;
        Page p(line.substr(0, comma), line.substr(comma + 1), "12:00:00");
        history.visit(p);
        cache.push(p);
        loaded++;
    }
    assert(loaded == expectedRows);
    assert(history.getSize() == expectedRows);
    assert(cache.getSize() <= 100);
}

static void testGeneratedDatasetIngestion() {
    BrowserHistory h100;
    CacheStack c100(100);
    loadDatasetInto("datasets/data_100.txt", h100, c100, 100);

    BrowserHistory h1000;
    CacheStack c1000(100);
    loadDatasetInto("datasets/data_1000.txt", h1000, c1000, 1000);
    assert(c1000.getSize() == 100);
    cout << "[PASS] UT-05: Tracked dataset ingestion (100 and 1,000 rows, cache capped at 100)\n";
}

int main() {
    testHistoryNavigationAndTruncation();
    testHistorySearchDeleteAndClear();
    testCacheStackDeduplicationAndEviction();
    testTwoStackParity();
    testGeneratedDatasetIngestion();
    cout << "ALL 5 UNIT & DATASET TEST SUITES PASSED.\n";
    return 0;
}
