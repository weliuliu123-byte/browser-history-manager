#ifndef CACHESTACK_H
#define CACHESTACK_H

#include "Page.h"

class CacheStack {
private:
    struct StackNode {
        Page       data;
        StackNode* next;
        StackNode(Page p) : data(p), next(nullptr) {}
    };

    StackNode* top;
    int        size;
    int        maxSize;

    bool urlExists(std::string url) const;

public:
    CacheStack(int maxSize = 5);
    ~CacheStack();

    // Disable copy (Rule of Three)
    CacheStack(const CacheStack&) = delete;
    CacheStack& operator=(const CacheStack&) = delete;

    void  push(Page p);
    Page  pop();
    Page* peek() const;
    void  displayCache() const;
    void  clearCache();
    bool  isEmpty() const;
    int   getSize() const;
};

#endif

