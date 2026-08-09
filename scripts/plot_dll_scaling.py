import argparse
import sys
from pathlib import Path
import matplotlib


def render_dll_dashboard(ds_rows, qpc_rows, save_path: Path, show: bool = False):
    import matplotlib.pyplot as plt

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(15.5, 6.6), dpi=200)
    fig.patch.set_facecolor("#F8FAFC")
    fig.suptitle(
        "Live DLL Performance Dashboard: Real Dataset Ingestion & In-Memory QPC Scaling",
        fontsize=14.5,
        fontweight="bold",
        color="#0F172A",
    )

    # Panel A: Option 11 Real Dataset File Ingestion (Working Set KB vs Load Time us)
    labels_ds = [f"N={r['N']:,}" for r in ds_rows]
    x_ds = list(range(len(ds_rows)))
    ram_ws = [r["working_set_kb"] for r in ds_rows]
    load_us = [r["load_time_us"] for r in ds_rows]

    ax_left.set_facecolor("#FFFFFF")
    bars_l = ax_left.bar(x_ds, ram_ws, width=0.48, color="#3B82F6", alpha=0.72, label="Working Set RAM (KB)")
    ax_left.set_title("CLI Option 11: Real Dataset File Ingestion (datasets/data_*.txt)", fontweight="bold", color="#1E293B", pad=10)
    ax_left.set_xlabel("Loaded Dataset Size (N Rows)", fontweight="bold", labelpad=8)
    ax_left.set_ylabel("Process Working Set (KB)", color="#1D4ED8", fontweight="bold")
    ax_left.tick_params(axis="y", labelcolor="#1D4ED8")
    ax_left.set_xticks(x_ds)
    ax_left.set_xticklabels(labels_ds, fontweight="bold")
    ax_left.set_ylim(0, max(ram_ws) * 1.28)
    ax_left.set_axisbelow(True)
    ax_left.grid(axis="y", linestyle="-", linewidth=0.75, color="#E2E8F0", alpha=0.95)
    ax_left.spines["top"].set_visible(False)

    for b in bars_l:
        val = b.get_height()
        ax_left.text(b.get_x() + b.get_width() / 2, val + max(ram_ws) * 0.02, f"{val:.0f} KB",
                     ha="center", va="bottom", color="#1E40AF", fontsize=8.5, fontweight="bold")

    ax_l2 = ax_left.twinx()
    ax_l2.spines["top"].set_visible(False)
    ax_l2.plot(x_ds, load_us, color="#DC2626", linewidth=2.5, marker="o", markersize=6.5, label="File Load Time (us)")
    ax_l2.set_ylabel("File Load Elapsed Time (us)", color="#B91C1C", fontweight="bold")
    ax_l2.tick_params(axis="y", labelcolor="#B91C1C")
    ax_l2.set_ylim(0, max(load_us) * 1.30 if max(load_us) > 0 else 100)

    for i, val in enumerate(load_us):
        ax_l2.text(x_ds[i], val + max(load_us) * 0.045, f"{val:,.0f} us",
                   color="#B91C1C", fontsize=8.3, fontweight="bold", ha="center",
                   bbox=dict(boxstyle="round,pad=0.14", facecolor="#FFFFFF", edgecolor="none", alpha=0.85))

    l1, lb1 = ax_left.get_legend_handles_labels()
    l2, lb2 = ax_l2.get_legend_handles_labels()
    ax_left.legend(l1 + l2, lb1 + lb2, loc="upper left", frameon=True, facecolor="#FFFFFF")

    # Panel B: Option 10 In-Memory Heap Delta vs Search/Delete O(N) Latency
    labels_qpc = [f"N={r['N']:,}" for r in qpc_rows]
    x_qpc = list(range(len(qpc_rows)))
    ram_delta = [r["dll_ram_delta_kb"] for r in qpc_rows]
    search_us = [r["dll_search_us"] for r in qpc_rows]
    delete_us = [r["dll_delete_us"] for r in qpc_rows]

    ax_right.set_facecolor("#FFFFFF")
    bars_r = ax_right.bar(x_qpc, ram_delta, width=0.48, color="#0EA5E9", alpha=0.72, label="DLL Heap Delta (KB)")
    ax_right.set_title("CLI Option 10: In-Memory DLL Heap Delta vs O(N) Operations", fontweight="bold", color="#1E293B", pad=10)
    ax_right.set_xlabel("Benchmark Scale (N Nodes)", fontweight="bold", labelpad=8)
    ax_right.set_ylabel("DLL Memory Delta (KB)", color="#0369A1", fontweight="bold")
    ax_right.tick_params(axis="y", labelcolor="#0369A1")
    ax_right.set_xticks(x_qpc)
    ax_right.set_xticklabels(labels_qpc, fontweight="bold")
    ax_right.set_ylim(0, max(ram_delta) * 1.25)
    ax_right.set_axisbelow(True)
    ax_right.grid(axis="y", linestyle="-", linewidth=0.75, color="#E2E8F0", alpha=0.95)
    ax_right.spines["top"].set_visible(False)

    for b in bars_r:
        val = b.get_height()
        ax_right.text(b.get_x() + b.get_width() / 2, val + max(ram_delta) * 0.02, f"{val:.0f} KB",
                      ha="center", va="bottom", color="#075985", fontsize=8.5, fontweight="bold")

    ax_r2 = ax_right.twinx()
    ax_r2.spines["top"].set_visible(False)
    ax_r2.plot(x_qpc, search_us, color="#DC2626", linewidth=2.5, marker="o", markersize=6.5, label="Search Latency (us)")
    ax_r2.plot(x_qpc, delete_us, color="#D97706", linewidth=2.2, linestyle="--", marker="s", markersize=5.8, label="Delete Latency (us)")
    ax_r2.set_ylabel("QPC 1,000-Iter Avg Latency (us)", color="#B91C1C", fontweight="bold")
    ax_r2.tick_params(axis="y", labelcolor="#B91C1C")
    ax_r2.set_ylim(0, max(max(search_us), max(delete_us)) * 1.30)

    for i, val in enumerate(search_us):
        offset_x = -0.28 if i == 2 else (-0.18 if i >= 3 else -0.14)
        offset_y = max(search_us) * (0.095 if i == 2 else (0.075 if i < 3 else 0.04))
        ax_r2.text(x_qpc[i] + offset_x, val + offset_y, f"{val:.2f} us",
                   color="#B91C1C", fontsize=8.3, fontweight="bold", ha="right")

    r1, rb1 = ax_right.get_legend_handles_labels()
    r2, rb2 = ax_r2.get_legend_handles_labels()
    ax_right.legend(r1 + r2, rb1 + rb2, loc="upper left", frameon=True, facecolor="#FFFFFF")

    plt.tight_layout(pad=2.8, rect=[0, 0, 1, 0.93])
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=200, facecolor="#F8FAFC")
        print(f"Saved DLL scaling chart to {save_path}")

    if show:
        plt.show()
    plt.close(fig)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Render DLL scaling dashboard from live benchmark CSVs.")
    parser.add_argument("--run", action="store_true", help="Recompile and run C++ binary before plotting")
    parser.add_argument("--save", type=Path, default=repo_root / "results" / "dll_performance.png")
    parser.add_argument("--show", action="store_true", help="Display interactive matplotlib window")
    args = parser.parse_args()

    if not args.show:
        matplotlib.use("Agg")

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from plot_benchmark import load_csv_rows, run_live_benchmarks

    qpc_csv = repo_root / "results" / "benchmark_metrics.csv"
    ds_csv = repo_root / "results" / "dataset_load_metrics.csv"
    if args.run or not qpc_csv.exists() or not ds_csv.exists():
        run_live_benchmarks(repo_root)

    ds_rows = load_csv_rows(ds_csv)
    qpc_rows = load_csv_rows(qpc_csv)
    render_dll_dashboard(ds_rows, qpc_rows, args.save, show=args.show)


if __name__ == "__main__":
    main()
