# Core Implementation (`src/`)

Implements the interactive CLI controller, Doubly Linked List history engine, bounded stack cache, and OS/console utilities.

---

## Module Breakdown

| File | Primary Responsibilities | Key Algorithmic Details |
| :--- | :--- | :--- |
| `BrowserHistory.cpp` | `visit`, `back`, `forward`, `searchHistory`, `searchHistorySilent`, `deleteByUrl`, `clearHistory` | Trims stale forward nodes when visiting from mid-history; performs case-insensitive substring matching (`toLower`); handles head, tail, middle, and `current` pointer relinking during deletion. |
| `CacheStack.cpp` | `push`, `pop`, `peek`, `urlExists`, `displayCache`, `clearCache` | Skips duplicate URLs before insertion; when `size >= maxSize`, traverses to the bottom of the singly-linked stack to free the oldest entry before pushing the newest page to `top`. |
| `Utils.cpp` | `getIntInput`, `getStringInput`, `getCurrentTime`, `getActualRAMUsageKB` | Clears invalid `std::cin` flags on malformed numeric input; formats local timestamps (`YYYY-MM-DD HH:MM:SS`); caches `LoadLibraryA("psapi.dll")` via `static HMODULE` to read `PROCESS_MEMORY_COUNTERS::WorkingSetSize` in KiB. |
| `main.cpp` | CLI menu loop (Options `0`–`11`), `printMiniReport`, `loadDataFromFile` | Measures single-operation wall time via `std::chrono::high_resolution_clock` and clears prior history/cache before loading CSV-style dataset files (`datasets/data_*.txt`). |

---

## Pointer & Memory Behavior

- **`BrowserHistory::visit(Page)`:** When `current->next != nullptr`, all nodes after `current` are deleted before linking the new node, matching real browser forward-branch truncation.
- **`BrowserHistory::deleteByUrl(string)`:** Updates `current` to `node->prev` (or `node->next`, or `nullptr` if last node) whenever the active page is deleted, then splices surrounding `prev`/`next` links and calls `delete node`.
- **`CacheStack::push(Page)`:** Prioritizes strict capacity bounding (`maxSize = 100`) and duplicate suppression without allocating auxiliary hash structures.
