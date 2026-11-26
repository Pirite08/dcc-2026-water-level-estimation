#!/usr/bin/env python3
"""Plot transcribed report aggregates; this script does not evaluate a model.

Run from any directory: python path/to/tools/plot_recorded_results.py
Requires only matplotlib beyond the Python standard library. CSV paths are
resolved relative to this file, not to the current working directory.
"""

from __future__ import annotations

import argparse
import csv
import os
from decimal import Decimal
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ft2font import FT2Font

ROOT = Path(__file__).resolve().parents[1]
MINT = "#80AA90"
BASELINE = "#CCD3CE"
INK = "#17221C"
MUTED = "#56625B"
GRID = "#E4E9E5"
BACKGROUND = "#FCFDFC"
SAMPLE_COUNT = 30809


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def load_results(results_dir: Path) -> tuple[list[dict], list[dict]]:
    """Check aggregate structure and units, not original prediction accuracy."""
    metrics = read_csv(results_dir / "overall_metrics.csv")
    counts = read_csv(results_dir / "error_threshold_counts.csv")
    assert [row["metric"] for row in metrics] == ["RMSE", "MAE", "absolute_error_P95"]
    assert [Decimal(row["absolute_error_threshold_m"]) for row in counts] == [
        Decimal("0.2"), Decimal("0.5"), Decimal("1.0")
    ]
    for row in metrics + counts:
        assert int(row["test_sample_count"]) == SAMPLE_COUNT
        assert row["source_id"] == "report_2026_09_21"
    for row in metrics:
        assert row["unit"] == "m"
        assert all(Decimal(row[key]).is_finite() and Decimal(row[key]) >= 0
                   for key in ("baseline_v3", "improved_v4"))
    for row in counts:
        assert row["comparison"] == "strictly_greater_than"
        assert row["aggregation"] == "nested_cumulative"
        assert all(0 <= int(row[key]) <= SAMPLE_COUNT
                   for key in ("baseline_v3_count", "improved_v4_count"))
    for key in ("baseline_v3_count", "improved_v4_count"):
        values = [int(row[key]) for row in counts]
        assert values == sorted(values, reverse=True), "Nested thresholds must be non-increasing."
    return metrics, counts


def choose_font(explicit_path: str | None = None) -> tuple[str, bool]:
    """Prefer installed Pretendard; verify actual Korean glyphs before use."""
    candidates: list[Path] = []
    if explicit_path:
        candidates.append(Path(explicit_path).expanduser())
    local_fonts = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/Windows/Fonts"
    candidates.extend([
        local_fonts / "Pretendard-Regular.ttf",
        Path("C:/Windows/Fonts/Pretendard-Regular.ttf"),
        Path("C:/Windows/Fonts/NotoSansKR-Regular.ttf"),
        Path("C:/Windows/Fonts/malgun.ttf"),
        Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
    ])
    for font in font_manager.fontManager.ttflist:
        if any(word in font.name.lower() for word in ("pretendard", "noto sans kr", "nanum", "malgun")):
            candidates.append(Path(font.fname))
    for path in candidates:
        if path.is_file():
            face = FT2Font(str(path))
            if all(face.get_char_index(ord(char)) for char in "수위추정기록결과초과오류감소"):
                font_manager.fontManager.addfont(str(path))
                return font_manager.FontProperties(fname=str(path)).get_name(), True
    if explicit_path:
        raise ValueError("The requested font is missing or lacks Korean glyphs.")
    return "DejaVu Sans", False


def apply_style(font_name: str) -> None:
    plt.rcParams.update({
        "font.family": font_name, "font.size": 13, "text.color": INK,
        "axes.labelcolor": MUTED, "xtick.color": INK, "ytick.color": MUTED,
        "axes.unicode_minus": False, "svg.fonttype": "path",
        "figure.facecolor": BACKGROUND, "axes.facecolor": BACKGROUND,
        "savefig.facecolor": BACKGROUND,
    })


def style_axis(axis, top: float, ticks: list[float], unit: str, korean: bool) -> None:
    axis.set_ylim(0, top)
    axis.set_xlim(-0.65, 1.65)
    axis.set_yticks(ticks)
    axis.set_ylabel(unit, fontsize=12, labelpad=6)
    model_labels = ["초기 모델\n(v3)", "보완 모델\n(v4)"] if korean else ["Initial model\n(v3)", "Revised model\n(v4)"]
    axis.set_xticks([0, 1], model_labels, fontsize=13 if korean else 11)
    axis.tick_params(axis="both", length=0, pad=9)
    axis.grid(axis="y", color=GRID, linewidth=0.8)
    axis.set_axisbelow(True)
    for side in ("top", "right", "left"):
        axis.spines[side].set_visible(False)
    axis.spines["bottom"].set_color("#B9C4BC")


def save_figure(figure, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "svg"):
        figure.savefig(output_dir / f"{stem}.{extension}", dpi=180,
                       metadata={"Creator": "DCC recorded report aggregates"})
    plt.close(figure)


