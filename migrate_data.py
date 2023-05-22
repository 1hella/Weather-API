from glob import glob
import sqlite3
import pandas as pd

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
try:
    cursor.execute("""
    CREATE TABLE "temperatures" (
        "staid"	INTEGER,
        "souid"	INTEGER,
        "date"	TEXT,
        "tg"	INTEGER,
        "q_tg"	INTEGER,
        CONSTRAINT primary_key PRIMARY KEY (staid, date)
    )""")
    connection.commit()
except sqlite3.OperationalError as e:
    print(e)

filenames = glob("data_small/TG_STAID*.txt")

for filename in filenames:
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    df.rename(columns={" SOUID": "souid", "STAID": "staid", "    DATE": "date", "   TG": "tg", " Q_TG": "q_tg"},
              inplace=True)
    print(filename)
    try:
        df.to_sql("temperatures", con=connection, if_exists="append", index=False)
    except sqlite3.IntegrityError as e:
        print(e)
