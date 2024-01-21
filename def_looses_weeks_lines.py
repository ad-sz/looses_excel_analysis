"""create chart showing looses in % by weeks for each line"""

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

def looses_weeks_lines(df_dane_losses):
    #coppy df_dane_losses to df_dane_losses_week
    df_dane_losses_week = df_dane_losses[:]
    #change date for week number
    df_dane_losses_week.iloc[:, 11] = df_dane_losses_week.iloc[:, 11].apply(lambda x: x.strftime('%W'))

    #grouping data by week number, line number and sum of looses in kg for weeks numbers, remove axis name
    df_dane_losses_week_losses_sum = df_dane_losses_week.groupby([df_dane_losses_week.columns[11], df_dane_losses_week.columns[9]])[df_dane_losses_week.columns[3]].sum().reset_index()
    #remove series name
    df_dane_losses_week_losses_sum.name = None

    #grouping data by week number, line number and sum of inserts in kg for weeks numbers, remove axis name
    df_dane_losses_week_insert_sum = df_dane_losses_week.groupby([df_dane_losses_week.columns[11], df_dane_losses_week.columns[9]])[df_dane_losses_week.columns[1]].sum().reset_index()
    #remove series name
    df_dane_losses_week_insert_sum.name = None

    #connecting both DataFrame obiects (df_dane_losses_week_losses_sum, df_dane_losses_week_insert_sum) in one
    df_combined_week_looses_insert = pd.merge(df_dane_losses_week_losses_sum, df_dane_losses_week_insert_sum, on=[df_dane_losses_week_losses_sum.columns[0], df_dane_losses_week_losses_sum.columns[1]])

    #adding new column to df_combined_week_looses_insert with % of looses
    df_combined_week_looses_insert[4] = df_combined_week_looses_insert.apply(lambda row: (row[2] / row[3]) * 100 if row[2] != 0 else 0, axis=1)

    #create DataFrame with % of looses by lines
    df_combined_week_looses_insert_line = df_combined_week_looses_insert.pivot(index=df_combined_week_looses_insert.columns[0], columns=df_combined_week_looses_insert.columns[1], values=df_combined_week_looses_insert.columns[4])

    #remove names of columns
    df_combined_week_looses_insert_line.index.name = None
    df_combined_week_looses_insert_line.columns.name = None

    #create chart with two y axis
    #create a subplot with two y axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    #create chart for % of losses for each line
    #create chart for % of losses for line 1
    fig.add_trace(
        go.Scatter(x=df_combined_week_looses_insert_line.index, y=df_combined_week_looses_insert_line.iloc[:, 0], 
                mode='markers+lines', name='% line 1', marker=dict(color='blue', size=10), hovertemplate='%{y:.1f}'),
        secondary_y=False,
    )
    #create chart for % of losses for line 2
    fig.add_trace(
        go.Scatter(x=df_combined_week_looses_insert_line.index, y=df_combined_week_looses_insert_line.iloc[:, 1], 
                mode='markers+lines', name='% line 2', marker=dict(color='green', size=10), hovertemplate='%{y:.1f}'),
        secondary_y=False,
    )
    #create chart for % of losses for line 3
    fig.add_trace(
        go.Scatter(x=df_combined_week_looses_insert_line.index, y=df_combined_week_looses_insert_line.iloc[:, 2], 
                mode='markers+lines', name='% line 3', marker=dict(color='red', size=10), hovertemplate='%{y:.1f}'),
        secondary_y=False,
    )
    #create chart for % of losses for line 4
    fig.add_trace(
        go.Scatter(x=df_combined_week_looses_insert_line.index, y=df_combined_week_looses_insert_line.iloc[:, 3], 
                mode='markers+lines', name='% line 4', marker=dict(color='cyan', size=10), hovertemplate='%{y:.1f}'),
        secondary_y=False,
    )
    #create chart for % of losses for line 5
    fig.add_trace(
        go.Scatter(x=df_combined_week_looses_insert_line.index, y=df_combined_week_looses_insert_line.iloc[:, 4], 
                mode='markers+lines', name='% line 5', marker=dict(color='magenta', size=10), hovertemplate='%{y:.1f}'),
        secondary_y=False,
    )
    #create chart for % of losses for line 6
    fig.add_trace(
        go.Scatter(x=df_combined_week_looses_insert_line.index, y=df_combined_week_looses_insert_line.iloc[:, 5], 
                mode='markers+lines', name='% line 6', marker=dict(color='brown', size=10), hovertemplate='%{y:.1f}'),
        secondary_y=False,
    )

    #create DataFrame with kg of looses by lines
    df_combined_week_looses_insert_line_kg = df_combined_week_looses_insert.pivot(index=df_combined_week_looses_insert.columns[0], columns=df_combined_week_looses_insert.columns[1], values=df_combined_week_looses_insert.columns[2])
    #remove names of columns
    df_combined_week_looses_insert_line_kg.index.name = None
    df_combined_week_looses_insert_line_kg.columns.name = None

    #create secondary chart - showing max value of kg of looses by week
    #calculate which column (line number) have max value for each line
    max_value_collumn = df_combined_week_looses_insert_line_kg.idxmax(axis=1)
    fig.add_trace(
        go.Scatter(x=df_combined_week_looses_insert_line_kg.index, y=df_combined_week_looses_insert_line_kg.max(axis=1), 
                mode='markers', name='max kg of looses', marker=dict(color='blue', symbol='x', size=12), hovertemplate='%{y:.0f}<br>line ' + max_value_collumn),
        secondary_y=True,
    )

    #adding labels
    fig.update_layout(
        title_text='losses by weeks for lines',
        xaxis_title='week',
        yaxis_title='% of losses',
        yaxis2_title='kg of losses',
    )

    #setting y(primary) axis range and ticks
    fig.update_yaxes(range=[0, 30], tickvals=np.arange(0, 30.5, 1), secondary_y=False)

    #setting y(secondary) axis properties
    fig.update_yaxes(tickcolor='red', secondary_y=True)

    #saving chart in HTML format
    fig.write_html("D:/python_data/losses/looses_by_week_lines.html")