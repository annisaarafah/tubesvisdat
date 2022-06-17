#!/usr/bin/env python
# coding: utf-8

# # Import Library

# In[1]:


import pandas as pd


# In[2]:


from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, HoverTool, Select
from bokeh.models.widgets import Tabs, Panel
from bokeh.layouts import row, widgetbox


# # Data Preparation

# In[3]:


data = pd.read_csv("Covid19_dataset.csv",parse_dates=['date'])


# In[4]:


data.info()


# In[5]:


df = data[['continent','location','date','total_cases','new_cases','total_deaths','new_deaths']]
df


# In[6]:


#df.isnull().sum()


# In[7]:


df['total_cases'].fillna(0,inplace=True)
df['new_cases'].fillna(0,inplace=True)
df['total_deaths'].fillna(0,inplace=True)
df['new_deaths'].fillna(0,inplace=True)


# In[8]:


df.isnull().sum()


# In[9]:


#Mengambil data negara Asia
df_asia = df[df['continent'] == 'Asia']


# In[10]:


df_asia['location'].unique()


# In[11]:


df_asia.drop(columns='continent',inplace=True)


# In[12]:


df_indo = df_asia[df_asia['location'] == 'Indonesia']


# In[13]:


df_indo


# # BOKEH

# In[14]:


#Membuat data untuk source awal plottingan
df_select = df_asia[df_asia['location'] == 'Indonesia']
df_select2 = df_asia[df_asia['location'] == 'Malaysia']


# In[15]:


#Membuat source data untuk plotting data
source1 = ColumnDataSource(data={
    'x' : df_select['date'],
    'y' : df_select['new_cases'],
    
})
source2 = ColumnDataSource(data={
    'x' : df_select2['date'],
    'y' : df_select2['new_cases'],
})


# In[16]:


#Mengatur Figure gambar
fig_gambar = figure(title='Data Covid-19 di Asia',
                   plot_height=550, plot_width=1000,
                   x_axis_type = 'datetime',
                   x_axis_label='Date', y_axis_label='Jumlah Orang',
                   tools=['pan', 'wheel_zoom', 'save', 'reset'])

#Negara 1
fig_gambar.line(x='x', y='y',
              color='coral',
              line_width=2,
              source=source1,
              legend_label ='Negara 1')

#Negara 2
fig_gambar.line(x='x', y='y',
              color='cornflowerblue',
              line_width=2,
              source=source2,
              legend_label = 'Negara 2')

#Lokasi & Fitur Legend
fig_gambar.legend.location = 'top_left'
fig_gambar.legend.click_policy = 'mute'

#Menambahkan Hover
fig_gambar.add_tools(HoverTool(tooltips=[
                                ('Date','@x{%F}'),
                                ('new_cases', '@y')
                               ],formatters={'@x': 'datetime'},
                               mode='vline'))


# In[17]:


def update_plot(attr, old, new):
    #Mengambil pilihan data Negara
    pilihan1 = select1.value
    pilihan3 = select3.value
    
    #Mengambil pilihan Negara
    pilihan0 = select0.value
    pilihan2 = select2.value
    
    #Membuat data berdasarkan pilihan negara
    df_select = df_asia[df_asia['location'] == pilihan0]
    df_select2 = df_asia[df_asia['location'] == pilihan2]
    
    #Membuat data baru berdasarkan pilihan
    new_source1 = {
        'x' : df_select['date'],
        'y' : df_select[pilihan1]
    }
    new_source2 = {
        'x' : df_select2['date'],
        'y' : df_select2[pilihan3]
    }
    
    #Memasukan data baru ke source plot
    source1.data = new_source1
    source2.data = new_source2


# In[18]:


def updateNegara_plot(attr, old, new):
    #Mengambil pilihan data Negara
    pilihan0 = select0.value
    pilihan2 = select2.value

    #Membuat data berdasarkan pilihan negara
    df_select = df_asia[df_asia['location'] == pilihan0]
    df_select2 = df_asia[df_asia['location'] == pilihan2]
    
    #Membuat data baru berdasarkan pilihan
    new_source1 = {
        'x' : df_select['date'],
        'y' : df_select['new_cases']
    }
    new_source2 = {
        'x' : df_select2['date'],
        'y' : df_select2['new_cases']
    }
    
    #Memasukan data baru ke source plot
    source1.data = new_source1
    source2.data = new_source2


# In[19]:


#Pilihan pada Select berupa List Seluruh Negara
#Membuat pilihan Negara
option0 = df_asia['location'].unique().tolist()

#Membuat pilihan data Negara
option1 = df_indo.columns.to_list()
del option1[0]
del option1[0]

##Menu pilihan Negara 1
#Select0 untuk memilih Negara 1
select0 = Select(
    options = option0,
    title = 'Pilih Negara 1',
    value = 'Indonesia'
)

#Select1 untuk memilih data Negara 1
select1 = Select(
    options = option1,
    title = 'Pilih Data Negara 1',
    value = 'new_cases'
)

##Menu pilihan Negara 2
#Select2 untuk memilih Negara 2
select2 = Select(
    options = option0,
    title = 'Pilih Negara 2',
    value = 'Malaysia'
)

#Select3 untuk memilih data Negara 2
select3 = Select(
    options = option1,
    title = 'Pilih Data Negara 2',
    value = 'new_cases'
) 

#Jika select dipilih
select0.on_change('value', updateNegara_plot)
select1.on_change('value', update_plot)
select2.on_change('value', updateNegara_plot)
select3.on_change('value', update_plot)


# In[20]:


#Membuat layout gambar
layout = row(widgetbox(select0,select1,select2,select3), fig_gambar)

#Membuat Panel gambar
panel1 = Panel(child=layout, title='Visualisasi Perbandingan Data Covid-19')

#Membuat Tabel dengan Panel yang ada
tabs = Tabs(tabs=[panel1,])

curdoc().add_root(tabs)

