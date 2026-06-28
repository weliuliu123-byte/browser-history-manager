#include "CacheStack.h"
#include <iostream>
#include <iomanip>
using namespace std;

CacheStack::CacheStack(int maxSize) : top(nullptr), size(0), maxSize(maxSize) {}

CacheStack::~CacheStack() {
    clearCache();
}

bool CacheStack::urlExists(string url) const {
    StackNode* node = top;
    while (node != nullptr) {
        if (node->data.url == url) return true;
        node = node->next;
    }
    return false;
}

void CacheStack::push(Page p) {
    // Skip if URL already cached (no duplicates)
    if (urlExists(p.url)) return;

    // If cache full, remove the oldest entry (bottom of stack)
    if (size >= maxSize) {
        if (size == 1) {
            delete top;
            top  = nullptr;
            size = 0;
        } else {
            StackNode* node = top;
            while (node->next->next != nullptr)
                node = node->next;
            delete node->next;
            node->next = nullptr;
            size--;
        }
    }

    StackNode* newNode = new StackNode(p);
    newNode->next = top;
    top  = newNode;
    size++;
}

Page CacheStack::pop() {
    if (isEmpty()) return Page();
    StackNode* temp = top;
    Page       data = temp->data;
    top  = top->next;
    delete temp;
    size--;
    return data;
}

Page* CacheStack::peek() const {
    if (isEmpty()) return nullptr;
    return &(top->data);
}

void CacheStack::displayCache() const {
    if (isEmpty()) {
        cout << "\n  [Cache is empty]\n";
        return;
    }

    cout << "\n=== BROWSER CACHE (Most Recent First | Max: " << maxSize << ") ===\n";
    cout << left
         << setw(5)  << "#"
         << setw(32) << "URL"
         << setw(25) << "Title"
         << setw(10) << "Time"
         << "\n";
    cout << string(72, '-') << "\n";

    StackNode* node  = top;
    int        index = 1;
    while (node != nullptr) {
        cout << left
             << setw(5)  << index
             << setw(32) << node->data.url
             << setw(25) << node->data.title
             << setw(10) << node->data.visitTime
             << "\n";
        node = node->next;
        index++;
    }
    cout << string(72, '-') << "\n";
    cout << "  Cached: " << size << "/" << maxSize << "\n";
}

void CacheStack::clearCache() {
    while (top != nullptr) {
        StackNode* temp = top;
        top  = top->next;
        delete temp;
    }
    size = 0;
}

bool CacheStack::isEmpty() const { return top == nullptr; }

int  CacheStack::getSize() const { return size; }

