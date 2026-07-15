import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Measured benchmark results (microseconds)
# ---------------------------------------------------------
N = [10, 100, 1000, 5000, 10000]

dll_search = [0.68, 5.64, 57.17, 352.19, 602.65]
ts_search  = [1.53, 13.64, 148.89, 733.50, 1417.31]

dll_delete = [0.74, 6.28, 74.22, 403.16, 796.65]
ts_delete  = [1.27, 13.39, 145.78, 712.12, 1527.33]

dll_back = [1.50e-03, 2.40e-03, 0.04, 0.02, 0.02]
ts_back  = [4.40e-03, 0.02, 0.19, 0.15, 0.15]

dll_forward = [1.40e-03, 1.60e-03, 8.30e-03, 6.80e-03, 5.70e-03]
ts_forward  = [4.70e-03, 0.02, 0.15, 0.15, 0.14]

# ---------------------------------------------------------
# 2. Plot configuration
# ---------------------------------------------------------
USE_LOG_SCALE = True 

fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Benchmark: Doubly Linked List vs Two-Stack Simulator', fontsize=16, fontweight='bold')

dll_style = {'color': '#0d6efd', 'marker': 'o', 'linewidth': 2, 'label': 'DLL (BrowserHistory)'}
ts_style  = {'color': '#dc3545', 'marker': 's', 'linewidth': 2, 'label': 'Two-Stack Simulator'}

def plot_chart(ax, data_dll, data_ts, title, use_log_y=False):
    ax.plot(N, data_dll, **dll_style)
    ax.plot(N, data_ts, **ts_style)
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel('Dataset size (N pages)', labelpad=10)
    ax.set_ylabel('Latency (microseconds)', labelpad=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    
    if USE_LOG_SCALE:
        ax.set_xscale('log')
        if use_log_y:
            ax.set_yscale('log')

# ---------------------------------------------------------
# 3. Render 2x2 latency comparison subplots
# ---------------------------------------------------------
plot_chart(axs[0, 0], dll_search, ts_search, 'Search', use_log_y=True)
plot_chart(axs[0, 1], dll_delete, ts_delete, 'Delete', use_log_y=True)
plot_chart(axs[1, 0], dll_back, ts_back, 'Back', use_log_y=True)
plot_chart(axs[1, 1], dll_forward, ts_forward, 'Forward', use_log_y=True)

# Add generous spacing so subplot labels do not overlap
plt.tight_layout(pad=4.0, w_pad=4.0, h_pad=4.0, rect=[0, 0, 1, 0.95])

plt.show()