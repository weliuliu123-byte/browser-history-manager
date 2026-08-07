# Captured Benchmark Results (`results/`)

Raw Windows QPC profiler output, live CLI dataset ingestion metrics, structured CSV tables, and rendered performance figures generated directly by running `python scripts/plot_benchmark.py` against the compiled C++11 binary.

---

## Tracked Artifacts

| File | Description |
| :--- | :--- |
| `benchmark_report.txt` | Complete live stdout captured from Option `10` (`N = 10..10000`, 1,000-iteration averages) |
| `benchmark_metrics.csv` | Structured CSV table extracted from `benchmark_report.txt` |
| `dataset_load_metrics.csv` | Live Option `11` file-ingestion latency and PSAPI working-set table (`datasets/data_*.txt`) |
| `benchmark_latency.png` | 2x2 log-log latency comparison (`BrowserHistory` DLL vs `TwoStackSimulator`) with N=10k speedups |
| `dll_performance.png` | 2-panel live dashboard: Option `11` file ingestion + Option `10` in-memory DLL scaling |

---

## Live QPC Benchmark Summary (`benchmark_metrics.csv`)

| `N` | DLL RAM Delta (`KB`) | TS RAM Delta (`KB`) | DLL Search (`us`) | TS Search (`us`) | DLL Delete (`us`) | TS Delete (`us`) | DLL Back (`us`) | TS Back (`us`) | DLL Forward (`us`) | TS Forward (`us`) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `10` | `16.00` | `8.00` | `0.20` | `0.61` | `0.16` | `0.49` | `6.00e-04` | `2.30e-03` | `6.00e-04` | `2.40e-03` |
| `100` | `16.00` | `8.00` | `1.95` | `5.47` | `1.54` | `5.50` | `3.40e-03` | `0.02` | `8.00e-04` | `0.01` |
| `1000` | `128.00` | `96.00` | `17.69` | `55.97` | `18.07` | `62.47` | `0.03` | `0.11` | `4.30e-03` | `0.08` |
| `5000` | `632.00` | `528.00` | `92.27` | `273.58` | `95.55` | `271.40` | `0.02` | `0.09` | `6.30e-03` | `0.10` |
| `10000` | `1040.00` | `1052.00` | `191.06` | `534.34` | `185.47` | `510.49` | `0.02` | `0.11` | `5.80e-03` | `0.09` |

## Live Dataset File Ingestion Summary (`dataset_load_metrics.csv`)

| Dataset File | Rows (`N`) | Load Elapsed Time (`us`) | Process Working Set (`KB`) |
| :--- | :---: | :---: | :---: |
| `datasets/data_10.txt` | `10` | `1000.00` | `4264` |
| `datasets/data_100.txt` | `100` | `2000.00` | `4356` |
| `datasets/data_1000.txt` | `1,000` | `14002.00` | `4632` |
| `datasets/data_5000.txt` | `5,000` | `67000.00` | `5800` |
| `datasets/data_10000.txt` | `10,000` | `127733.00` | `7112` |

---

## Reproduction

```bash
python scripts/plot_benchmark.py
```
