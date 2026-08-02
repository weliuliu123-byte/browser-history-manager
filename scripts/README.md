# Visualization Scripts (`scripts/`)

Python plotting utilities driven directly by captured QPC benchmark measurements in [`results/benchmark_metrics.csv`](../results/benchmark_metrics.csv).

---

## Scripts

| Script | Purpose | Default Output |
| :--- | :--- | :--- |
| `plot_benchmark.py` | Renders a 2x2 log-log latency comparison (`DLL` vs `TwoStackSimulator`) for Search, Delete, Back, and Forward | `results/benchmark_latency.png` |
| `plot_dll_scaling.py` | Renders a dual-axis chart comparing DLL heap RAM delta (`KB`) against `O(N)` Search & Delete latency (`us`) | `results/dll_performance.png` |

---

## Usage

Requires Python 3 with `matplotlib`:

```bash
pip install matplotlib
python scripts/plot_benchmark.py --save results/benchmark_latency.png
python scripts/plot_dll_scaling.py --save results/dll_performance.png
```

Pass `--show` to open an interactive `matplotlib` window instead of headless `Agg` export.
