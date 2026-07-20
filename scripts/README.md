# Visualization Scripts (`scripts/`)

Helper scripts for plotting comparative latency curves from benchmark runs.

---

## `plot_benchmark.py`

Renders a `2x2` `matplotlib` figure comparing **Doubly Linked List (`BrowserHistory`)** against **Two-Stack Simulator** across `N = 10, 100, 1000, 5000, 10000` on log-scaled axes (`USE_LOG_SCALE = True`):

- **Search Latency (`us`):** Highlights `O(N)` linear scan scaling vs stack pop/push overhead.
- **Delete Latency (`us`):** Compares in-place DLL node unlinking against full two-stack rebuilds.
- **Back & Forward Latency (`us`):** Verifies near-constant `O(1)` navigation across all dataset sizes.

---

## Usage

Requires Python 3 with `matplotlib`:

```bash
pip install matplotlib
python scripts/plot_benchmark.py
```
