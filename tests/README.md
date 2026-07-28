# Unit & Dataset Parity Tests (`tests/`)

Automated assertion suite verifying `BrowserHistory`, `CacheStack`, `TwoStackSimulator`, and live ingestion of versioned files under `datasets/`.

**Status:** Verified passing (`5/5` suites passed, exit code `0` under TDM-GCC C++11).

---

## Test Matrix (`test_history_and_cache.cpp`)

| ID | Suite Scope | Verified Invariants | Status |
| :---: | :--- | :--- | :---: |
| `UT-01` | `BrowserHistory` Navigation | `visit`, `back`, `forward`, mid-history forward-branch deletion | PASS |
| `UT-02` | `BrowserHistory` Search & Delete | Case-insensitive keyword search, head/middle/tail node relinking, `clearHistory` | PASS |
| `UT-03` | `CacheStack` Bounded LIFO | Duplicate URL suppression, bottom-node eviction on overflow (`maxSize = 3`), LIFO `peek`/`pop` | PASS |
| `UT-04` | `TwoStackSimulator` Parity | Navigation (`back`/`forward`), full stack search, `deleteByUrl` parity | PASS |
| `UT-05` | Dataset File Ingestion | Parses `datasets/data_100.txt` (`100` rows) & `datasets/data_1000.txt` (`1,000` rows), cache cap `100` | PASS |

---

## Build & Run

```bash
make test
```

Or directly with `g++`:

```bash
g++ -std=c++11 -O2 -Wall -Wextra -Iinclude tests/test_history_and_cache.cpp src/BrowserHistory.cpp src/CacheStack.cpp src/Utils.cpp benchmarks/Benchmark.cpp -lpsapi -o test_suite.exe
./test_suite.exe
```

## Observed Output

```text
[PASS] UT-01: BrowserHistory navigation and mid-history truncation
[PASS] UT-02: BrowserHistory search, relink deletion, and clear
[PASS] UT-03: CacheStack deduplication and bottom eviction
[PASS] UT-04: TwoStackSimulator navigation, search, and delete parity
[PASS] UT-05: Tracked dataset ingestion (100 and 1,000 rows, cache capped at 100)
ALL 5 UNIT & DATASET TEST SUITES PASSED.
```
