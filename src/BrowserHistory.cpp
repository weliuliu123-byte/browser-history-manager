#include "BrowserHistory.h"
#include <iostream>
#include <iomanip>
using namespace std;

BrowserHistory::BrowserHistory() : head(nullptr), current(nullptr), size(0) {}

BrowserHistory::~BrowserHistory() {
    clearHistory();
}

string BrowserHistory::toLower(string s) const {
    for (char& c : s) c = tolower(c);
    return s;
}

void BrowserHistory::printTableHeader() const {
    cout << left
         << setw(5)  << "#"
         << setw(32) << "URL"
         << setw(25) << "Title"
         << setw(10) << "Time"
         << setw(10) << "Status"
         << "\n";
    cout << string(82, '-') << "\n";
}

void BrowserHistory::printPageRow(int index, DLLNode* node, bool isCurrent) const {
    cout << left
         << setw(5)  << index
         << setw(32) << node->data.url
         << setw(25) << node->data.title
         << setw(10) << node->data.visitTime
         << setw(10) << (isCurrent ? "<< HERE" : "")
         << "\n";
}

void BrowserHistory::visit(Page p) {
    // Delete all forward nodes when visiting a new page from mid-history
    if (current != nullptr && current->next != nullptr) {
        DLLNode* toDelete = current->next;
        current->next = nullptr;
        while (toDelete != nullptr) {
            DLLNode* next = toDelete->next;
            delete toDelete;
            toDelete = next;
            size--;
        }
    }

    DLLNode* newNode = new DLLNode(p);

    if (head == nullptr) {
        head = newNode;
    } else {
        current->next  = newNode;
        newNode->prev  = current;
    }

    current = newNode;
    size++;
}

bool BrowserHistory::back() {
    if (current == nullptr || current->prev == nullptr) return false;
    current = current->prev;
    return true;
}

bool BrowserHistory::forward() {
    if (current == nullptr || current->next == nullptr) return false;
    current = current->next;
    return true;
}

void BrowserHistory::displayHistory() const {
    if (isEmpty()) {
        cout << "\n  [History is empty]\n";
        return;
    }

    cout << "\n=== BROWSER HISTORY (" << size << " pages) ===\n";
    printTableHeader();

    DLLNode* node = head;
    int index = 1;
    while (node != nullptr) {
        printPageRow(index, node, node == current);
        node = node->next;
        index++;
    }
    cout << string(82, '-') << "\n";
    cout << "  Back: " << (canGoBack()    ? "Yes" : "No")
         << "   Forward: " << (canGoForward() ? "Yes" : "No") << "\n";
}

void BrowserHistory::searchHistory(string keyword) const {
    string keyLower = toLower(keyword);
    bool   found    = false;
    int    index    = 1;

    cout << "\n[SEARCH RESULTS for \"" << keyword << "\"]\n";
    printTableHeader();

    DLLNode* node = head;
    while (node != nullptr) {
        bool matchUrl   = toLower(node->data.url).find(keyLower)   != string::npos;
        bool matchTitle = toLower(node->data.title).find(keyLower) != string::npos;
        if (matchUrl || matchTitle) {
            printPageRow(index, node, node == current);
            found = true;
        }
        node = node->next;
        index++;
    }

    if (!found)
        cout << "  No results found for \"" << keyword << "\".\n";
}

bool BrowserHistory::searchHistorySilent(string keyword) const {
    string keyLower = toLower(keyword);
    DLLNode* node = head;
    while (node != nullptr) {
        bool matchUrl   = toLower(node->data.url).find(keyLower)   != string::npos;
        bool matchTitle = toLower(node->data.title).find(keyLower) != string::npos;
        if (matchUrl || matchTitle) return true;
        node = node->next;
    }
    return false;
}

bool BrowserHistory::deleteByUrl(string url) {
    string urlLower = toLower(url);
    DLLNode* node = head;

    while (node != nullptr) {
        if (toLower(node->data.url) == urlLower) {
            // Move current pointer if deleting current node
            if (node == current) {
                if      (node->prev) current = node->prev;
                else if (node->next) current = node->next;
                else                 current = nullptr;
            }

            // Re-link neighbours
            if (node->prev) node->prev->next = node->next;
            else            head = node->next;

            if (node->next) node->next->prev = node->prev;

            delete node;
            size--;
            return true;
        }
        node = node->next;
    }
    return false;
}

void BrowserHistory::clearHistory() {
    DLLNode* node = head;
    while (node != nullptr) {
        DLLNode* next = node->next;
        delete node;
        node = next;
    }
    head    = nullptr;
    current = nullptr;
    size    = 0;
}

Page* BrowserHistory::getCurrentPage() const {
    if (current == nullptr) return nullptr;
    return &(current->data);
}

bool BrowserHistory::canGoBack() const {
    return current != nullptr && current->prev != nullptr;
}

bool BrowserHistory::canGoForward() const {
    return current != nullptr && current->next != nullptr;
}

int BrowserHistory::getSize() const { return size; }

bool BrowserHistory::isEmpty() const { return head == nullptr; }

