"""Main module for the interactive distribution plot."""
import numpy as np
from bokeh.layouts import Column
from bokeh.models import ColumnDataSource
# from bokeh.models import MultiSelect
# from bokeh.models import Select
from bokeh.models.widgets import Div
from bokeh.models.widgets import RangeSlider
from bokeh.plotting import figure

from src.comparison_plot.callbacks import add_hover_tool
from src.comparison_plot.callbacks import add_select_tools
from src.comparison_plot.callbacks import create_group_widget
from src.comparison_plot.callbacks import create_view
from src.comparison_plot.callbacks import value_slider
from src.comparison_plot.process_inputs import process_inputs


def interactive_distribution_plot(
    doc,
    source,
    group_cols=None,
    subgroup_col=None,
    reference_id=None,
    figsize=(500, 150),
    x_padding=0.1,
    num_bins=50,
    clip=False,
):
    """Create an interactive distribution plot from a tidy DataFrame.

    The column for which clickable histograms will be generated must be called "value".
    The column identifying rows that belong to the same observation must be called "id".

    Args:
        doc (bokeh.Document):
            document to which to add the plot
        source (pd.DataFrame or str or pathlib.Path):
            Tidy DataFrame or location of the database file that contains tidy data.
            see: http://vita.had.co.nz/papers/tidy-data.pdf
        group_cols (list):
            Name of the columns that identify groups that will be plotted together.
            In case of a parameter comparison plot this would be the parameter group
            and parameter name by default.
        subgroup_col (str, optional):
            Name of a column according to whose values individual bricks will be
            color coded.
        figsize (tuple, optional): width, height in points
        x_padding (float, optional):
            the x_range is extended on each side by this factor of the range of the data
        num_bins (int, optional):
            number of bins

    """
    width, plot_height = figsize
    df, reference_df, group_cols = process_inputs(
        source=source,
        group_cols=group_cols,
        subgroup_col=subgroup_col,
        plot_height=plot_height,
        x_padding=x_padding,
        num_bins=num_bins,
        reference_id=reference_id,
        clip=clip,
    )

    grid = _create_grid(
        df=df,
        group_cols=group_cols,
        subgroup_col=subgroup_col,
        plot_height=plot_height,
        width=width,
    )
    doc.add_root(grid)

    source, plots = _plot_bricks(
        doc=doc, df=df, group_cols=group_cols, subgroup_col=subgroup_col,
        reference_df=reference_df,
    )

    return source, plots, grid


def _create_grid(df, subgroup_col, group_cols, plot_height, width):
    """Create the empty grid to which the contributions or parameters will be plotted.

    Args:
        df (pd.DataFrame): df to build histograms from
        group_cols (list):
            Name of the columns that identify groups that will be plotted together.
            In case of a parameter comparison plot this would be the parameter group
            and parameter name by default.
        subgroup_col (str, optional):
            Name of a column according to whose values individual bricks will be
            color coded.
        plot_height (int): height of the plots in pixels.
        width (int): width of the plots in pixels.

    """
    # cols_to_ignore = [
    #     "value",
    #     "binned_x",
    #     "rect_width",
    #     "xmin",
    #     "xmax",
    #     "dodge",
    #     "unit_height",
    #     "color",
    # ]
    # col_candidates = [
    #     col
    #     for col in df.columns
    #     if col not in cols_to_ignore and not col.startswith("index")
    # ]
    plots = [
        RangeSlider(start=0, end=1, value=(0, 1), name="placeholder_value_slider"),
        RangeSlider(start=0, end=1, value=(0, 1), name="placeholder_subgroup_widget"),
        # Select(
        #     title="Subgroup Column",
        #     value=subgroup_col,
        #     options=col_candidates,
        #     name="subgroup_selector",
        # ),
        # MultiSelect(
        #     title="Grouping Columns",
        #     value=group_cols,
        #     options=col_candidates,
        #     name="column_groups_selector",
        # ),
    ]
    if len(group_cols) == 0:
        fig = figure(
            title="",
            plot_height=plot_height,
            plot_width=width,
            tools="reset,save",
            y_axis_location="left",
            name="all",
        )
        plots.append(fig)
    else:
        gb = df.groupby(group_cols)
        old_group_tup = tuple(np.nan for name in group_cols)
        for tup, df_slice in gb:
            if not isinstance(tup, tuple):
                tup = (tup,)
            plots = _add_titles_if_group_switch(
                plots=plots,
                group_cols=group_cols,
                old_group_tup=old_group_tup,
                group_tup=tup,
            )
            fig_name = " ".join(str(x) for x in tup)
            fig = figure(
                title="{} {}".format(group_cols[-1].title(), str(tup[-1]).title()),
                plot_height=plot_height,
                plot_width=width,
                tools="reset,save",
                y_axis_location="left",
                x_range=(df_slice["xmin"].min(), df_slice["xmax"].max()),
                name=fig_name,
            )
            fig = _style_plot(fig)
            plots.append(fig)
            old_group_tup = tup
    grid = Column(*plots)
    return grid


