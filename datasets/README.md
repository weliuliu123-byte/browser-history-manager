# Synthetic Workload Datasets (`datasets/`)

Versioned browsing-history text workloads generated via `generate_datasets.py` and consumed by CLI Menu Option `11` (`Load Data From File`) and the C++ dataset parity test suite.

---

## Dataset Schema

Each line stores one visited page record formatted as comma-separated `url,title`:

```text
https://www.github.com/search?q=tu+khoa+3,GitHub - Luu tru ma nguon (Tim kiem)
https://www.stackoverflow.com/user/profile_5,Stack Overflow - Hoi dap code - Ho so
```

---

## Tracked Datasets (`generate_datasets.py` Output)

| File | Rows (`N`) | File Size (bytes) | CLI Option | Verification Status |
| :--- | :---: | :---: | :--- | :--- |
| `data_10.txt` | `10` | `744` | Option `11 -> 1` | Verified load (`10 pages loaded`) |
| `data_100.txt` | `100` | `7,294` | Option `11 -> 2` | Verified load (`100 pages loaded`) |
| `data_1000.txt` | `1,000` | `74,401` | Option `11 -> 3` | Verified load (`1000 pages loaded`, Cache `100/100`) |
| `data_5000.txt` | `5,000` | `376,188` | Option `11 -> 4` | Verified load (`5000 pages loaded`, Cache `100/100`) |
| `data_10000.txt` | `10,000` | `753,486` | Option `11 -> 5` | Verified load (`10000 pages loaded`, Cache `100/100`) |

---

## Regeneration

To regenerate identical schema workloads at any time:

```bash
cd datasets
python generate_datasets.py
```
