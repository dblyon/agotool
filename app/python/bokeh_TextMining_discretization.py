''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np
import math
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure

# Set up data
num_data_points_to_plot = 200

num_genes = 100
alpha = 0.5
beta = 3 # ?
score = 3.0

def generate_data_points_x(num_data_points_to_plot):
    return np.linspace(0, 5, num_data_points_to_plot)

def calculate_y_from_x(x, num_genes, alpha, beta):
    y = []
    for score_temp in x:
        y.append(math.pow(num_genes, math.pow(alpha * (1 - score_temp / 5), (1 - alpha))) <= beta)
    y = np.array(y)
    return y

x = generate_data_points_x(num_data_points_to_plot)
y = calculate_y_from_x(x, num_genes, alpha, beta)
source = ColumnDataSource(data=dict(x=x, y=y))

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="Text mining score discretization",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 5], y_range=[0, 1])
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.8)

# Set up widgets
num_genes_slider = Slider(title="num_genes", value=100, start=0, end=5000, step=1)
alpha_slider = Slider(title="alpha", value=0.5, start=0, end=1, step=0.1)
beta_slider = Slider(title="beta", value=3, start=0, end=5, step=0.1)
text = TextInput(title="Parameters", value='num_genes: {}, alpha: {}, beta: {}'.format(num_genes, alpha, beta))

# Set up callbacks
def update_title(attrname, old, new):
    plot.title.text = text.value

text.on_change('value', update_title)

def update_data(attrname, old, new):
    # Get the current slider values
    num_genes = num_genes_slider.value
    alpha = alpha_slider.value
    beta = beta_slider.value
    # Generate the new curve
    x = generate_data_points_x(num_data_points_to_plot)
    y = calculate_y_from_x(x, num_genes, alpha, beta)
    source.data = dict(x=x, y=y)

# for w in [offset, amplitude, phase, freq]:
for w in [text, num_genes_slider, alpha_slider, beta_slider]:
    w.on_change('value', update_data)

# Set up layouts and add to document
# inputs = column(text, offset, amplitude, phase, freq)
inputs = column(text, num_genes_slider, alpha_slider, beta_slider)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"
