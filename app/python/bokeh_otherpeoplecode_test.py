from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models.tools import LassoSelectTool, TapTool
from bokeh.models.widgets.buttons import Button
from bokeh.models.callbacks import CustomJS

# source = ColumnDataSource(dict(
#     x=[1, 2, 3, 4, 5, 6],
#     y=[1, 2, 3, 4, 5, 6],
# ))

fn_example = os.path.join(os.path.expanduser("~"), "modules/cpr/agotool/data/exampledata/DF_Bokeh_example_for_plotting_playground.txt")
df = pd.read_csv(fn_example, sep="\t")
df = df[df["etype"] != -20].reset_index(drop=True)
source = ColumnDataSource(data=df)

p = figure(
    plot_height=300,
    tools='',)

p.circle( x='x', y='y', size=20, source=source)

lasso_select = LassoSelectTool(
    select_every_mousemove=False,)
tap = TapTool()
tools = (lasso_select, tap)
p.add_tools(*tools)

def update_selection_programmatically():
    # source.selected.update(indices=[4])           # indices is updated but the update event (source.change.emit();) is not triggered
    source.selected.update(indices=[])           # indices is updated but the update event (source.change.emit();) is not triggered
                                                  # the figure is not repainted and the points are not marked as selected
bt = Button(
    label="Update Selection DBL",
    button_type="success",
    width=50
)

bt.on_click(update_selection_programmatically)

# this works fine

bt.callback = CustomJS(
    args=dict(source=source),
    code="""
        source.selected.indices = [4];
        source.change.emit();
    """
)

def update_selection(attr, old, new):
    print('>> NEW SELECTION: {}'.format(new.indices))
    # new.indices = [0]       # this works fine here

source.on_change('selected', update_selection)

curdoc().add_root(column([p, bt]))






