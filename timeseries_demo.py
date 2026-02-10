"""生成四条时间序列的示意图。

运行方式:
    python timeseries_demo.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def generate_series(n_points: int = 300, seed: int = 42):
    """生成四条不同模式的时间序列。"""
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 30, n_points)

    trend = 0.12 * t + 0.4 * np.sin(0.8 * t) + rng.normal(0, 0.15, n_points)
    seasonal = 1.2 * np.sin(2 * np.pi * t / 6) + rng.normal(0, 0.2, n_points)
    irregular = np.cumsum(rng.normal(0, 0.08, n_points))

    regime = np.piecewise(
        t,
        [t < 10, (t >= 10) & (t < 20), t >= 20],
        [
            lambda x: 0.5 * np.sin(1.1 * x),
            lambda x: 1.2 + 0.2 * np.sin(2.5 * x),
            lambda x: -0.8 + 0.3 * np.sin(1.4 * x),
        ],
    )
    regime += rng.normal(0, 0.12, n_points)

    return t, trend, seasonal, irregular, regime


def plot_series(output_path: str = "four_time_series_demo.png"):
    """绘制并保存示意图。"""
    t, trend, seasonal, irregular, regime = generate_series()

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axs = plt.subplots(2, 2, figsize=(12, 7), sharex=True)
    fig.suptitle("四条时间序列示意图", fontsize=16, y=0.98)

    axs = axs.ravel()
    series_list = [
        (trend, "趋势 + 弱周期"),
        (seasonal, "强周期序列"),
        (irregular, "随机游走序列"),
        (regime, "状态切换序列"),
    ]

    for ax, (series, title) in zip(axs, series_list):
        ax.plot(t, series, linewidth=1.7)
        ax.set_title(title, fontsize=11)
        ax.set_ylabel("值")

    for ax in axs[2:]:
        ax.set_xlabel("时间")

    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return Path(output_path).resolve()


if __name__ == "__main__":
    output = plot_series()
    print(f"示意图已保存至: {output}")
