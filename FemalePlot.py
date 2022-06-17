import pandas as pd
import numpy as np
import bokeh

from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, Slider, Select, Panel
from bokeh.layouts import widgetbox, row, gridplot

def femaleplot_tab(data):
    #Setting the data
    data.set_index('Year', inplace = True)
    data.rename({'Country Name': 'Country'}, axis=1, inplace=True)
    country_list = data['Country'].unique().tolist()
    
    x = np.arange(0,len(data.loc[1970].Country))
    
    #ColumnDataSource
    source = ColumnDataSource(data={
        'x': x,
        'y': data.loc[1970].Count,
        'country': data.loc[1970].Country,})
    
    #Making Plot
    plot = figure(x_range=(0,100), title='Female Population Percentage for 1970', 
                  x_axis_label='Country', y_axis_label='Female Perc',
                  plot_height=400, plot_width=700)
    
    hover = HoverTool(tooltips=[('Country','@country'),('Value','@y')])
    plot.add_tools(hover)

    # Add a circle glyph
    plot.circle(x='x', y='y', source=source, size=10, color="firebrick", alpha=0.5)
    
    def update_plot(attr, old, new):
        yr = slider.value
        x = np.arange(0,len(data.loc[yr].Country))

        new_data = {'x': x,
                    'y': data.loc[yr].Count,
                    'country': data.loc[yr].Country,}
        source.data = new_data
   
        plot.title.text = 'Female Population Percentage for %d' % yr

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
    
    slider = Slider(start=1960, end=2017, step=1, value=1960, title='Year')
    slider.on_change('value',update_plot)
    plot = style(plot)
    layout = row(widgetbox(slider), plot)
    tab = Panel(child=layout, title = 'Female Percentage Plot')
    
    return tab