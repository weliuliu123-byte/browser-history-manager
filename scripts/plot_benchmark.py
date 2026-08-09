import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
import matplotlib


MILESTONES = [10, 100, 1000, 5000, 10000]


def find_gpp() -> str:
    on_path = shutil.which("g++")
    if on_path:
        return on_path
    candidates = [
        r"C:\Program Files (x86)\Embarcadero\Dev-Cpp\TDM-GCC-64\bin\g++.exe",
        r"C:\TDM-GCC-64\bin\g++.exe",
        r"C:\msys64\mingw64\bin\g++.exe",
        r"C:\mingw64\bin\g++.exe",
    ]
    for cand in candidates:
        if os.path.exists(cand):
            return cand
    raise FileNotFoundError("Could not locate g++.exe on PATH or in standard MinGW/TDM-GCC folders.")


def ensure_datasets(repo_root: Path):
    ds_dir = repo_root / "datasets"
    missing = [n for n in MILESTONES if not (ds_dir / f"data_{n}.txt").exists()]
    if missing:
        subprocess.run([sys.executable, "generate_datasets.py"], cwd=ds_dir, check=True)


def run_live_benchmarks(repo_root: Path):
    """Compile the C++11 binary, run Option 10 (QPC) and Option 11 (Datasets), and save CSV/TXT outputs."""
    ensure_datasets(repo_root)
    gpp = find_gpp()
    exe_path = repo_root / "browser_history_bench_tmp.exe"
    results_dir = repo_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    srcs = [
        "src/main.cpp",
        "src/BrowserHistory.cpp",
        "src/CacheStack.cpp",
        "src/Utils.cpp",
        "benchmarks/Benchmark.cpp",
    ]
    compile_cmd = [gpp, "-std=c++11", "-O2", "-Iinclude", *srcs, "-lpsapi", "-o", str(exe_path)]
    subprocess.run(compile_cmd, cwd=repo_root, check=True)

    try:
        # 1. Live Run: Option 10 (QPC Benchmark)
        run10 = subprocess.run(
            [str(exe_path)],
            input="10\n0\n",
            text=True,
            capture_output=True,
            cwd=repo_root,
            check=True,
        )
        report_path = results_dir / "benchmark_report.txt"
        report_path.write_text(run10.stdout, encoding="utf-8")

        blocks = re.split(r"\[\s*N\s*=\s*(\d+)\s*\]", run10.stdout)
        qpc_rows = []
        for idx in range(1, len(blocks), 2):
            n = int(blocks[idx])
            block = blocks[idx + 1]
            m_ram = re.search(r"DLL:\s*([\d.]+)\s*KB\s*\|\s*Two-Stack:\s*([\d.]+)\s*KB", block)
            ops = {}
            for op in ("Search", "Delete", "Back", "Forward"):
                mo = re.search(
                    rf"\|\s*{op}\s*\|\s*([\deE.+-]+)\s*\|\s*([\deE.+-]+)\s*\|\s*([\deE.+-]+)\s*\|",
                    block,
                )
                ops[op] = (mo.group(1), mo.group(2))
            qpc_rows.append([
                n,
                m_ram.group(1),
                m_ram.group(2),
                ops["Search"][0],
                ops["Search"][1],
                ops["Delete"][0],
                ops["Delete"][1],
                ops["Back"][0],
                ops["Back"][1],
                ops["Forward"][0],
                ops["Forward"][1],
            ])

        qpc_csv = results_dir / "benchmark_metrics.csv"
        with qpc_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "N",
                "dll_ram_delta_kb",
                "ts_ram_delta_kb",
                "dll_search_us",
                "ts_search_us",
                "dll_delete_us",
                "ts_delete_us",
                "dll_back_us",
                "ts_back_us",
                "dll_forward_us",
                "ts_forward_us",
            ])
            writer.writerows(qpc_rows)
        print(f"Captured live QPC benchmark -> {qpc_csv} ({len(qpc_rows)} milestones)")

        # 2. Live Run: Option 11 (Real File Dataset Ingestion for N=10..10000)
        run11 = subprocess.run(
            [str(exe_path)],
            input="11\n1\n11\n2\n11\n3\n11\n4\n11\n5\n0\n",
            text=True,
            capture_output=True,
            cwd=repo_root,
            check=True,
        )
        load_matches = re.findall(
            r"\[SUCCESS\]\s+(\d+)\s+pages loaded from file!.*?"
            r"Elapsed Time\s*:\s*([\deE.+-]+)\s*us.*?"
            r"Working Set\s*:\s*([\deE.+-]+)\s*KB",
            run11.stdout,
            flags=re.DOTALL,
        )
        ds_csv = results_dir / "dataset_load_metrics.csv"
        with ds_csv.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["N", "load_time_us", "working_set_kb", "dataset_file"])
            for rows_str, time_us, ram_kb in load_matches:
                n_val = int(rows_str)
                writer.writerow([n_val, time_us, ram_kb, f"datasets/data_{n_val}.txt"])
        print(f"Captured live dataset ingestion -> {ds_csv} ({len(load_matches)} datasets)")
    finally:
        if exe_path.exists():
            exe_path.unlink()


