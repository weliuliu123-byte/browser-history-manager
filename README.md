# Browser History & Cache Navigation System

A modular C++11 console application and benchmarking suite comparing a custom **Doubly Linked List** history manager and bounded **Stack Cache** against a **Two-Stack** navigation simulator (`std::stack`).

**Author:** Ha Gia Bao  
**Contact:** `weliuliu123@gmail.com`  
**Toolchain:** C++11 (`g++` / TDM-GCC-64), Windows PSAPI (`-lpsapi`), Python 3 (`matplotlib`)

---

## System Architecture

- **History Engine (`BrowserHistory`):** Custom Doubly Linked List supporting `O(1)` forward/back pointer traversal, mid-history branch truncation on new visits, case-insensitive keyword search, and safe node relinking on deletion.
- **Bounded Cache (`CacheStack`):** Singly-linked LIFO stack capped at `100` unique URLs, suppressing duplicates and evicting the oldest bottom node upon overflow.
- **Benchmark Harness (`TwoStackSimulator` + QPC):** Measures 1,000-iteration average latency via Windows `QueryPerformanceCounter` and resident memory delta via `GetProcessMemoryInfo` (`psapi.dll`) across `N = 10` to `10,000`.
- **Architecture & Algorithm Diagrams:** UML class design and orthogonal algorithm flowcharts stored under [`docs/diagrams/`](docs/diagrams/).

---

## Subsystem & Verification Summary

| Component | Purpose | Verification Status | Module Documentation |
| :--- | :--- | :--- | :--- |
| **Governance** | Branching model, commit rules, 1-to-1 scope table | Complete | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| **Public Headers** | `Page`, `DLLNode`, `BrowserHistory`, `CacheStack`, `Utils`, `Benchmark` | Compiles clean (`-Wall`) | [`include/README.md`](include/README.md) |
| **Core Engine** | DLL history navigation, bounded LIFO cache, CLI menu controller | CLI & UT verified | [`src/README.md`](src/README.md) |
| **Benchmark Harness** | `TwoStackSimulator` vs DLL latency & PSAPI RAM delta profiler | Captured (`N = 10..10000`) | [`benchmarks/README.md`](benchmarks/README.md) |
| **Unit & Parity Tests** | 5 C++ assertion suites (`UT-01..UT-05`) covering core & CSV ingestion | `5/5` Passed (exit `0`) | [`tests/README.md`](tests/README.md) |
| **Tracked Workloads** | Synthetic `url,title` text datasets (`10` to `10,000` rows) | Verified CLI Option `11` | [`datasets/README.md`](datasets/README.md) |
| **Plotting Scripts** | Log-log latency & dual-axis RAM/latency PNG chart generators | Rendered headlessly | [`scripts/README.md`](scripts/README.md) |
| **Captured Results** | Raw QPC stdout report, metrics CSV, and rendered charts | Verified on Windows QPC | [`results/README.md`](results/README.md) |
| **Architecture Docs** | System architecture, UML class diagram, 4 algorithm flowcharts | Complete | [`docs/README.md`](docs/README.md) |

---

## Repository Structure

| Path | Description |
| :--- | :--- |
| `README.md` | Root architecture overview, build/test steps, and measured results |
| `CONTRIBUTING.md` | Development order, branching rules, Conventional Commits, and scope mapping |
| `Makefile` | CLI build and automated test targets (`all`, `test`, `clean`) |
| `Project_topic_9.dev` | Dev-C++ IDE project configuration |
| `.gitignore` | Excludes compiled binaries (`*.exe`, `*.o`), Python caches, and IDE clutter |
| `include/` | Clean header contracts (`Page.h`, `DLLNode.h`, `BrowserHistory.h`, `CacheStack.h`, `Benchmark.h`, `Utils.h`) |
| `src/` | Core C++ source files (`main.cpp`, `BrowserHistory.cpp`, `CacheStack.cpp`, `Utils.cpp`) |
| `benchmarks/` | `TwoStackSimulator` implementation and multi-scale QPC profiler (`Benchmark.cpp`) |
| `tests/` | Automated C++ unit and dataset parity suite (`test_history_and_cache.cpp`) |
| `datasets/` | Python workload generator (`generate_datasets.py`) and generated `data_*.txt` workloads |
| `scripts/` | Matplotlib visualization scripts (`plot_benchmark.py`, `plot_dll_scaling.py`) |
| `results/` | Captured benchmark output (`benchmark_report.txt`, `benchmark_metrics.csv`, PNG charts) |
| `docs/` | System design UML, architecture overview, and algorithm flowcharts (`docs/diagrams/`) |

---

## Build, Test & Plot

### 1. Build & Run Interactive CLI
```bash
g++ -std=c++11 -O2 -Wall -Wextra -Iinclude src/main.cpp src/BrowserHistory.cpp src/CacheStack.cpp src/Utils.cpp benchmarks/Benchmark.cpp -lpsapi -o browser_history.exe
./browser_history.exe
```

### 2. Run Automated Unit & Dataset Parity Tests (`UT-01..UT-05`)
```bash
g++ -std=c++11 -O2 -Wall -Wextra -Iinclude tests/test_history_and_cache.cpp src/BrowserHistory.cpp src/CacheStack.cpp src/Utils.cpp benchmarks/Benchmark.cpp -lpsapi -o test_suite.exe
./test_suite.exe
```

### 3. Regenerate Datasets & Charts
```bash
cd datasets && python generate_datasets.py && cd ..
python scripts/plot_benchmark.py --save results/benchmark_latency.png
python scripts/plot_dll_scaling.py --save results/dll_performance.png
```

---

## Measured Benchmark Results (Windows QPC, 1,000 Iterations)

Captured verbatim in [`results/benchmark_report.txt`](results/benchmark_report.txt) and [`results/benchmark_metrics.csv`](results/benchmark_metrics.csv):

| `N` | DLL Memory Delta | TS Memory Delta | DLL Search (`us`) | TS Search (`us`) | DLL Delete (`us`) | TS Delete (`us`) | DLL Back (`us`) | TS Back (`us`) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `10` | `16.00 KB` | `4.00 KB` | `0.20` | `0.61` | `0.19` | `0.48` | `6.00e-04` | `2.70e-03` |
| `100` | `24.00 KB` | `12.00 KB` | `1.80` | `5.22` | `1.55` | `5.33` | `1.40e-03` | `0.01` |
| `1000` | `120.00 KB` | `100.00 KB` | `17.46` | `50.70` | `16.94` | `50.63` | `0.02` | `0.12` |
| `5000` | `628.00 KB` | `528.00 KB` | `86.54` | `265.07` | `88.87` | `259.69` | `0.03` | `0.10` |
| `10000` | `1052.00 KB` | `1024.00 KB` | `192.30` | `551.27` | `179.18` | `531.42` | `0.02` | `0.11` |

Visualizations:
- Comparative 2x2 Latency Curve: [`results/benchmark_latency.png`](results/benchmark_latency.png)
- DLL Memory vs `O(N)` Latency Scaling: [`results/dll_performance.png`](results/dll_performance.png)
- System UML & Algorithm Diagrams: [`docs/README.md`](docs/README.md)
