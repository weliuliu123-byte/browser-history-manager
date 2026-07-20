# Synthetic Workload Datasets (`datasets/`)

Generates reproducible browsing-history text datasets consumed by CLI Menu Option `11` (`Load Data From File`). Generated `.txt` files are excluded via `.gitignore` and recreated locally on demand.

---

## Dataset Schema

Each line stores one visited page record formatted as comma-separated `url,title`:

```text
https://www.github.com/search?q=tu+khoa+3,GitHub - Luu tru ma nguon (Tim kiem)
https://www.stackoverflow.com/user/profile_5,Stack Overflow - Hoi dap code - Ho so
```

---

## Generated Presets

Running `generate_datasets.py` emits five scaling datasets:

| File | Line Count (`N`) | Used By |
| :--- | :---: | :--- |
| `data_10.txt` | `10` | Option `11 -> 1` |
| `data_100.txt` | `100` | Option `11 -> 2` |
| `data_1000.txt` | `1,000` | Option `11 -> 3` |
| `data_5000.txt` | `5,000` | Option `11 -> 4` |
| `data_10000.txt` | `10,000` | Option `11 -> 5` |

---

## Usage

```bash
cd datasets
python generate_datasets.py
```
