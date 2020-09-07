import bokeh.plotting
import bokeh.io
import bokeh.layouts
from bokeh.models import CustomJS,TapTool
from bokeh.models import ColumnDataSource
import pandas as pd

bokeh.io.output_file("bar.html")


def get_onClick_filter_callback(source_1):
    return CustomJS(args=dict(source_1=source_1), code=""" 
                    var selected_value = source_1.selected.indices
                    console.log("a column has been selected");
                    console.log("selected_value", selected_value);
                    """)


def get_UnClick_filter_callback(source_1):
    return CustomJS(args=dict(source_1=source_1), code=""" 
                    var selected_value = source_1.selected.indices
                    if (selected_value.length==0){
                        console.log("no column selected");
                        console.log("selected_value", selected_value);
                    }
                    """)


fruit = ['apple', 'orange', 'pear']
data = pd.DataFrame({'x': fruit, 'y': [3, 4, 6]})
source_1 = ColumnDataSource(data)
plot_1 = bokeh.plotting.figure(x_range=fruit)
plot_1.vbar(x='x', top='y', width=.9, source=source_1)

click_cb = get_onClick_filter_callback(source_1)
tap = TapTool(callback=click_cb)
plot_1.add_tools(tap)

layout = bokeh.layouts.layout(plot_1)

unselect = get_UnClick_filter_callback(source_1)
plot_1.js_on_event('tap', unselect)
bokeh.io.show(layout)

### https://discourse.bokeh.org/t/callback-on-taptool-unselect/5237/6