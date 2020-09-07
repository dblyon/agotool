import os, sys
import pandas as pd
import numpy as np
import math
from collections import namedtuple
from itertools import combinations

homedir = os.path.expanduser("~")
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc, output_file, show
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, LassoSelectTool, WheelZoomTool, PanTool, SaveTool, TapTool, Legend, ZoomInTool, ZoomOutTool, Button, Toggle, BoxAnnotation
from bokeh.models import Circle

from bokeh.io import output_notebook, export_png, show
# output_notebook()
from bokeh.events import ButtonClick

from bokeh.plotting import figure, show
from bokeh.models.sources import ColumnDataSource
from bokeh.models import CustomJS, LabelSet, TapTool

import os
import pandas as pd
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models.tools import LassoSelectTool, TapTool
from bokeh.models.widgets.buttons import Button
from bokeh.models.callbacks import CustomJS

# fn_example = os.path.join(os.path.expanduser("~"), "modules/cpr/agotool/data/exampledata/DF_Bokeh_example_for_plotting_playground.txt")
# df = pd.read_csv(fn_example, sep="\t")
# df = df[df["etype"] != -20].reset_index(drop=True)
# df_as_cds = ColumnDataSource(data=df)
# hover = HoverTool(tooltips=[("term", "@term"), ("desc", "@description"), ("FG count", "@FG_count")])
# plot = figure(plot_width=1000, plot_height=500, title = "", toolbar_sticky=False, toolbar_location="above",
#            tools=[hover, BoxZoomTool(), ZoomInTool(), ZoomOutTool(), ResetTool(), PanTool(), SaveTool() ]) # , TapTool() ]) # , TapTool(), LassoSelectTool()
# renderer = plot.circle(x="logFDR", y="effectSize", source=df_as_cds,
#         size="FG_count_2_circle_size", fill_alpha="rank_2_transparency",
#         color="color", muted_color="color", muted_alpha=0.2,
#         nonselection_fill_alpha="rank_2_transparency", nonselection_line_alpha=1.0,
#         nonselection_fill_color="color", nonselection_line_color="color", selection_color="color", legend_label="category")

# plot.add_layout(Legend(), 'right')
# for category, group in df.groupby("category"):
#     color_of_etype = group.iloc[0].color
#     renderer_per_category = plot.circle(x="logFDR", y="effectSize", source=group,
#         size="FG_count_2_circle_size", fill_alpha="rank_2_transparency",
#         color="color", muted_color="color", muted_alpha=0.2, selection_color=color_of_etype,
#         # selection_fill_alpha="rank_2_transparency", selection_fill_color=color_of_etype,
#         nonselection_fill_alpha="rank_2_transparency", nonselection_fill_color=color_of_etype,
#         nonselection_line_color=color_of_etype, nonselection_line_alpha=1.0,  # nonselection_fill_alpha=0.2,
#         name="subplot_{}".format(category),
#         # legend_label=category)
#         legend_group="category")
#
#
#     labels = ColumnDataSource(data=dict(x=[], y=[], t=[], ind=[]))
#     plot.add_layout(LabelSet(x="x", y="y", text="t", y_offset=7, x_offset=7, source=labels, text_font_size="8pt"))
#
#
# plot.legend.location = "bottom_right"
# plot.legend.click_policy = "hide"
source = ColumnDataSource(dict(
    x=[1, 2, 3, 4, 5, 6],
    y=[1, 2, 3, 4, 5, 6], ))
plot = figure(plot_height=300, tools='',)
plot.circle( x='x', y='y', size=20, source=source)

lasso_select = LassoSelectTool(select_every_mousemove=False, )

# code_2_add_term_label_on_click = """
# const data = labels.data;
# for (var i = 0; i < points.selected.indices.length; i++) {
#     const ind = points.selected.indices[i];
#     data.x.push(points.data.logFDR[ind]);
#     data.y.push(points.data.effectSize[ind]);
#     data.t.push(points.data.term[ind]);
#     data.ind.push(ind);
# }
# console.log("DBL message: tapping ");
# labels.change.emit();
# """
# callback = CustomJS(args=dict(points=df_as_cds, labels=labels), code=code_2_add_term_label_on_click)
# plot.add_tools(TapTool(callback=callback))
# renderer_transparent = plot.circle(x="logFDR", y="effectSize", source=df_as_cds, size="FG_count_2_circle_size", alpha=0.0, color=None)

def update_selection_programmatically():
    source.selected.update(indices=[4])           # indices is updated but the update event (source.change.emit();) is not triggered
    source.selected.update(indices=[])           # indices is updated but the update event (source.change.emit();) is not triggered
    # df_as_cds.selected.update(indices=[])
    # labels.selected.update(indices=[])
    print("update_selection_programmatically triggered")

bt = Button(label="Clear selection please", button_type="success", width=50)
bt.on_click(update_selection_programmatically)

### this works fine
# bt.callback = CustomJS(
#     args=dict(source=source),
#     code="""
#         source.selected.indices = [4];
#         source.change.emit();
#     """
# )

# def update_selection(attr, old, new):
#     print('>> NEW SELECTION: {}'.format(new.indices))
#     # new.indices = [0]       # this works fine here

# source.on_change('selected', update_selection)

curdoc().add_root(column([plot, bt]))

