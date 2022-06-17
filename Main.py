#All Rights Reserved ® Muhammad Kiko Reiki, Deviya Yuliani, Siti Inayah Putri

import pandas as pd

import bokeh
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from os.path import dirname, join

from LinePlot import lineplot_tab 
from Table import table_tab
from FemalePlot import femaleplot_tab

world_population = pd.read_csv('archive/WorldPopulation.csv')
femaleperc = pd.read_csv('archive/population_female_percentage_long.csv')

tab1 = lineplot_tab(world_population)
tab2 = femaleplot_tab(femaleperc)
tab3 = table_tab(world_population)
tabs = Tabs(tabs = [tab1, tab2, tab3])

curdoc().add_root(tabs)