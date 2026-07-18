# Public Header Interfaces (`include/`)

C++11 header specifications defining data models, pointer-based container boundaries, ownership constraints, and platform helper APIs.

---

## Header Inventory

| Header | Core Types / Functions | Ownership & Safety Notes |
| :--- | :--- | :--- |
| `Page.h` | `struct Page` (`url`, `title`, `visitTime`) | Plain value record with default and parameterized constructors; explicit `std::string` qualification (no `using namespace std;` in headers). |
| `DLLNode.h` | `struct DLLNode` (`data`, `prev`, `next`) | Heap-allocated doubly-linked node taking `const Page&` to avoid redundant record copies. |
| `BrowserHistory.h` | `class BrowserHistory` | Owns linked list nodes from `head` and tracks `current` + `size`; deletes copy constructor and copy assignment (`= delete`) to prevent double-free bugs. |
| `CacheStack.h` | `class CacheStack`, `struct StackNode` | Owns singly-linked LIFO stack capped at `maxSize` (default `100`); deletes copy constructor and copy assignment (`= delete`). |
| `Benchmark.h` | `class TwoStackSimulator`, `runPerformanceBenchmark()` | Uses two `std::stack<Page>` containers (`backStack`, `forwardStack`) plus `Page* current` for baseline comparison against `BrowserHistory`. |
| `Utils.h` | `getIntInput`, `getStringInput`, `getCurrentTime`, `getActualRAMUsageKB` | Console input validation helpers, timestamp formatting, and Windows PSAPI memory lookup. |

---

## Design Rules Applied

- **Namespace Isolation:** Every header avoids `using namespace std;` to keep translation-unit symbol resolution clean.
- **Explicit Copy Prevention:** Pointer-owning classes (`BrowserHistory`, `CacheStack`) enforce non-copyable semantics (`= delete`) so raw node pointers are freed exactly once in their destructors.