def plot_metrics(metrics: list[dict], output_dir: Path, korean: bool) -> None:
    figure = plt.figure(figsize=(12, 6.4))
    title = "기록된 전체 오차는 세 지표 모두 감소했습니다" if korean else "All three recorded aggregate errors decreased"
    subtitle = "같은 내부 test 30,809장 · 낮을수록 좋음 · 모든 축은 0~18 cm" if korean else "Same internal test: 30,809 images | Lower is better | All axes: 0–18 cm"
    figure.text(0.055, 0.925, title, fontsize=23, weight="bold")
    figure.text(0.055, 0.866, subtitle, fontsize=13, color=MUTED)
    labels = ["RMSE", "MAE", "절대오차 P95" if korean else "Absolute error P95"]
    descriptions = (["큰 오차에 민감", "절대오차의 평균", "95% 지점의 절대오차"] if korean else
                    ["Sensitive to large errors", "Mean absolute error", "95th percentile of absolute error"])
    for index, row in enumerate(metrics):
        left = 0.08 + index * 0.315
        center = left + 0.118
        before, after = Decimal(row["baseline_v3"]), Decimal(row["improved_v4"])
        reduction = (before - after) / before * 100
        values = [float(before * 100), float(after * 100)]
        figure.text(center, 0.76, labels[index], ha="center", fontsize=17, weight="bold")
        figure.text(center, 0.714, descriptions[index], ha="center", fontsize=12, color=MUTED)
        axis = figure.add_axes([left, 0.285, 0.245, 0.365])
        style_axis(axis, 18, [0, 5, 10, 15], "cm", korean)
        axis.bar([0, 1], values, width=0.52, color=[BASELINE, MINT], zorder=3)
        for x_value, value in enumerate(values):
            axis.text(x_value, value + 0.65, f"{value:.2f}", ha="center", fontsize=15, weight="bold")
        change_label = f"{reduction:.2f}% 감소" if korean else f"{reduction:.2f}% decrease"
        figure.text(center, 0.14, change_label, ha="center", fontsize=15, weight="bold", color="#436650")
    caption = ("출처: 2026.09.21 연구보고서 16쪽, 표 12 · m 기록값을 cm로 변환\n"
               "감소율은 보고서의 반올림 수치로 계산했습니다. 원예측 재계산이나 외부 평가 결과가 아닙니다."
               if korean else
               "Source: research report dated 2026-09-21, p.16, Table 12 | Recorded m values converted to cm\n"
               "Changes use rounded report values. These are not recomputed predictions or external evaluation results.")
    figure.text(0.055, 0.048, caption, fontsize=11, color=MUTED, linespacing=1.55)
    save_figure(figure, output_dir, "recorded_metrics")


def plot_counts(counts: list[dict], output_dir: Path, korean: bool) -> None:
    figure = plt.figure(figsize=(12, 6.4))
    title = "1 m를 넘는 큰 오류는 28장에서 31장으로 늘었습니다" if korean else "Errors over 1 m increased from 28 to 31 images"
    subtitle = ("절대오차 초과 건수 · 같은 내부 test 30,809장 · 패널마다 세로축 범위가 다름" if korean else
                "Absolute-error threshold counts | Same 30,809 images | Each panel has a different y-axis range")
    figure.text(0.055, 0.925, title, fontsize=23, weight="bold")
    figure.text(0.055, 0.866, subtitle, fontsize=13, color=MUTED)
    limits = [(1100, [0, 500, 1000]), (250, [0, 100, 200]), (40, [0, 10, 20, 30, 40])]
    for index, row in enumerate(counts):
        left = 0.08 + index * 0.315
        center = left + 0.118
        threshold = f"{Decimal(row['absolute_error_threshold_m']):g}"
        if threshold == "1.0":
            threshold = "1"
        label = f"{threshold} m 초과" if korean else f"Over {threshold} m"
        figure.text(center, 0.76, label, ha="center", fontsize=17, weight="bold")
        values = [int(row["baseline_v3_count"]), int(row["improved_v4_count"])]
        axis = figure.add_axes([left, 0.285, 0.245, 0.365])
        top, ticks = limits[index]
        style_axis(axis, top, ticks, "장" if korean else "images", korean)
        axis.bar([0, 1], values, width=0.52, color=[BASELINE, MINT], zorder=3)
        for x_value, value in enumerate(values):
            axis.text(x_value, value + top * 0.037, f"{value:,}", ha="center", fontsize=16, weight="bold")
        delta = values[1] - values[0]
        change = f"{abs(delta):,}장 {'감소' if delta < 0 else '증가'}" if korean else f"{delta:+,} images"
        figure.text(center, 0.14, change, ha="center", fontsize=15, weight="bold",
                    color="#436650" if delta < 0 else INK)
    caption = ("출처: 2026.09.21 연구보고서 21쪽 · 모든 세로축은 0부터 시작합니다.\n"
               "서로 겹치는 누적 조건이므로 건수를 합산할 수 없습니다. 원예측을 다시 평가한 결과가 아닙니다."
               if korean else
               "Source: research report dated 2026-09-21, p.21 | Every y-axis starts at zero.\n"
               "These are overlapping cumulative thresholds: do not sum the counts. Predictions were not reevaluated.")
    figure.text(0.055, 0.048, caption, fontsize=11, color=MUTED, linespacing=1.55)
    save_figure(figure, output_dir, "recorded_error_counts")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "assets")
    parser.add_argument("--font", help="Optional local Korean TTF/OTF path; fonts are never downloaded.")
    arguments = parser.parse_args()
    metrics, counts = load_results(arguments.results_dir)
    name, korean = choose_font(arguments.font)
    apply_style(name)
    plot_metrics(metrics, arguments.output_dir, korean)
    plot_counts(counts, arguments.output_dir, korean)
    print(f"Font: {name}; Korean glyphs verified: {korean}")
    print("Validated: report aggregate units, 30,809-image scope, non-increasing nested threshold counts.")
    print("Generated recorded_metrics and recorded_error_counts as PNG + SVG.")
    print("Scope: rounded report aggregates only; no training, inference, or raw-prediction metric recomputation.")


if __name__ == "__main__":
    main()
