import matplotlib.pyplot as plt


def mark_peak(ax, values, display_precision=".4g", line_color="tab:red"):
    peak = values.max()
    ax.axhline(peak, color=line_color, linewidth=1.0, linestyle=":", zorder=3)
    ax.annotate(
        f"max = {peak:{display_precision}}",
        xy=(0.98, peak),
        xycoords=("axes fraction", "data"),
        xytext=(-6, 6),
        textcoords="offset points",
        ha="right",
        va="bottom",
        fontsize=8,
        color=line_color,
        fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="white",
            edgecolor=line_color,
            linewidth=1.2,
            alpha=0.9,
        ),
        zorder=4,
    )


def plot_signal_window(
    ax,
    t,
    values,
    ylabel,
    title,
    display_precision=".4g",
    show_peak=True,
    line_color="tab:blue",
):
    ax.plot(t, values, color=line_color, linewidth=1.6)
    ax.set(xlabel="t [s]", ylabel=ylabel, title=title)
    ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.6)
    if show_peak:
        mark_peak(ax, values, display_precision=display_precision)
