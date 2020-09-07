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
output_file("bokeh_testing.html")

from bokeh.events import ButtonClick

from bokeh.plotting import figure, show
from bokeh.models.sources import ColumnDataSource
from bokeh.models import CustomJS, LabelSet, TapTool

# fn_output =  os.path.join(os.path.expanduser("~"), "modules/cpr/agotool/app/python/bokeh_testing.html")
# output_file(fn_output)
### run "python bokeh_testing.py" --> creates bokeh_testing.html

# fn_example = os.path.join(os.path.expanduser("~"), "modules/cpr/agotool/data/exampledata/DF_Bokeh_example_for_plotting_playground.txt")
fn_example = os.path.join(os.path.expanduser("~"), "modules/cpr/agotool/data/exampledata/DF_Bokeh_example_for_plotting_playground_small.txt")
df = pd.read_csv(fn_example, sep="\t")
df = df[df["etype"] != -20].reset_index(drop=True)
del df["FG_IDs"]
source = ColumnDataSource(data=df)

# links need be replaced with proper edge values based on hierarchy
links = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 5],
    3: [1, 4],
    4: [1, 3],
    5: [2, 3, 4]
}

### Hover
hover = HoverTool(tooltips=[("term", "@term"), ("desc", "@description"), ("FG count", "@FG_count")])
plot = figure(plot_width=1000, plot_height=500, title = "", toolbar_sticky=False, toolbar_location="above",
           tools=[hover, BoxZoomTool(), ZoomInTool(), ZoomOutTool(), ResetTool(), PanTool(), SaveTool() ]) # , TapTool() ]) # , TapTool(), LassoSelectTool()
plot.title.text_font_size, plot.title.align = "1pt", "center"
plot.xaxis.axis_label, plot.yaxis.axis_label = "-log(corrected p_value)", "effect size"
plot.xaxis.axis_label_text_font_style, plot.yaxis.axis_label_text_font_style = "normal", "normal"
plot.xgrid.grid_line_alpha, plot.ygrid.grid_line_alpha = 0.5, 0.5
plot.xaxis.minor_tick_line_color, plot.yaxis.minor_tick_line_color = None, None
# labels = ColumnDataSource(data=dict(x=[], y=[], t=[], ind=[]))

legend_it = []
for category, group in df.groupby("category"):
    color_of_etype = group.iloc[0].color
    renderer_per_category = plot.circle(x="logFDR", y="effectSize", source=group,
        size="FG_count_2_circle_size", fill_alpha="rank_2_transparency",
        color="color", muted_color="color", muted_alpha=0.2,
        nonselection_fill_alpha="rank_2_transparency", nonselection_line_alpha=1.0,  # nonselection_fill_alpha=0.2,
        nonselection_fill_color=color_of_etype, nonselection_line_color=color_of_etype, selection_color=color_of_etype,
        name="subplot_{}".format(category))
    legend_it.append((category, [renderer_per_category]))

labels = ColumnDataSource(data=dict(x=[], y=[], t=[], ind=[]))
plot.add_layout(LabelSet(x="x", y="y", text="t", y_offset=7, x_offset=7, source=labels, text_font_size="8pt"))

legend = Legend(items=legend_it, location=(10, 0))
legend.click_policy = "hide" #"mute"
plot.add_layout(legend, "right")
# plot.legend.location = (10, 0)
# plot.legend.click_policy = "hide"

### if on_click() is outside of circle --> change labels.data to be empty, else do the existing loop
code_2_add_term_label_on_click = """
const data = labels.data;
for (var i = 0; i < points.selected.indices.length; i++) {
    const ind = points.selected.indices[i];
    data.x.push(points.data.logFDR[ind]);
    data.y.push(points.data.effectSize[ind]);
    data.t.push(points.data.term[ind]);
    data.ind.push(ind);
}
console.log("DBL message: tapping ");
labels.change.emit();
"""
callback = CustomJS(args=dict(points=source, labels=labels), code=code_2_add_term_label_on_click)
plot.add_tools(TapTool(callback=callback))
renderer_transparent = plot.circle(x="logFDR", y="effectSize", source=source, size="FG_count_2_circle_size", alpha=0.0, color=None, name="plot_transparent")

