import argparse
import csv
from pathlib import Path
import matplotlib


def load_metrics(csv_path: Path):
    rows = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({k: float(v) if k != "N" else int(v) for k, v in r.items()})
    return rows


def render_comparison(rows, save_path: Path, show: bool = False):
    import matplotlib.pyplot as plt

    N = [r["N"] for r in rows]
    dll_search = [r["dll_search_us"] for r in rows]
    ts_search = [r["ts_search_us"] for r in rows]
    dll_delete = [r["dll_delete_us"] for r in rows]
    ts_delete = [r["ts_delete_us"] for r in rows]
    dll_back = [r["dll_back_us"] for r in rows]
    ts_back = [r["ts_back_us"] for r in rows]
    dll_forward = [r["dll_forward_us"] for r in rows]
    ts_forward = [r["ts_forward_us"] for r in rows]

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "Benchmark: Doubly Linked List vs Two-Stack Simulator (Windows QPC)",
        fontsize=15,
        fontweight="bold",
    )

    dll_style = {"color": "#0d6efd", "marker": "o", "linewidth": 2, "label": "DLL (BrowserHistory)"}
    ts_style = {"color": "#dc3545", "marker": "s", "linewidth": 2, "label": "Two-Stack Simulator"}

    def plot_panel(ax, data_dll, data_ts, title):
        ax.plot(N, data_dll, **dll_style)
        ax.plot(N, data_ts, **ts_style)
        ax.set_title(title, fontweight="bold")
        ax.set_xlabel("Dataset size (N pages)", labelpad=8)
        ax.set_ylabel("Latency (microseconds)", labelpad=8)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.grid(True, which="both", linestyle="--", alpha=0.45)
        ax.legend()

    plot_panel(axs[0, 0], dll_search, ts_search, "Search (Keyword Scan)")
    plot_panel(axs[0, 1], dll_delete, ts_delete, "Delete (By URL)")
    plot_panel(axs[1, 0], dll_back, ts_back, "Back Navigation O(1)")
    plot_panel(axs[1, 1], dll_forward, ts_forward, "Forward Navigation O(1)")

    plt.tight_layout(pad=3.5, w_pad=3.5, h_pad=3.5, rect=[0, 0, 1, 0.94])

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=200)
        print(f"Saved comparison chart to {save_path}")

    if show:
        plt.show()
    plt.close(fig)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Plot DLL vs Two-Stack benchmark metrics.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=repo_root / "results" / "benchmark_metrics.csv",
        help="Input benchmark metrics CSV path",
    )
    parser.add_argument(
        "--save",
        type=Path,
        default=repo_root / "results" / "benchmark_latency.png",
        help="Output PNG chart path",
    )
    parser.add_argument("--show", action="store_true", help="Display interactive matplotlib window")
    args = parser.parse_args()

    if not args.show:
        matplotlib.use("Agg")

    rows = load_metrics(args.csv)
    render_comparison(rows, args.save, show=args.show)


if __name__ == "__main__":
    main()