def load_csv_rows(csv_path: Path):
    with csv_path.open("r", encoding="utf-8") as f:
        return [{k: (int(v) if k == "N" else (v if k == "dataset_file" else float(v))) for k, v in r.items()} for r in csv.DictReader(f)]


def render_comparison(qpc_rows, save_path: Path, show: bool = False):
    import matplotlib.pyplot as plt

    N = [r["N"] for r in qpc_rows]
    fig, axs = plt.subplots(2, 2, figsize=(14, 9.5), dpi=200)
    fig.patch.set_facecolor("#F8FAFC")
    fig.suptitle(
        "Live Windows QPC Benchmark: Doubly Linked List vs Two-Stack Simulator",
        fontsize=15,
        fontweight="bold",
        color="#0F172A",
    )

    dll_style = {"color": "#2563EB", "marker": "o", "linewidth": 2.3, "markersize": 6.5, "label": "DLL (BrowserHistory)"}
    ts_style = {"color": "#DC2626", "marker": "s", "linewidth": 2.3, "markersize": 6.0, "label": "Two-Stack Simulator"}

    panels = [
        (axs[0, 0], "dll_search_us", "ts_search_us", "Search (Case-Insensitive Linear Scan)"),
        (axs[0, 1], "dll_delete_us", "ts_delete_us", "Delete By URL (In-Place vs Stack Rebuild)"),
        (axs[1, 0], "dll_back_us", "ts_back_us", "Back Navigation O(1)"),
        (axs[1, 1], "dll_forward_us", "ts_forward_us", "Forward Navigation O(1)"),
    ]

    for ax, dll_key, ts_key, title in panels:
        y_dll = [r[dll_key] for r in qpc_rows]
        y_ts = [r[ts_key] for r in qpc_rows]
        ax.set_facecolor("#FFFFFF")
        ax.plot(N, y_dll, **dll_style)
        ax.plot(N, y_ts, **ts_style)
        ax.set_title(title, fontweight="bold", color="#1E293B", pad=10)
        ax.set_xlabel("Dataset size (N pages)", labelpad=8)
        ax.set_ylabel("Average latency (us)", labelpad=8)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.minorticks_off()
        ax.set_axisbelow(True)
        ax.grid(True, which="major", linestyle="-", linewidth=0.75, color="#E2E8F0", alpha=0.95)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#94A3B8")
        ax.spines["bottom"].set_color("#94A3B8")
        ax.legend(frameon=True, facecolor="#FFFFFF", edgecolor="#E2E8F0", framealpha=0.95)

        if y_dll[-1] > 0:
            speedup = y_ts[-1] / y_dll[-1]
            ax.annotate(
                f"N=10k speedup: {speedup:.2f}x",
                xy=(N[-1], y_dll[-1]),
                xytext=(0.96, 0.14),
                textcoords="axes fraction",
                ha="right",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                color="#0F172A",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#EFF6FF", edgecolor="#93C5FD"),
            )

    plt.tight_layout(pad=3.0, w_pad=3.0, h_pad=3.0, rect=[0, 0, 1, 0.94])
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=200, facecolor="#F8FAFC")
        print(f"Saved comparison chart to {save_path}")

    if show:
        plt.show()
    plt.close(fig)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Compile C++ project, run live benchmarks, and plot charts.")
    parser.add_argument("--no-run", action="store_true", help="Reuse existing CSVs in results/ without recompiling C++ binary")
    parser.add_argument("--show", action="store_true", help="Display interactive matplotlib windows")
    parser.add_argument("--sodo-dir", type=Path, default=None, help="Optional secondary folder copy (e.g. so do/)")
    args = parser.parse_args()

    if not args.show:
        matplotlib.use("Agg")

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from plot_dll_scaling import render_dll_dashboard

    if not args.no_run:
        run_live_benchmarks(repo_root)

    qpc_rows = load_csv_rows(repo_root / "results" / "benchmark_metrics.csv")
    ds_rows = load_csv_rows(repo_root / "results" / "dataset_load_metrics.csv")

    comp_path = repo_root / "results" / "benchmark_latency.png"
    dll_path = repo_root / "results" / "dll_performance.png"
    render_comparison(qpc_rows, comp_path, show=args.show)
    render_dll_dashboard(ds_rows, qpc_rows, dll_path, show=args.show)

    if args.sodo_dir is not None:
        args.sodo_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(comp_path, args.sodo_dir / "benchmark_comparison.png")
        shutil.copy2(dll_path, args.sodo_dir / "dll_performance.png")


if __name__ == "__main__":
    main()
