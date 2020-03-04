# ===========================================================
# Remove this when calling the script from waf
import sys
from pathlib import Path
p = Path(__file__).resolve().parent.parent.parent
sys.path.append(f"{p}/")
# ===========================================================
from src.comparison_plot.interactive_distribution_plot import interactive_distribution_plot
import pandas as pd
import numpy as np
from bokeh.io import save
from bokeh.document import Document

if __name__ == "__main__":
    # concat the true and calculated data
    data_true = pd.read_csv("../analysis/true_df.csv")
    data_true["algorithm"] = "true_solution"
    data_calc = pd.read_csv("../analysis/calculated_21_df.csv")
    data = pd.concat([data_true, data_calc], sort=True)
    data.rename(columns={"algorithm": "id"}, inplace=True)

    # for testing purposes
    small_data = data[data["criterion"] == "rosenbrock"].copy()

    doc = Document()
    source, plots, grid = interactive_distribution_plot(
        doc=doc,
        source=small_data,
        group_cols=["criterion", "constraints", "parameters"],
        reference_id="true_solution",
        clip=False
    )

    save(grid, "comparison_plots.html", title="Benchmark Plot")
