import pandas as pd
import bokeh

from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, RangeSlider, Select, Panel
from bokeh.layouts import widgetbox, row, gridplot

def lineplot_tab(data):
    #Setting source
    source = ColumnDataSource(data={
        'x': data['Year'],
        'y': data['Population']})

    #Making line plot
    plot = figure(x_range=(1951,2020), title = 'Population per Year', 
                  x_axis_label = 'Year', y_axis_label = 'Population',plot_height=700,
                  plot_width=700)
    
    hover = HoverTool(tooltips=[('Value','@y')])
    plot.add_tools(hover)

    plot.line(x='x', y='y', source=source, line_width=3, color='firebrick')
    plot.circle(x='x', y='y', source=source, fill_color="white", line_color="firebrick", size=5)

    #Define Update function
    def update_plot(attr, old, new):
        x = x_select.value
        y = y_select.value

        plot.xaxis.axis_label = x
        plot.yaxis.axis_label = y

        new_data = {
        'x': data[x],
        'y': data[y]}
    
        source.data = new_data

        plot.title.text = '%s per Year' % y
        
    def style(p):
        p.title.align = 'center'
        p.title.text_font_size = '20pt'
        p.title.text_font = 'sans-serif'
        
        p.xaxis.axis_label_text_font_size = '14pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '14pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p
    
    # Make a dropdown select
    x_select = Select(
        options=['Year'],
        value='Year',
        title='X Axis')
    x_select.on_change('value', update_plot)

    y_select = Select(
        options=['Population', 'NetChange', 'Urban'],
        value='Population',
        title='Y Axis')
    y_select.on_change('value', update_plot)
    
    range_slider = RangeSlider(title = "Year Range",start = 1951, end = 2020, step = 1,
                               value = (plot.x_range.start, plot.x_range.end))
    range_slider.js_link("value", plot.x_range, "start", attr_selector=0)
    range_slider.js_link("value", plot.x_range, "end", attr_selector=1)
    
    plot = style(plot)

    layout = row(widgetbox(x_select, y_select, range_slider), plot)
    tab = Panel(child=layout, title = 'World Population Plot')
    
    return tab
    
    
    