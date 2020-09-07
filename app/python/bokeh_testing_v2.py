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
import bokeh.io
# fn_output =  os.path.join(os.path.expanduser("~"), "modules/cpr/agotool/app/python/bokeh_testing.html")
# output_file(fn_output)
bokeh.io.output_file("bokeh_testing_v2.html")
### run "python bokeh_testing.py" --> creates bokeh_testing.html

# fn_example = os.path.join(os.path.expanduser("~"), "modules/cpr/agotool/data/exampledata/DF_Bokeh_example_for_plotting_playground.txt")
fn_example = os.path.join(os.path.expanduser("~"), "modules/cpr/agotool/data/exampledata/DF_Bokeh_example_for_plotting_playground_small.txt")
df = pd.read_csv(fn_example, sep="\t")
# df = df[df["etype"] != -20].reset_index(drop=True)
# del df["FG_IDs"]
source_1 = ColumnDataSource(data=df)

def get_onClick_filter_callback(source_1):
    return CustomJS(args=dict(source_1=source_1), code=""" 
                    var selected_value = source_1.selected.indices                    
                    console.log("a column has been selected");
                    console.log("selected_value", selected_value);
                    const data = labels.
                    """)

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
# callback = CustomJS(args=dict(points=source, labels=labels), code=code_2_add_term_label_on_click)
# plot.add_tools(TapTool(callback=callback))

def get_UnClick_filter_callback(source_1):
    return CustomJS(args=dict(source_1=source_1), code=""" 
                    var selected_value = source_1.selected.indices
                    if (selected_value.length==0){
                        console.log("no column selected");
                        console.log("selected_value", selected_value);
                    }
                    """)

hover = HoverTool(tooltips=[("term", "@term"), ("desc", "@description"), ("FG count", "@FG_count")])
plot = figure(plot_width=1000, plot_height=500, title = "", toolbar_sticky=False, toolbar_location="above",
           tools=[hover, BoxZoomTool(), ZoomInTool(), ZoomOutTool(), ResetTool(), PanTool(), SaveTool() ]) # , TapTool() ]) # , TapTool(), LassoSelectTool()
plot.title.text_font_size, plot.title.align = "1pt", "center"
plot.xaxis.axis_label, plot.yaxis.axis_label = "-log(corrected p_value)", "effect size"
plot.xaxis.axis_label_text_font_style, plot.yaxis.axis_label_text_font_style = "normal", "normal"
plot.xgrid.grid_line_alpha, plot.ygrid.grid_line_alpha = 0.5, 0.5
plot.xaxis.minor_tick_line_color, plot.yaxis.minor_tick_line_color = None, None

renderer_per_category = plot.circle(x="logFDR", y="effectSize", source=source_1,
        size="FG_count_2_circle_size", fill_alpha="rank_2_transparency",
        color="color", muted_color="color", muted_alpha=0.2,
        # nonselection_fill_alpha="rank_2_transparency", nonselection_line_alpha=1.0,
        nonselection_fill_alpha=0.2, nonselection_line_alpha=1.0,
        nonselection_fill_color="color", nonselection_line_color="color", selection_color="color",
        legend_group="category")

# legend = Legend(location=(250, 0), click_policy="hide") # legend_group="category")
# legend.click_policy = "hide" #"mute"
# plot.add_layout(legend, "right")

labels = LabelSet(x="logFDR", y="effectSize", text="term", x_offset=7, y_offset=7, source=source_1, text_font_size="8pt", visible=False) # render_mode="canvas", level="glyph",
plot.add_layout(labels)


click_cb = get_onClick_filter_callback(source_1)
tap = TapTool(callback=click_cb)
plot.add_tools(tap)

layout = bokeh.layouts.layout(plot)

unselect = get_UnClick_filter_callback(source_1)
plot.js_on_event('tap', unselect)
bokeh.io.show(layout)

### https://discourse.bokeh.org/t/callback-on-taptool-unselect/5237/6