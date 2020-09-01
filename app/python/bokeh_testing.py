import os, sys
import pandas as pd
import numpy as np
import math
from collections import namedtuple
from itertools import combinations

import query, variables
homedir = os.path.expanduser("~")


from bokeh.plotting import figure, curdoc, output_file, show
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, LassoSelectTool, WheelZoomTool, PanTool, SaveTool, TapTool, Legend
from bokeh.io import output_notebook, export_png, show
output_notebook()

from bokeh.plotting import figure, show
from bokeh.models.sources import ColumnDataSource
from bokeh.models import CustomJS, LabelSet, TapTool



# fn_output =  os.path.join(os.path.expanduser("~"), "modules/cpr/agotool/app/python/bokeh_testing.html")
# output_file(fn_output)
### run "python bokeh_testing.py" --> creates bokeh_testing.html

fn_example = os.path.join(os.path.expanduser("~"), "modules/cpr/agotool/data/exampledata/DF_Bokeh_example_for_plotting_playground.txt")
df = pd.read_csv(fn_example, sep="\t")
df = df[df["etype"] != -20]
points = ColumnDataSource(data=df)

### Hover
hover = HoverTool(tooltips=[("term", "@term"), ("desc", "@description"), ("FG count", "@FG_count")])
p = figure(plot_width=1000, plot_height=500,
           title = "",
           toolbar_sticky=False,
           toolbar_location='above',
           tools=[hover, BoxZoomTool(), WheelZoomTool(), ResetTool(), PanTool(), SaveTool(), LassoSelectTool()]) # , TapTool(), LassoSelectTool()
p.title.text_font_size = "1pt"
p.title.align = "center"
p.xaxis.axis_label = '-log(corrected p_value)'
p.xaxis.axis_label_text_font_style = "normal" # not "italic"
p.yaxis.axis_label_text_font_style = "normal"
p.yaxis.axis_label = 'effect size'
p.xgrid.grid_line_alpha = 0.5
p.ygrid.grid_line_alpha = 0.5
p.xaxis.minor_tick_line_color = None
p.yaxis.minor_tick_line_color = None
# labels = ColumnDataSource(data=dict(x=[], y=[], t=[], ind=[]))

legend_it = []
for category, group in df.groupby("category"):
    color_of_etype = group.iloc[0].color
    plot_ = p.circle(x="logFDR", y="effectSize", source=group,
                     size="FG_count_2_circle_size", fill_alpha="rank_2_transparency",
                     color="color", muted_color="color", muted_alpha=0.2,
                     nonselection_fill_alpha=0.2,
                     nonselection_line_alpha=1.0,
                     nonselection_fill_color=color_of_etype,
                     nonselection_line_color=color_of_etype,
                     selection_color=color_of_etype)
    legend_it.append((category, [plot_]))
    labels = ColumnDataSource(data=dict(x=[], y=[], t=[], ind=[]))
    p.add_layout(LabelSet(x='x', y='y', text='t', y_offset=7, x_offset=7, source=labels, text_font_size="8pt"))

legend = Legend(items=legend_it, location=(10, 0))
legend.click_policy = "hide" #"mute"
p.add_layout(legend, 'right')
plot_ = p.circle(x='logFDR', y='effectSize', source=points, size="FG_count_2_circle_size", alpha=0.0, color=None)

code_2_add_term_label_on_click = """
const data = labels.data;
for (var i = 0; i < points.selected.indices.length; i++) {
    const ind = points.selected.indices[i];
    data.x.push(points.data.logFDR[ind]);
    data.y.push(points.data.effectSize[ind]);
    data.t.push(points.data.term[ind]);
    data.ind.push(ind);
}
labels.change.emit();
"""

callback = CustomJS(args=dict(points=points, labels=labels), code=code_2_add_term_label_on_click)
p.add_tools(TapTool(callback=callback))#, LassoSelectTool(callback=callback))

# show(p)
curdoc().add_root(p)


### check out this next
# https://docs.bokeh.org/en/latest/docs/user_guide/interaction/callbacks.html#userguide-interaction-jscallbacks