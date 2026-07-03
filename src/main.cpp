#include <iostream>
#include <string>
#include <fstream>
#include <chrono>
#include <iomanip>
#include <sstream>
#include "BrowserHistory.h"
#include "CacheStack.h"
#include "Utils.h"
#include "Benchmark.h"

using namespace std;

static string formatTime(double timeUs) {
    ostringstream ss;
    if (timeUs < 0.01 && timeUs > 0) {
        ss << scientific << setprecision(2) << timeUs;
    } else {
        ss << fixed << setprecision(2) << timeUs;
    }
    return ss.str();
}

void printMiniReport(string opName, double timeUs) {
    double actualRamKB = getActualRAMUsageKB();
    double opsPerSec = (timeUs > 0) ? (1000000.0 / timeUs) : 0;
    
    cout << "\n  [PERFORMANCE REPORT]\n";
    cout << "  - Operation    : " << opName << "\n";
    cout << "  - Elapsed Time : " << formatTime(timeUs) << " us\n";
    if (opsPerSec > 0) {
        if (opsPerSec >= 1e7) {
            cout << "  - Throughput   : ~" << scientific << setprecision(2) << opsPerSec << " Ops/sec\n" << fixed;
        } else {
            cout << "  - Throughput   : ~" << (long long)opsPerSec << " Ops/sec\n";
        }
    }
    cout << "  - Working Set  : " << actualRamKB << " KB\n";
}

void visitPage(BrowserHistory& history, CacheStack& cache) {
    cout << "\n--- VISIT NEW PAGE ---\n";
    string url   = getStringInput("  URL   : ");
    string title = getStringInput("  Title : ");
    Page   p(url, title, getCurrentTime());
    
    auto start = chrono::high_resolution_clock::now();
    history.visit(p);
    auto end = chrono::high_resolution_clock::now();
    
    cache.push(p);
    cout << "\n  [Visited] " << title << " (" << url << ")\n";
    
    double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
    printMiniReport("Visit Page", us == 0 ? 0.01 : us);
}

void goBack(BrowserHistory& history) {
    if (!history.canGoBack()) {
        cout << "\n  [Already at the beginning of history]\n";
        return;
    }
    
    auto start = chrono::high_resolution_clock::now();
    history.back();
    auto end = chrono::high_resolution_clock::now();
    
    Page* cur = history.getCurrentPage();
    cout << "\n  << Back | Now at: " << cur->title << " (" << cur->url << ")\n";
    
    double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
    printMiniReport("Go Back", us == 0 ? 0.01 : us);
}

void goForward(BrowserHistory& history) {
    if (!history.canGoForward()) {
        cout << "\n  [Already at the latest page]\n";
        return;
    }
    
    auto start = chrono::high_resolution_clock::now();
    history.forward();
    auto end = chrono::high_resolution_clock::now();
    
    Page* cur = history.getCurrentPage();
    cout << "\n  >> Forward | Now at: " << cur->title << " (" << cur->url << ")\n";
    
    double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
    printMiniReport("Go Forward", us == 0 ? 0.01 : us);
}

void showCurrentPage(const BrowserHistory& history) {
    Page* cur = history.getCurrentPage();
    if (cur == nullptr) {
        cout << "\n  [No page currently open]\n";
        return;
    }
    cout << "\n  --- CURRENT PAGE ---\n";
    cout << "    URL   : " << cur->url       << "\n";
    cout << "    Title : " << cur->title     << "\n";
    cout << "    Time  : " << cur->visitTime << "\n";
    cout << "    Back  : " << (history.canGoBack()    ? "Yes" : "No") << "\n";
    cout << "    Fwd   : " << (history.canGoForward() ? "Yes" : "No") << "\n";
}

void deletePage(BrowserHistory& history) {
    if (history.isEmpty()) {
        cout << "\n  [History is empty]\n";
        return;
    }
    string url = getStringInput("\n  Enter URL to delete: ");
    
    auto start = chrono::high_resolution_clock::now();
    bool success = history.deleteByUrl(url);
    auto end = chrono::high_resolution_clock::now();
    
    if (success)
        cout << "\n  [SUCCESS] Deleted \"" << url << "\" from history.\n";
    else
        cout << "\n  [NOT FOUND] \"" << url << "\" is not in history.\n";
        
    double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
    printMiniReport("Delete Page", us == 0 ? 0.01 : us);
}

