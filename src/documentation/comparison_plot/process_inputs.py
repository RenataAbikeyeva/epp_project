"""Process inputs of the interactive distribution plot."""
import os
import warnings
from pathlib import Path

import pandas as pd

from src.comparison_plot.manipulate_data import add_hist_cols
from src.comparison_plot.manipulate_data import clean_data


def process_inputs(
    source,
    group_cols,
    subgroup_col,
    plot_height,
    x_padding,
    num_bins,
    reference_id,
    clip,
):
    df = _handle_source_type(source)

    if clip:
        df["value"] = df.groupby(group_cols)["value"].transform(_clip_values)

    group_cols = _process_group_cols(group_cols)
    df = clean_data(df=df, group_cols=group_cols, subgroup_col=subgroup_col,)

    if reference_id is not None:
        reference_df = df[df["id"] == reference_id]
        # necessary to clean again to get the dodge right.
        df = clean_data(
            df=df[df["id"] != reference_id],
            group_cols=group_cols,
            subgroup_col=subgroup_col,
        )
    else:
        reference_df = pd.DataFrame(columns=["id", "value"] + group_cols)

    df = add_hist_cols(
        df=df, group_cols=group_cols, x_padding=x_padding, num_bins=num_bins,
    )

    # plot_height = _determine_plot_height(
    #     figure_height=figure_height, data=df, group_cols=group_cols
    # )

    return df, reference_df, group_cols


def _process_group_cols(group_cols):
    if group_cols is None:
        group_cols = []
    elif isinstance(group_cols, str):
        group_cols = [group_cols]
    return group_cols


def _handle_source_type(source):
    if isinstance(source, pd.DataFrame):
        df = source
    elif isinstance(source, Path) or isinstance(source, str):
        assert os.path.exists(
            source
        ), f"The path {source} you specified does not exist."
        database = load_database(path=source)  # noqa
        raise NotImplementedError("Databases not supported yet.")
    return df


def _determine_plot_height(figure_height, data, group_cols):
    """Calculate the height alloted to each plot in pixels.

    Args:
        figure_height (int): height of the entire figure in pixels
        data (pd.DataFrame): the data to be plotted

    Returns:
        plot_height (int): Plot height in pixels.

    """
    if figure_height is None:
        figure_height = 1000

    if len(group_cols) == 0:
        n_groups = 0
        n_plots = 1
    elif len(group_cols) == 1:
        n_groups = 0
        n_plots = len(data.groupby(group_cols))
    else:
        n_groups = len(data.groupby(group_cols[:-1]))
        n_plots = len(data.groupby(group_cols))
    space_of_titles = n_groups * 50
    available_space = figure_height - space_of_titles
    plot_height = int(available_space / n_plots)
    if plot_height < 20:
        warnings.warn(
            "The figure height you specified results in very small ({}) ".format(
                plot_height
            )
            + "plots which may not render well. Adjust the figure height "
            "to a larger value or set it to None to get a larger plot. "
            "Alternatively, you can click on the Reset button "
            "on the right of the plot and your plot should render correctly."
        )
    return plot_height


def _clip_values(group):
    mean = group.mean()
    std = group.std()
    lower = mean - 3 * std
    upper = mean + 3 * std
    new_vals = group.where(group >= lower, lower)
    new_vals = new_vals.where(new_vals <= upper, upper)
    return new_vals
