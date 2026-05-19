from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV_PATH = Path(__file__).resolve().parents[1] / "outputs_2" / "speed_comparision.csv"

def normalize_value(value: int) -> str:

	if (pd.isna(value)) or value is None:
		return ""

	text = str(value).strip()
	return "" if text == "None" else text


def build_label(row: pd.Series) -> str:
	parts = [normalize_value(row["variant"])]
	for column in ["schedule", "chunk", "blocksize"]:
		if column == "blocksize":
			val = row["blocksize"]
			if pd.isna(val):
				value = ""
			else:
				try:
					value = f"{int(val) // 1024}kb"
				except Exception:
					value = normalize_value(val)
		else:
			value = normalize_value(row[column])

		if value:
			parts.append(value)

	return "-".join(parts)


def main() -> None:
	df = pd.read_csv(
		CSV_PATH,
		sep=";",
		header=None,
		names=["variant", "range", "schedule", "chunk", "blocksize", "avg_time", "std_dev"],
		skipinitialspace=True,
		encoding="utf-8",
	)

	df["variant"] = df["variant"].astype(str).str.strip()
	df["range"] = df["range"].astype(str).str.strip()
	df["schedule"] = df["schedule"].astype(str).str.strip()

	def _to_optional_int(series: pd.Series) -> pd.Series:
		s = series.astype(str).str.strip()
		s = s.replace({"None": "", "nan": ""})
		return pd.to_numeric(s, errors="coerce").astype("Int64")

	df["chunk"] = _to_optional_int(df["chunk"])
	df["blocksize"] = _to_optional_int(df["blocksize"])

	df["avg_time"] = pd.to_numeric(df["avg_time"].astype(str).str.replace(",", ".", regex=False))
	df["std_dev"] = pd.to_numeric(df["std_dev"].astype(str).str.replace(",", ".", regex=False))
	df["label"] = df.apply(build_label, axis=1)

	range_order = df["range"].drop_duplicates().tolist()
	variant_order = df.drop_duplicates(subset=["variant", "schedule", "chunk", "blocksize"])["label"].tolist()
	# Assign colors to variants; handle Colormap types that don't expose a `.colors` attribute
	cmap = plt.get_cmap("tab10")
	colors_attr = getattr(cmap, "colors", None)
	if colors_attr is not None:
		cmap_colors = list(colors_attr)
	else:
		# Fallback: sample 10 distinct colors from the colormap
		cmap_colors = [cmap(i / 9) for i in range(10)]

	if not cmap_colors:
		cmap_colors = [(0.0, 0.0, 0.0)]

	variant_colors = {label: cmap_colors[i % len(cmap_colors)] for i, label in enumerate(variant_order)}

	fig, axis = plt.subplots(figsize=(14, 7), dpi=150, constrained_layout=True)

	x = np.arange(len(range_order))
	bar_width = min(0.8 / max(len(variant_order), 1), 0.16)
	offsets = (np.arange(len(variant_order)) - (len(variant_order) - 1) / 2) * bar_width

	for index, label in enumerate(variant_order):
		variant_df = df[df["label"] == label].set_index("range").reindex(range_order)
		bars = axis.bar(
			x + offsets[index],
			variant_df["avg_time"],
			bar_width,
			yerr=variant_df["std_dev"],
			label=label,
			color=variant_colors[label],
			edgecolor="black",
			linewidth=0.6,
			capsize=4,
			error_kw={"elinewidth": 1.1},
		)

		axis.bar_label(bars, fmt="%.3f", padding=2, fontsize=7)

	axis.set_xticks(x)
	axis.set_xticklabels(range_order)
	axis.set_xlabel("Data range")
	axis.set_ylabel("Time [s]")
	axis.set_title("Speed comparison by data range", fontsize=14, weight="bold")
	axis.grid(True, axis="y", linestyle="--", alpha=0.35)
	axis.set_axisbelow(True)
	axis.legend(title="Variant")

	plt.show()


if __name__ == "__main__":
	main()
