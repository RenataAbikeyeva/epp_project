# import numpy as np
import pandas as pd
from bokeh.document import Document
from bokeh.io import save

from bld.project_paths import project_paths_join as ppj
from src.comparison_plot.interactive_distribution_plot import (
    interactive_distribution_plot,
)

if __name__ == "__main__":
    # concat the true and calculated data
    data_true = pd.read_csv(ppj("IN_ANALYSIS", "true_df.csv"))
    data_true["algorithm"] = "true_solution"
    data_calc = pd.read_csv(ppj("OUT_ANALYSIS", "21_calculated_df.csv"))
    data = pd.concat([data_true, data_calc], sort=True)
    data.rename(columns={"algorithm": "id"}, inplace=True)

    # for testing purposes
    small_data = data[data["criterion"] == "rosenbrock"].copy()

    doc = Document()
    source, plots, grid = interactive_distribution_plot(
        doc=doc,
        source=data,
        group_cols=["criterion", "constraints", "parameters"],
        reference_id="true_solution",
        clip=False,
    )

    save(grid, ppj("OUT_FIGURES", "comparison_plots.html"), title="Benchmark Plot")
