#include "Benchmark.h"
#include "Utils.h"
#include <iostream>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <windows.h>
using namespace std;

TwoStackSimulator::TwoStackSimulator() : current(nullptr) {}
TwoStackSimulator::~TwoStackSimulator() { delete current; }

void TwoStackSimulator::visit(Page p) {
    if (current) {
        backStack.push(*current);
        delete current;
    }
    current = new Page(p);
    while (!forwardStack.empty()) forwardStack.pop();
}

bool TwoStackSimulator::back() {
    if (backStack.empty()) return false;
    if (current) forwardStack.push(*current);
    current = new Page(backStack.top());
    backStack.pop();
    return true;
}

bool TwoStackSimulator::forward() {
    if (forwardStack.empty()) return false;
    if (current) backStack.push(*current);
    current = new Page(forwardStack.top());
    forwardStack.pop();
    return true;
}

bool TwoStackSimulator::searchHistory(string keyword) {
    bool found = false;
    stack<Page> temp;
    if (current && current->url == keyword) found = true;
    
    while (!backStack.empty()) {
        if (backStack.top().url == keyword) found = true;
        temp.push(backStack.top());
        backStack.pop();
    }
    while (!temp.empty()) {
        backStack.push(temp.top());
        temp.pop();
    }
    // Also search forwardStack
    while (!forwardStack.empty()) {
        if (forwardStack.top().url == keyword) found = true;
        temp.push(forwardStack.top());
        forwardStack.pop();
    }
    while (!temp.empty()) {
        forwardStack.push(temp.top());
        temp.pop();
    }
    return found;
}

bool TwoStackSimulator::deleteByUrl(string url) {
    // Check current page
    if (current && current->url == url) {
        delete current;
        current = nullptr;
        return true;
    }
    // Check backStack
    bool deleted = false;
    stack<Page> temp;
    while (!backStack.empty()) {
        if (!deleted && backStack.top().url == url) {
            deleted = true;
            backStack.pop();
            break;
        }
        temp.push(backStack.top());
        backStack.pop();
    }
    while (!temp.empty()) {
        backStack.push(temp.top());
        temp.pop();
    }
    if (deleted) return true;
    // Check forwardStack
    while (!forwardStack.empty()) {
        if (forwardStack.top().url == url) {
            deleted = true;
            forwardStack.pop();
            break;
        }
        temp.push(forwardStack.top());
        forwardStack.pop();
    }
    while (!temp.empty()) {
        forwardStack.push(temp.top());
        temp.pop();
    }
    return deleted;
}

template <typename Func>
double measureExecutionTime(int iterations, Func func) {
#ifdef _WIN32
    LARGE_INTEGER frequency;
    LARGE_INTEGER start, end;
    QueryPerformanceFrequency(&frequency);
    QueryPerformanceCounter(&start);
    for (int i = 0; i < iterations; i++) {
        func();
    }
    QueryPerformanceCounter(&end);
    double total_us = (end.QuadPart - start.QuadPart) * 1000000.0 / frequency.QuadPart;
    double avg_us = total_us / iterations;
    return avg_us == 0 ? 1e-9 : avg_us;
#else
    auto start = chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; i++) {
        func();
    }
    auto end = chrono::high_resolution_clock::now();
    double total_us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
    double avg_us = total_us / iterations;
    return avg_us <= 0 ? 1e-9 : avg_us;
#endif
}

string formatOps(double timeUs) {
    double ops = 1e6 / timeUs;
    ostringstream ss;
    if (ops >= 1e7) {
        ss << scientific << setprecision(2) << ops;
        // Clean up string like "1.00e+008" to "1.00e+08" if needed, but default is fine
    } else {
        ss << (long long)ops;
    }
    return ss.str();
}

static string formatTime(double timeUs) {
    ostringstream ss;
    if (timeUs < 0.01 && timeUs > 0) {
        ss << scientific << setprecision(2) << timeUs;
    } else {
        ss << fixed << setprecision(2) << timeUs;
    }
    return ss.str();
}

void runPerformanceBenchmark() {
    cout << "\n--- PERFORMANCE BENCHMARK ---\n";
    cout << "  Running sequential tests (N = 10, 100, 1000, 5000, 10000)...\n";
    
    int milestones[] = {10, 100, 1000, 5000, 10000};
    
    cout << fixed << setprecision(2);

    
    for (int i = 0; i < 5; i++) {
        int n = milestones[i];
        double dll_before = getActualRAMUsageKB();
        BrowserHistory dllHistory;
        for (int j = 1; j <= n; j++) {
            Page p("url_" + to_string(j) + ".com", "Title", "12:00");
            dllHistory.visit(p);
        }
        double dll_after = getActualRAMUsageKB();
        double actual_dll_ram = dll_after - dll_before;

        double ts_before = getActualRAMUsageKB();
        TwoStackSimulator tsHistory;
        for (int j = 1; j <= n; j++) {
            Page p("url_" + to_string(j) + ".com", "Title", "12:00");
            tsHistory.visit(p);
        }
        double ts_after = getActualRAMUsageKB();
        double actual_ts_ram = ts_after - ts_before;
        
        string target = "url_" + to_string(n / 2) + ".com";
        
        
        double dlls = measureExecutionTime(1000, [&]() { dllHistory.searchHistorySilent(target); });
        double tss  = measureExecutionTime(1000, [&]() { tsHistory.searchHistory(target); });
        double dlld = measureExecutionTime(1000, [&]() { dllHistory.deleteByUrl(target); });
        double tssd = measureExecutionTime(1000, [&]() { tsHistory.deleteByUrl(target); });
        
        double dllb = measureExecutionTime(1000, [&]() { dllHistory.back(); });
        double tsb  = measureExecutionTime(1000, [&]() { tsHistory.back(); });
        double dllf = measureExecutionTime(1000, [&]() { dllHistory.forward(); });
        double tsf  = measureExecutionTime(1000, [&]() { tsHistory.forward(); });
        

        
        cout << "\n[ N = " << n << " ]\n";
        cout << "  [Memory Delta] DLL: " << actual_dll_ram << " KB  |  Two-Stack: " << actual_ts_ram << " KB\n";
        cout << "  --------------------------------------------------------------\n";
        cout << "  | Operation |  DLL Time (us) |   TS Time (us) | DLL Ops/sec |\n";
        cout << "  --------------------------------------------------------------\n";
        cout << "  | Search    | " << setw(14) << formatTime(dlls) << " | " << setw(14) << formatTime(tss) << " | " << setw(11) << formatOps(dlls) << " |\n";
        cout << "  | Delete    | " << setw(14) << formatTime(dlld) << " | " << setw(14) << formatTime(tssd) << " | " << setw(11) << formatOps(dlld) << " |\n";
        cout << "  | Back      | " << setw(14) << formatTime(dllb) << " | " << setw(14) << formatTime(tsb) << " | " << setw(11) << formatOps(dllb) << " |\n";
        cout << "  | Forward   | " << setw(14) << formatTime(dllf) << " | " << setw(14) << formatTime(tsf) << " | " << setw(11) << formatOps(dllf) << " |\n";
        cout << "  --------------------------------------------------------------\n";
    }
}

