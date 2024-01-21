"""Looses analysis - create charts"""
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

import def_looses_weeks
import def_looses_weeks_lines

"""create DataFrame obiect from excel file and prepare data for analysis"""

#path to the excel file with data
filename = "D:/python_data/losses/testy.xlsx"

#upload "dane" sheet from excel file to DatFrame object
#changing colums "MLYN" and "NR.PRODUKCYJNY" on strings (dtype={'MLYN': str, 'NR.PRODUKCYJNY': str})
#remove first row from excel because have not needed informations (skiprows=1)
df_dane = pd.read_excel(filename, sheet_name="dane",dtype={'MLYN': str, 'NR.PRODUKCYJNY': str} ,skiprows=1)

#searching last fulfill element in collumn "NR.PRODUKCYJNY"
last_index = df_dane['NR.PRODUKCYJNY'].last_valid_index()
#cut the DataFrame obiect on last fulfill element
df_dane_cut = df_dane.iloc[:last_index + 1, :36]

#designation columns which are needed
needed_columns_for_losses = [0, 4, 5, 11, 12, 13, 14, 15, 16, 17, 19, 21, 35]
#create DataFrame obiect with collums needed for looses analysis
df_dane_losses = df_dane_cut.iloc[:, needed_columns_for_losses]

#change data type for date in column 11
df_dane_losses.iloc[:, 11] = pd.to_datetime(df_dane_losses.iloc[:, 11])

#adding values from last collumn (value of adding FINES) to column with looses in kg
df_dane_losses.iloc[:, 3] = df_dane_losses.iloc[:, 3] + df_dane_losses.iloc[:, -1].fillna(0)

#setting value of looses for 0 if value is less than 0
df_dane_losses.iloc[:, 3] = df_dane_losses.iloc[:, 3].apply(lambda x: max(x, 0))


"""create chart showing looses in % by weeks"""
def_looses_weeks.looses_weeks(df_dane_losses)

"""create chart showing looses in % by weeks for each line"""
def_looses_weeks_lines.looses_weeks_lines(df_dane_losses)