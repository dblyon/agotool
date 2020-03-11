import numpy as np
import pandas as pd
import matplotlib
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
import bokeh.sampledata
from bokeh.plotting import figure, output_file, show
from bokeh.models import Legend
from bokeh.io import output_notebook
from bokeh.models import HoverTool, BoxZoomTool, ResetTool, LassoSelectTool, WheelZoomTool, PanTool, SaveTool, TapTool
from bokeh.plotting import figure, show
from bokeh.models.sources import ColumnDataSource
from bokeh.models import CustomJS, LabelSet, TapTool
from bokeh.io import export_png
from flask import Flask, render_template
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop
from bokeh.palettes import Spectral
from bokeh import palettes

# from https://docs.bokeh.org/en/latest/docs/reference/palettes.html
# and http://colorbrewer2.org/#type=qualitative&scheme=Dark2&n=4
# Category20 from 3 - 20 but use only for 13 and 14
# or Category10 from 3 - 10

palette_dict = {}
palette_dict[1] = ['#d95f02']
palette_dict[2] = ['#1b9e77','#d95f02']
palette_dict[3] = palettes.d3['Category10'][3] # ['#1b9e77','#d95f02','#7570b3']
palette_dict[4] = palettes.d3['Category10'][4] # ['#e41a1c','#377eb8','#4daf4a','#984ea3'] # ['#1b9e77','#d95f02','#7570b3','#e7298a']
palette_dict[5] = palettes.d3['Category10'][5] # ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e']
palette_dict[6] = palettes.d3['Category10'][6] # ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02']
palette_dict[7] = palettes.d3['Category10'][7] # ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d']
palette_dict[8] = palettes.d3['Category10'][8] # ['#1b9e77','#d95f02','#7570b3','#e7298a','#66a61e','#e6ab02','#a6761d','#666666']
palette_dict[9] = palettes.d3['Category10'][9] # ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf','#999999']
palette_dict[10] = palettes.d3['Category10'][10] # ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a']
palette_dict[11] = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99']
palette_dict[12] = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c','#fdbf6f','#ff7f00','#cab2d6','#6a3d9a','#ffff99','#b15928']
palette_dict[13] = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2'] # palettes.d3['Category20'][13]
palette_dict[14] = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2'] # palettes.d3['Category20'][14]


app = Flask(__name__)


def modify_doc(doc):
    # df = sea_surface_temperature.copy()
    # source = ColumnDataSource(data=df)
    #
    # plot = figure(x_axis_type='datetime', y_range=(0, 25), y_axis_label='Temperature (Celsius)',
    #               title="Sea Surface Temperature at 43.18, -70.43")
    # plot.line('time', 'temperature', source=source)
    fn_example = r"/Users/dblyon/modules/cpr/agotool/data/exampledata/DF_Bokeh_example_for_plotting_playground.txt"
    df = pd.read_csv(fn_example, sep="\t")
    points = ColumnDataSource(data=df)

    ### Hover
    hover = HoverTool(tooltips=[("term", "@term"), ("desc", "@description"), ("FG count", "@FG_count")])
    p = figure(plot_width=1000, plot_height=500,
               title = " ",
               toolbar_sticky=False,
               toolbar_location='above',
               tools=[hover, BoxZoomTool(), WheelZoomTool(), ResetTool(), PanTool(), SaveTool()]) # , TapTool(), LassoSelectTool()
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

    legend_it = []
    for name, group in df.groupby("etype"):
        color_of_etype = group.iloc[0].color
        plot_ = p.circle(x="logFDR", y="effectSize", source=group,
                         size="FG_count_2_circle_size", fill_alpha="rank_2_transparency",
                         color="color",
                         muted_color="color", muted_alpha=0.2,
                           nonselection_fill_alpha=0.2,
                           nonselection_line_alpha=1.0,
                           nonselection_fill_color=color_of_etype,
                           nonselection_line_color=color_of_etype,
                         selection_color=color_of_etype)
        name = group.iloc[0].category
        legend_it.append((name, [plot_]))

        labels = ColumnDataSource(data=dict(x=[], y=[], t=[], ind=[]))
        p.add_layout(LabelSet(x='x', y='y', text='t', y_offset=7, x_offset=7, source=labels, text_font_size="8pt"))

    legend = Legend(items=legend_it, location=(10, 0))
    legend.click_policy = "mute"
    p.add_layout(legend, 'right')

    plot_ = p.circle(x='logFDR', y='effectSize', source=points, size="FG_count_2_circle_size", alpha=0.0, color=None)

    def callback(attr, old, new):
        if new == 0:
            data = df
        else:
            #data = df.rolling('{0}D'.format(new)).mean()
            data = df[df["rank"] <= new]
        source.data = ColumnDataSource(data=data).data

    slider = Slider(start=0, end=100, value=5, step=1, title="top n ranks per category")
    slider.on_change('value', callback)

    doc.add_root(column(slider, plot))

    doc.theme = Theme(filename="theme.yaml")


@app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return render_template("embed.html", script=script, template="Flask")


def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    server = Server({'/bkapp': modify_doc}, io_loop=IOLoop(), allow_websocket_origin=["localhost:8000"])
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    print('Opening single process Flask app with embedded Bokeh application on http://localhost:8000/')
    print()
    print('Multiple connections may block the Bokeh app in this configuration!')
    print('See "flask_gunicorn_embed.py" for one way to run multi-process')
    app.run(port=8000)





# code_2_add_term_label_on_click = """
# const data = labels.data
# for (i=0; i<points.selected.indices.length; i++) {
#     const ind = points.selected.indices[i]
#     data.x.push(points.data.logFDR[ind])
#     data.y.push(points.data.effectSize[ind])
#     data.t.push(points.data.term[ind])
#     data.ind.push(ind)
# }
# labels.change.emit()
# """
#
# callback=CustomJS(args=dict(points=points, labels=labels), code=code_2_add_term_label_on_click)
# p.add_tools(TapTool(callback=callback), LassoSelectTool(callback=callback))
#
#
# show(p)