def _add_titles_if_group_switch(plots, group_cols, old_group_tup, group_tup):
    nr_levels = len(group_cols) - 1
    for level in range(nr_levels):
        old_name = old_group_tup[level]
        new_name = group_tup[level]
        if old_name != new_name:
            title = "<b>{} {}</b>".format(
                group_cols[level].title(), str(new_name).title()
            )
            percent = "{}%".format(100 * (1.5 * (nr_levels - level)))
            plots.append(Div(text=title, name=title, style={"font-size": percent}))
    return plots


def _plot_bricks(doc, df, reference_df, group_cols, subgroup_col):
    """Create the ColumnDataSource and replace the plots and widgets.

    Args:
        df (pd.DataFrame): Tidy DataFrame.
        reference_df (pd.DataFrame): DataFrame with x positions where to plot lines.
        group_cols (list):
            Name of the columns that identify groups that will be plotted together.
            In case of a parameter comparison plot this would be the parameter group
            and parameter name by default.
        subgroup_col (str):
            Name of a column according to whose values individual bricks will be
            color coded.

    """
    all_elements = doc.roots[0].children
    source = ColumnDataSource(df)
    widget = create_group_widget(source=source, subgroup_col=subgroup_col)
    all_elements[1] = widget

    plots = []
    tuples = _create_tuples(df=df, group_cols=group_cols)
    for tup in tuples:
        fig_name = " ".join(str(x) for x in tup)
        fig = doc.get_model_by_name(fig_name)
        if fig is None:
            raise ValueError(
                "Figure {} not found in the bokeh document.".format(fig_name))
        fig.renderers = []
        fig.tools = []
        df_slice = df[(df[group_cols] == tup).all(axis=1)]
        group_index = df_slice.index
        view = create_view(
            source=source,
            group_index=group_index,
            subgroup_col=subgroup_col,
            widget=widget,
        )

        # get values from the reference_df
        ref_slice = reference_df[(reference_df[group_cols] == tup).all(axis=1)]
        x_vals = ref_slice["value"]
        fig = _add_renderers(
            fig=fig, source=source, view=view, group_cols=group_cols,
            x_vals_for_lines=x_vals)
        plots.append(fig)

    # this has to happen at the end because all plots must be passed to this
    all_elements[0] = value_slider(source=source, plots=plots,)

    return source, all_elements


def _create_tuples(df, group_cols):
    if len(group_cols) == 0:
        tuples = ["all"]
    elif len(group_cols) == 1:
        tuples = [(x,) for x in df[group_cols[0]].unique()]
    else:
        tuples = list(set(zip(*[df[col] for col in group_cols])))
    return tuples


def _add_renderers(fig, source, view, group_cols, x_vals_for_lines):
    point_glyph = fig.rect(
        source=source,
        view=view,
        x="binned_x",
        width="rect_width",
        y="dodge",
        height=1,
        color="color",
        selection_color="color",
        nonselection_color="color",
        alpha=0.5,
        selection_alpha=0.7,
        nonselection_alpha=0.1,
    )

    for val in x_vals_for_lines:
        fig.line(
            x=[val, val],
            y=[0, source.data["dodge"].max() + 1],
            line_width=1.5, line_color="firebrick"
        )

    if "ci_lower" in source.column_names and "ci_upper" in source.column_names:
        fig.hbar(
            source=source,
            view=view,
            y="dodge",
            left="ci_lower",
            right="ci_upper",
            height=0.01,
            alpha=0.0,
            selection_alpha=0.7,
            nonselection_alpha=0.0,
            color="color",
            selection_color="color",
            nonselection_color="color",
        )
    fig = add_hover_tool(
        fig=fig, point_glyph=point_glyph, source=source, group_cols=group_cols
    )
    fig = add_select_tools(fig=fig, point_glyph=point_glyph, source=source,)
    return fig


def _style_plot(fig):
    fig.xaxis.minor_tick_line_color = None
    fig.xaxis.axis_line_color = None
    fig.xaxis.major_tick_line_color = None
    fig.yaxis.minor_tick_line_color = None
    fig.yaxis.axis_line_color = None
    fig.yaxis.major_tick_line_color = None

    fig.title.vertical_align = "top"
    fig.title.text_alpha = 70
    fig.title.text_font_style = "normal"
    fig.outline_line_color = None
    fig.min_border_top = 20
    fig.min_border_bottom = 20
    fig.xgrid.visible = False
    fig.ygrid.visible = False
    fig.sizing_mode = "scale_width"

    return fig