# labels = LabelSet(x="logFDR", y="effectSize", source=source, text="term", level="glyph", render_mode="canvas") # x_offset=3, y_offset=3,
# plot.add_layout(labels)
selected_circle = Circle()
nonselected_circle = Circle()
renderer_transparent.selection_glyph = selected_circle
renderer_transparent.nonselection_glyph = nonselected_circle


# def sel_cb(attr, old, new):
#     if new:
#         labels = ColumnDataSource(data=dict(x=[], y=[], t=[], ind=[]))
#     else:
#         pass
#
# source.selected.on_change('indices', sel_cb)


# button_reset_labels = Button()
# button_reset_labels.js_on_click(CustomJS(args=dict(plot=plot), code="""
#     plot.reset.emit()
# """))
# on button click run python code ( https://docs.bokeh.org/en/latest/docs/user_guide/styling.html#visible-property )
# p.select(name="mycircle") --> renderer_transparent
def reset_labels(): # running a python callback --> works
    print('running Python callback reset_labels')
    # global labels
    # labels = ColumnDataSource(data=dict(x=[], y=[], t=[], ind=[]))
    # return labels
    # renderer_per_category.selection_glyph = None
    # renderer_per_category.nonselection_glyph = None
    # renderer_transparent.selection_glyph = None
    # renderer_transparent.nonselection_glyph = None
    # source.selected.update(indices=[2])
    # source.selected.unapply_theme()
    # global source
    # source = ColumnDataSource(data=df)
    source.selected.update(indices=[])
    labels.selected.update(indices=[])
    source.selected.indices = []
    labels.selected.indices = []
    # LabelSet.select(None)

button_reset_labels = Button(label="Button reset labels Python callback", button_type="success", width=100)
button_reset_labels.on_click(reset_labels)


code_2_reset_labels = """
console.log('DBL JS callback: code_2_reset_labels ');

for (var i = 0; i < points.selected.indices.length; i++) {
    const ind = points.selected.indices[i];
    data.x.pop();
    data.y.pop();
    data.t.pop();
    data.ind.pop();
}
labels.change.emit();

labels.selected.indices = [];
labels.change.emit();

points.selected.indices = [];
points.change.emit();

source.selected.indices = [];
source.change.emit();
"""
callback_2 = CustomJS(args=dict(points=source, labels=labels, source=source), code=code_2_reset_labels)
button_reset_labels2 = Button(label="Button reset labels JS callback")
# button_reset_labels.on_click(reset_labels)
button_reset_labels2.js_on_event(ButtonClick, callback_2)

# yellow_box = BoxAnnotation(left=6, right=12, fill_color='yellow', fill_alpha=0.2)
# plot.add_layout(yellow_box)
# toggle_labels = Toggle(label="Toggle labels", button_type="success", active=True)
# toggle_labels.js_link('active', yellow_box, 'visible')

# blue_box = BoxAnnotation(left=10, right=14, fill_color='blue', fill_alpha=0.2)
# plot.add_layout(blue_box)
# toggle_edges = Toggle(label="Toggle edges", button_type="success", active=True)
# toggle_edges.js_link('active', blue_box, 'visible')

# plot.add_tools(Toggle(callback=callback))
# plot.add_tools(TapTool(callback=callback), BoxZoomTool(), ZoomInTool(), ZoomOutTool(), ResetTool(), PanTool(), SaveTool())

# callback = CustomJS(args=dict(points=points, labels=labels), code=code_2_add_term_label_on_click)
# plot.add_tools(LassoSelectTool(callback=callback))

show(column(plot, button_reset_labels, button_reset_labels2))
# curdoc().add_root(plot)
# curdoc().add_root(column(plot, button_reset_labels, button_reset_labels2)) #, toggle_labels, toggle_edges))

### check out this next
# https://docs.bokeh.org/en/latest/docs/user_guide/interaction/callbacks.html#userguide-interaction-jscallbacks
# linking plot with datatable http://www.snowpacktracker.com/btac/event-radial-plot
# https://discourse.bokeh.org/t/unselect-individual-glyph-using-taptool/2759/8 --> this is what I need
# https://docs.bokeh.org/en/latest/docs/user_guide/interaction/callbacks.html
# https://discourse.bokeh.org/t/callback-on-taptool-unselect/5237
# https://discourse.bokeh.org/t/unselect-individual-glyph-using-taptool/2759/9