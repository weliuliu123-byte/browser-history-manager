# Automation, Diagram & Visualization Scripts (`scripts/`)

Python utilities that compile/run the live C++11 binary on tracked datasets, generate deterministic engineering diagrams, and render benchmark figures directly from measured outputs.

---

## Scripts

| Script | Purpose | Default Outputs |
| :--- | :--- | :--- |
| `generate_diagrams.py` | Deterministically renders all 6 architecture, UML, and algorithm flowcharts from Python | `docs/diagrams/*.png` |
| `plot_benchmark.py` | Compiles C++ binary, executes Option `10` & Option `11`, exports CSVs/TXT, and renders charts | `results/benchmark_report.txt`, `results/benchmark_metrics.csv`, `results/dataset_load_metrics.csv`, `results/benchmark_latency.png`, `results/dll_performance.png` |
| `plot_dll_scaling.py` | Renders the 2-panel live DLL ingestion + in-memory scaling dashboard (`--run` recompiles binary first) | `results/dll_performance.png` |

---

## Usage

Requires Python 3 with `matplotlib` (and `g++` / TDM-GCC on Windows to execute live C++ compilation):

```bash
pip install matplotlib
python scripts/generate_diagrams.py
python scripts/plot_benchmark.py
```

Pass `--no-run` to `plot_benchmark.py` to re-plot from existing CSVs in `results/` without recompiling, or `--show` for interactive `matplotlib` windows.
