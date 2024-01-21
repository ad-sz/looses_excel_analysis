"""create chart showing looses in % by weeks"""

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from bokeh.plotting import figure, output_file, save
from plotly.tools import mpl_to_plotly
import plotly.offline as py_offline
import plotly.io as pio
import mpld3
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def looses_weeks(df_dane_losses):
    #coppy df_dane_losses to df_dane_losses_week
    df_dane_losses_week = df_dane_losses[:]
    #change date for week number
    df_dane_losses_week.iloc[:, 11] = df_dane_losses_week.iloc[:, 11].apply(lambda x: x.strftime('%W'))

    #grouping data by week number and sum of looses in kg for weeks numbers, remove axis name
    df_dane_losses_week_losses_sum = df_dane_losses_week.groupby(df_dane_losses_week.columns[11])[df_dane_losses_week.columns[3]].sum().rename_axis(None)
    #remove series name
    df_dane_losses_week_losses_sum.name = None

    #grouping data by week number and sum of inserts in kg for weeks numbers, remove axis name
    df_dane_losses_week_insert_sum = df_dane_losses_week.groupby(df_dane_losses_week.columns[11])[df_dane_losses_week.columns[1]].sum().rename_axis(None)
    #remove series name
    df_dane_losses_week_insert_sum.name = None

    #connecting both DataFrame obiects (df_dane_losses_week_losses_sum, df_dane_losses_week_insert_sum) in one
    df_combined_week_looses_insert = pd.concat([df_dane_losses_week_losses_sum, df_dane_losses_week_insert_sum], axis=1)

    #adding new column to df_combined_week_looses_insert with % of looses
    df_combined_week_looses_insert[2] = df_combined_week_looses_insert.apply(lambda row: (row[0] / row[1]) * 100 if row[1] != 0 else 0, axis=1)

    #create chart with two y axis
    #create a subplot with two y axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    #create chart for % of losses
    fig.add_trace(
        go.Scatter(x=df_combined_week_looses_insert.index, y=df_combined_week_looses_insert.iloc[:, 2], 
                mode='markers+lines', name='% of losses', marker=dict(color='blue', size=10), hovertemplate='%{y:.1f}'),
        secondary_y=False,
    )

    #create secondary chart for kg of losses
    fig.add_trace(
        go.Scatter(x=df_combined_week_looses_insert.index, y=df_combined_week_looses_insert.iloc[:, 0], 
                mode='markers', name='kg of losses', marker=dict(color='red', symbol='x', size=12), hovertemplate='%{y:.0f}'),
        secondary_y=True,
    )

    #adding labels
    fig.update_layout(
        title_text='losses by weeks',
        xaxis_title='week',
        yaxis_title='% of losses',
        yaxis2_title='kg of losses',
    )

    #setting y(primary) axis range and ticks
    fig.update_yaxes(range=[0, 10], tickvals=np.arange(0, 10.5, 1), secondary_y=False)

    #setting y(secondary) axis properties
    fig.update_yaxes(tickcolor='red', secondary_y=True)

    #saving chart in HTML format
    fig.write_html("D:/python_data/losses/looses_by_week.html")