void searchPage(BrowserHistory& history) {
    string kw = getStringInput("\n  Search keyword: ");
    
    auto start = chrono::high_resolution_clock::now();
    history.searchHistorySilent(kw);
    auto end = chrono::high_resolution_clock::now();
    
    history.searchHistory(kw);
    double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
    printMiniReport("Search History", us == 0 ? 0.01 : us);
}

void loadDataFromFile(BrowserHistory& history, CacheStack& cache) {
    cout << "\n--- LOAD DATA FROM FILE ---\n";
    cout << "  Select dataset size to load:\n";
    cout << "  1. 10 records\n";
    cout << "  2. 100 records\n";
    cout << "  3. 1,000 records\n";
    cout << "  4. 5,000 records\n";
    cout << "  5. 10,000 records\n";
    cout << "  0. Cancel\n";
    
    int choice = getIntInput("  Enter choice: ");
    string filename = "";
    if (choice == 1) filename = "datasets/data_10.txt";
    else if (choice == 2) filename = "datasets/data_100.txt";
    else if (choice == 3) filename = "datasets/data_1000.txt";
    else if (choice == 4) filename = "datasets/data_5000.txt";
    else if (choice == 5) filename = "datasets/data_10000.txt";
    else {
        cout << "  [Cancelled]\n";
        return;
    }
    
    ifstream file(filename);
    if (!file.is_open()) {
        cout << "  [ERROR] Cannot open " << filename << ".\n";
        cout << "  Make sure you run the python script first.\n";
        return;
    }
    
    history.clearHistory();
    cache.clearCache();
    
    cout << "  Reading and loading data into memory...\n";
    
    int count = 0;
    string line;
    
    auto start = chrono::high_resolution_clock::now();
    while (getline(file, line)) {
        size_t pos1 = line.find(',');
        if (pos1 == string::npos) continue;
        
        string url = line.substr(0, pos1);
        string title = line.substr(pos1 + 1);
        string timeStr = getCurrentTime();
        
        Page p(url, title, timeStr);
        history.visit(p);
        cache.push(p);
        count++;
    }
    file.close();
    auto end = chrono::high_resolution_clock::now();
    
    cout << "  [SUCCESS] " << count << " pages loaded from file!\n";
    
    double us = chrono::duration_cast<chrono::nanoseconds>(end - start).count() / 1000.0;
    printMiniReport("Load File Data", us == 0 ? 0.01 : us);
}



int main() {
    BrowserHistory history;
    CacheStack     cache(100);

    // loadSampleData(history, cache); // Start with an empty history by default
    cout << "\nWelcome to Browser History Manager!\n";
    cout << "  (History is initially empty)\n";

    int choice;
    do {
        cout << "\n================================\n";
        cout << "   BROWSER HISTORY MANAGER\n";
        cout << "================================\n";
        cout << "  1. Visit new page\n";
        cout << "  2. Go Back\n";
        cout << "  3. Go Forward\n";
        cout << "  4. Display history\n";
        cout << "  5. Search in history\n";
        cout << "  6. Delete page from history\n";
        cout << "  7. Clear history & cache\n";
        cout << "  8. Display cache\n";
        cout << "  9. Current page info\n";
        cout << " 10. Run Performance Benchmark\n";
        cout << " 11. Load Data From File (Custom Size)\n";
        cout << "  0. Exit\n";
        cout << "================================\n";
        choice = getIntInput("  Enter your choice: ");

        switch (choice) {
            case 1: visitPage(history, cache); break;
            case 2: goBack(history);           break;
            case 3: goForward(history);        break;
            case 4: history.displayHistory();  break;
            case 5: searchPage(history); break;
            case 6: deletePage(history);   break;
            case 7:
                history.clearHistory();
                cache.clearCache();
                cout << "\n  [Cleared] History and cache have been cleared.\n";
                break;
            case 8: cache.displayCache();  break;
            case 9: showCurrentPage(history); break;
            case 10: runPerformanceBenchmark(); break;
            case 11: loadDataFromFile(history, cache); break;
            case 0: cout << "\nGoodbye!\n"; break;
            default:
                cout << "\n  [ERROR] Invalid choice. Please enter 0-11.\n";
        }
    } while (choice != 0);

    return 0;
}

