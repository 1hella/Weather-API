from glob import glob
import sqlite3
import pandas as pd


def populate_database():
    connection = sqlite3.connect("data.db")

    filenames = glob("data_small/TG_STAID*.txt")

    for filename in filenames:
        df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
        df.rename(columns={" SOUID": "souid", "STAID": "staid", "    DATE": "date", "   TG": "tg", " Q_TG": "q_tg"},
                  inplace=True)
        df['date'] = df['date'].astype(str)
        print("populating", filename)
        try:
            df.to_sql("temperatures", con=connection, if_exists="append", index=False)
        except sqlite3.IntegrityError as e:
            print(e)
