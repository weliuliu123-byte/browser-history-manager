# Architecture & Algorithm Diagrams (`docs/`)

Visual system modeling and step-by-step algorithm flowcharts rendered deterministically from Python via [`scripts/generate_diagrams.py`](../scripts/generate_diagrams.py) (`220 DPI` widescreen figures aligned 1:1 with the C++11 source code).

---

## Diagram Index (`docs/diagrams/`)

| Diagram | Scope & Source Grounding | File |
| :--- | :--- | :--- |
| **1. DLL Deletion Flowchart** | `BrowserHistory::deleteByUrl` (`src/BrowserHistory.cpp`) — loop guard, active `current` cursor safety, and bidirectional pointer relinking | [`1_DLL_Deletion_Algorithm.png`](diagrams/1_DLL_Deletion_Algorithm.png) |
| **2. Two-Stack Navigation** | `TwoStackSimulator` (`benchmarks/Benchmark.cpp`) — 3 `O(1)` lanes + `O(N)` temporary stack rebuild penalty for search/delete | [`2_Two-Stack_Navigation.png`](diagrams/2_Two-Stack_Navigation.png) |
| **3. Bounded Cache Eviction** | `CacheStack::push` (`src/CacheStack.cpp`) — deduplication check, `size == 1` guard, bottom-node eviction (`maxSize = 100`), LIFO top push | [`3_Cache_Limit_Algorithm.png`](diagrams/3_Cache_Limit_Algorithm.png) |
| **4. QPC Benchmark Harness** | `runPerformanceBenchmark` & `measureExecutionTime` (`benchmarks/Benchmark.cpp`) — `N = 10..10000` sweep, PSAPI memory probe, 1,000-iteration QPC loop | [`4_Benchmark_QPC_Algorithm.png`](diagrams/4_Benchmark_QPC_Algorithm.png) |
| **5. System Architecture** | 4-layer architecture across CLI options `1–11`, core engines/tests, Windows probes, and reproducible datasets/plots | [`5_System_Architecture.png`](diagrams/5_System_Architecture.png) |
| **6. C++11 UML Class Diagram** | Exact member types, deleted Rule-of-Three operators, and composition (`BrowserHistory`, `CacheStack`, `StackNode`, `DLLNode`, `Page`, `TwoStackSimulator`) | [`6_System_Design_UML.png`](diagrams/6_System_Design_UML.png) |

---

## Regeneration

```bash
python scripts/generate_diagrams.py
```
