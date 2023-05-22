import sqlite3
import pandas as pd
from main import DATA_FOLDER
import os

# must create data.db
connection = sqlite3.connect("data.db")

stations_df = pd.read_csv(f'{os.path.dirname(__file__)}/{DATA_FOLDER}/stations.txt', skiprows=17)
stations_df = stations_df[['STAID', 'STANAME                                 ']]
stations_df.rename(columns={"STAID": "staid", "STANAME                                 ": "staname"}, inplace=True)

if DATA_FOLDER == "data_small":
    stations_df = stations_df.loc[stations_df["staid"] <= 100]

stations_df.to_sql('stations', con=connection, index=False, if_exists="replace")
