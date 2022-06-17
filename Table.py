import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable

def table_tab(data):
    source = ColumnDataSource(data)

    columns = [
        TableColumn(field='Year', title='Year'),
        TableColumn(field='Population', title='World Population'),
        TableColumn(field='ChangePerc', title='Yearly Change in Percentage'),
        TableColumn(field='NetChange', title='Total Yearly Change'),
        TableColumn(field='Density', title='Density in P/Km²'),
        TableColumn(field='Urban', title='Urban Population'),
        TableColumn(field='UrbanPerc', title='Urban Population Percentage')
        ]
    
    table = DataTable(source=source, columns=columns, width = 1000)
    tab = Panel(child = table, title = 'World Population Table')
    
    return tab