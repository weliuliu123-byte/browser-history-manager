import argparse
import csv
from pathlib import Path
import matplotlib


def load_metrics(csv_path: Path):
    rows = []
    with csv_path.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({k: float(v) if k != "N" else int(v) for k, v in r.items()})
    return rows


def render_dll_scaling(rows, save_path: Path, show: bool = False):
    import matplotlib.pyplot as plt

    labels = [f"N={r['N']:,}" for r in rows]
    x_pos = list(range(len(rows)))
    ram_kb = [r["dll_ram_delta_kb"] for r in rows]
    search_us = [r["dll_search_us"] for r in rows]
    delete_us = [r["dll_delete_us"] for r in rows]

    fig, ax1 = plt.subplots(figsize=(10.5, 6))

    bar_color = "#3498db"
    bars = ax1.bar(x_pos, ram_kb, color=bar_color, alpha=0.72, width=0.5, label="DLL RAM Delta (KB)")
    ax1.set_xlabel("Dataset Size (N Pages)", fontsize=11, fontweight="bold", labelpad=8)
    ax1.set_ylabel("Heap Working-Set Delta (KB)", color=bar_color, fontsize=11, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor=bar_color)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(labels, fontsize=10, fontweight="bold")
    ax1.set_ylim(0, max(ram_kb) * 1.22)
    ax1.grid(axis="y", linestyle="--", alpha=0.35)

    for bar in bars:
        val = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            val + max(ram_kb) * 0.02,
            f"{val:.0f} KB",
            ha="center",
            va="bottom",
            color="#1f6fa8",
            fontweight="bold",
            fontsize=9,
        )

    ax2 = ax1.twinx()
    ax2.plot(x_pos, search_us, color="#e74c3c", linewidth=2.5, marker="o", markersize=7, label="Search Latency (us)")
    ax2.plot(x_pos, delete_us, color="#f39c12", linewidth=2.2, linestyle="--", marker="s", markersize=6, label="Delete Latency (us)")
    ax2.set_ylabel("O(N) Operation Latency (us)", color="#c0392b", fontsize=11, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#c0392b")
    ax2.set_ylim(0, max(max(search_us), max(delete_us)) * 1.28)

    for i, val in enumerate(search_us):
        offset_y = max(search_us) * (0.08 if i < 3 else 0.035)
        offset_x = -0.22 if i == 2 else (-0.18 if i >= 3 else -0.15)
        ax2.text(
            x_pos[i] + offset_x,
            val + offset_y,
            f"{val:.2f} us",
            color="#c0392b",
            fontsize=8.5,
            fontweight="bold",
            ha="right",
        )

    plt.title("Doubly Linked List Scaling: Memory Delta vs O(N) Latency", fontsize=13.5, fontweight="bold", pad=14)
    lines1, lbls1 = ax1.get_legend_handles_labels()
    lines2, lbls2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, lbls1 + lbls2, loc="upper left", frameon=True, shadow=True)

    plt.tight_layout()
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=200)
        print(f"Saved DLL scaling chart to {save_path}")

    if show:
        plt.show()
    plt.close(fig)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Plot DLL RAM and O(N) latency scaling chart.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=repo_root / "results" / "benchmark_metrics.csv",
        help="Input benchmark metrics CSV path",
    )
    parser.add_argument(
        "--save",
        type=Path,
        default=repo_root / "results" / "dll_performance.png",
        help="Output PNG chart path",
    )
    parser.add_argument("--show", action="store_true", help="Display interactive matplotlib window")
    args = parser.parse_args()

    if not args.show:
        matplotlib.use("Agg")

    rows = load_metrics(args.csv)
    render_dll_scaling(rows, args.save, show=args.show)


if __name__ == "__main__":
    main()
