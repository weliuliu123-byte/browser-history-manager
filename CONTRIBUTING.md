# Contributing Guidelines

This repository follows a layered C++11 module architecture, isolated feature-branch development, and strict 1-to-1 Conventional Commit scoping.

---

## Development Order

Changes should progress along dependency order so every layer compiles and passes verification before downstream integration:

1. **Public Interfaces (`include/`)** — `Page`, `DLLNode`, `BrowserHistory`, `CacheStack`, `Utils`, `Benchmark`.
2. **Core Containers (`src/`)** — `BrowserHistory`, `CacheStack`, `Utils`, and CLI `main.cpp`.
3. **Synthetic Workloads (`datasets/`)** — Generator script and versioned `data_*.txt` browsing snapshots.
4. **Benchmarking & Unit Tests (`benchmarks/`, `tests/`)** — `TwoStackSimulator`, QPC harness, and automated `UT-01..UT-05` assertions.
5. **Visualization & Results (`scripts/`, `results/`)** — CSV export, PNG chart rendering, and captured reports.
6. **Architecture Docs (`docs/`, root `README.md`)** — UML/system flowcharts and root documentation sync.

---

## Branching Rules

- **`main`**: Clean integration branch. Always compiles with `g++ -std=c++11 -O2` and passes `tests/test_history_and_cache.cpp`.
- **Feature / Task Branches**: Create one branch per functional scope before modifying code or data:
  - `feat/<short-description>` (new capabilities or visualization pipelines)
  - `data/<short-description>` (generated datasets or captured benchmark artifacts)
  - `test/<short-description>` (unit and dataset parity suites)
  - `docs/<short-description>` (architecture diagrams, READMEs, governance)
  - `fix/<short-description>` (bug fixes, relinking guards, spec alignment)
- Verify compilation and tests on the branch before merging into `main`. Never force-push rewritten orphan histories to `main`.

---

## Conventional Commits & 1-to-1 Scope Mapping

Format: `<type>(<scope>): <imperative summary <= 72 chars>`

**Allowed Types:** `feat`, `fix`, `docs`, `test`, `perf`, `refactor`, `build`, `ci`, `chore`, `data`, `sync`

| Scope | Target Directory / Files | Example Commit |
| :--- | :--- | :--- |
| `repo` | `.gitignore`, `Makefile`, `Project_topic_9.dev`, `CONTRIBUTING.md` | `build(repo): add test target to Makefile` |
| `readme` | Root `README.md` | `docs(readme): sync root README with test and chart outputs` |
| `include` | `include/*.h` | `feat(include): define Page, DLLNode, and core container interfaces` |
| `src` / `history` / `cache` / `utils` / `cli` | `src/*.cpp` | `feat(cache): implement bounded LIFO cache stack with bottom eviction` |
| `benchmarks` / `benchmark` | `benchmarks/` | `feat(benchmark): implement TwoStackSimulator and QPC profiler` |
| `tests` | `tests/` | `test(tests): add unit and dataset parity suite for core containers` |
| `datasets` | `datasets/` | `data(datasets): add generated 5k and 10k scaling workloads` |
| `scripts` | `scripts/` | `feat(scripts): add CSV parsing and headless chart export scripts` |
| `results` | `results/` | `feat(results): render QPC comparison and DLL scaling charts` |
| `docs` | `docs/` | `docs(docs): add system architecture and UML class diagrams` |

---

## Pre-Merge Verification Checklist

- [ ] `git status` is clean; `.gitignore` blocks compiled binaries (`*.exe`, `*.o`), `__pycache__/`, and editor folders.
- [ ] Core binary builds cleanly (`g++ -std=c++11 -O2 -Wall -Wextra -Iinclude src/*.cpp benchmarks/Benchmark.cpp -lpsapi -o browser_history.exe`).
- [ ] All 5 unit and dataset parity suites (`UT-01..UT-05`) pass with exit code `0`.
- [ ] Every directory listed in root `README.md` exists and contains an accurate, up-to-date `README.md`.
