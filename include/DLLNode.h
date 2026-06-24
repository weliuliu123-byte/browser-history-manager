#ifndef DLLNODE_H
#define DLLNODE_H

#include "Page.h"

struct DLLNode {
    Page     data;
    DLLNode* prev;
    DLLNode* next;

    DLLNode(Page p) : data(p), prev(nullptr), next(nullptr) {}
};

#endif

