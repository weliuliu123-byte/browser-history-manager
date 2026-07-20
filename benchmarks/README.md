# Performance Benchmarking (`benchmarks/`)

Compares the custom **Doubly Linked List** (`BrowserHistory`) against a **Two-Stack Simulator** (`TwoStackSimulator`) across scaling dataset sizes (`N = 10, 100, 1000, 5000, 10000`).

---

## Measurement Methodology (`Benchmark.cpp`)

- **High-Resolution Timing:** Uses Windows `QueryPerformanceFrequency()` and `QueryPerformanceCounter()` inside `measureExecutionTime(iterations, func)`, averaging `1,000` executions per operation (`Search`, `Delete`, `Back`, `Forward`) to resolve sub-microsecond pointer moves.
- **Target Selection:** `Search` and `Delete` query the midpoint URL (`url_<N/2>.com`) to capture representative linear traversal cost.
- **Working-Set Delta Isolation:** Samples `getActualRAMUsageKB()` immediately before and after populating `BrowserHistory` and `TwoStackSimulator` independently to report per-structure resident memory growth (`WorkingSetSize` delta in KB).
- **Parity Fix Included:** `TwoStackSimulator::searchHistory` and `deleteByUrl` traverse both `backStack` and `forwardStack` (plus `current`) via a temporary stack so complexity comparisons match `BrowserHistory` semantics.

---

## Observed Results (`g++ -std=c++11 -lpsapi`, Windows)

| `N` | DLL Memory Delta | TS Memory Delta | DLL Search (`us`) | TS Search (`us`) | DLL Delete (`us`) | TS Delete (`us`) | DLL Back (`us`) | TS Back (`us`) | DLL Forward (`us`) | TS Forward (`us`) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `10` | `8.00 KB` | `8.00 KB` | `0.98` | `1.65` | `0.82` | `1.28` | `1.60e-03` | `4.70e-03` | `1.40e-03` | `4.30e-03` |
| `100` | `20.00 KB` | `8.00 KB` | `6.25` | `14.07` | `7.75` | `13.95` | `2.50e-03` | `0.02` | `2.20e-03` | `0.02` |
| `1000` | `120.00 KB` | `96.00 KB` | `60.25` | `136.19` | `81.40` | `145.58` | `0.03` | `0.15` | `4.30e-03` | `0.15` |
| `5000` | `612.00 KB` | `520.00 KB` | `330.31` | `701.44` | `433.57` | `739.73` | `0.03` | `0.34` | `0.05` | `0.14` |
| `10000` | `1088.00 KB` | `1008.00 KB` | `678.22` | `1427.46` | `887.67` | `1464.58` | `0.02` | `0.18` | `7.70e-03` | `0.16` |
