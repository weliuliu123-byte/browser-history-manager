#ifndef PAGE_H
#define PAGE_H

#include <string>
using namespace std;

struct Page {
    string url;
    string title;
    string visitTime;

    Page() : url(""), title(""), visitTime("") {}
    Page(string url, string title, string visitTime)
        : url(url), title(title), visitTime(visitTime) {}
};

#endif

