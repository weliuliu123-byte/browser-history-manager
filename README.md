# Browser History & Cache Navigation System

A modular C++11 console application and benchmarking suite comparing a custom **Doubly Linked List** history manager and bounded **Stack Cache** against a **Two-Stack** navigation simulator (`std::stack`).

**Author:** Ha Gia Bao  
**Contact:** `weliuliu123@gmail.com`  
**Toolchain:** C++11 (`g++` / TDM-GCC), Windows PSAPI (`-lpsapi`), Python 3 (`matplotlib`)

---

## Engineering Overview

The project implements stateful browser session navigation alongside quantitative latency and working-set profiling:

- **History Engine (`BrowserHistory`):** Custom Doubly Linked List supporting `O(1)` forward/back pointer traversal, mid-history branch truncation on new visits, case-insensitive keyword search, and safe node relinking on deletion.
- **Bounded Cache (`CacheStack`):** Singly-linked LIFO stack capped at `100` unique URLs, suppressing duplicates and evicting the oldest bottom node upon overflow.
- **Benchmark Harness (`TwoStackSimulator` + QPC):** Measures 1,000-iteration average latency via Windows `QueryPerformanceCounter` and resident memory delta via `GetProcessMemoryInfo` (`psapi.dll`) from `N = 10` to `10,000`.

---

## Complexity & Subsystem Summary

| Component | Operations | Time Complexity | Module Documentation |
| :--- | :--- | :---: | :--- |
| **Public Interfaces** | `Page`, `DLLNode`, `BrowserHistory`, `CacheStack`, `Utils` | — | [`include/README.md`](include/README.md) |
| **Core Implementations** | `visit`, `back`, `forward` (`O(1)`); `search`, `delete`, bounded `push` (`O(N)`) | `O(1)` / `O(N)` | [`src/README.md`](src/README.md) |
| **Benchmark Suite** | `TwoStackSimulator` parity & Windows QPC profiler (`N = 10..10000`) | `O(1)` / `O(N)` | [`benchmarks/README.md`](benchmarks/README.md) |
| **Synthetic Workloads** | Reproducible `url,title` dataset generator (`10` to `10,000` rows) | — | [`datasets/README.md`](datasets/README.md) |
| **Visualization** | 2x2 log-scale latency comparison charts (`matplotlib`) | — | [`scripts/README.md`](scripts/README.md) |

---

## Repository Structure

| Path | Description |
| :--- | :--- |
| `README.md` | Root architecture overview, build instructions, and benchmark summary |
| `Makefile` | CLI build configuration (`g++ -std=c++11 -O2 -Iinclude ... -lpsapi`) |
| `Project_topic_9.dev` | Dev-C++ IDE project configuration |
| `.gitignore` | Excludes compiled binaries (`*.exe`, `*.o`), generated `.txt` datasets, and caches |
| `include/` | Clean header interfaces (`Page.h`, `DLLNode.h`, `BrowserHistory.h`, `CacheStack.h`, `Benchmark.h`, `Utils.h`) |
| `src/` | Core C++ source files (`main.cpp`, `BrowserHistory.cpp`, `CacheStack.cpp`, `Utils.cpp`) |
| `benchmarks/` | `TwoStackSimulator` implementation and multi-scale QPC profiler (`Benchmark.cpp`) |
| `datasets/` | Python workload generator (`generate_datasets.py`) |
| `scripts/` | Latency visualization script (`plot_benchmark.py`) |

---

## Build & Run

### 1. Generate Synthetic Datasets (for Menu Option `11`)
```bash
cd datasets
python generate_datasets.py
cd ..
```

### 2. Compile & Execute
Using `g++` (TDM-GCC / MinGW-w64) or `make`:

```bash
g++ -std=c++11 -O2 -Iinclude src/main.cpp src/BrowserHistory.cpp src/CacheStack.cpp src/Utils.cpp benchmarks/Benchmark.cpp -lpsapi -o browser_history.exe
./browser_history.exe
```

---

## Measured Benchmark Snapshot (Windows QPC, 1,000 Iterations)

Observed via CLI Option `10` (`Run Performance Benchmark`):

| `N` | DLL Memory Delta | TS Memory Delta | DLL Search (`us`) | TS Search (`us`) | DLL Delete (`us`) | TS Delete (`us`) | DLL Back (`us`) | TS Back (`us`) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `10` | `8.00 KB` | `8.00 KB` | `0.98` | `1.65` | `0.82` | `1.28` | `1.60e-03` | `4.70e-03` |
| `100` | `20.00 KB` | `8.00 KB` | `6.25` | `14.07` | `7.75` | `13.95` | `2.50e-03` | `0.02` |
| `1000` | `120.00 KB` | `96.00 KB` | `60.25` | `136.19` | `81.40` | `145.58` | `0.03` | `0.15` |
| `5000` | `612.00 KB` | `520.00 KB` | `330.31` | `701.44` | `433.57` | `739.73` | `0.03` | `0.34` |
| `10000` | `1088.00 KB` | `1008.00 KB` | `678.22` | `1427.46` | `887.67` | `1464.58` | `0.02` | `0.18` |

Key takeaways:
- Both structures achieve sub-microsecond `O(1)` `Back`/`Forward` navigation across all tested sizes.
- Direct Doubly Linked List traversal reduces `Search` and `Delete` latency by roughly 2x compared to copying elements through a temporary stack in `TwoStackSimulator`.
