#ifndef BROWSERHISTORY_H
#define BROWSERHISTORY_H

#include "DLLNode.h"
#include <string>
using namespace std;

class BrowserHistory {
private:
    DLLNode* head;
    DLLNode* current;
    int      size;

    string toLower(string s) const;
    void   printTableHeader() const;
    void   printPageRow(int index, DLLNode* node, bool isCurrent) const;

public:
    BrowserHistory();
    ~BrowserHistory();

    void  visit(Page p);
    bool  back();
    bool  forward();
    void  displayHistory() const;
    void  searchHistory(string keyword) const;
    bool  searchHistorySilent(string keyword) const;
    bool  deleteByUrl(string url);
    void  clearHistory();

    Page* getCurrentPage() const;
    bool  canGoBack() const;
    bool  canGoForward() const;
    int   getSize() const;
    bool  isEmpty() const;
};

#endif

