from flask import Flask, render_template
import pandas as pd
import sqlite3

from migrate_data import populate_database

app = Flask(__name__)
DATA_FOLDER = "data_small"

connection = sqlite3.connect("data.db")
stations_df = pd.read_sql("SELECT * FROM stations", con=connection)


@app.route("/")
def home():
    return render_template("home.html", data=stations_df.to_html(index=False))


@app.route("/api/v1/<station>/<date>")
def temperature(station, date):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    station = int(station)
    query = f"SELECT tg FROM temperatures WHERE staid=({station}) AND date=('{date}')"
    cursor.execute(query)
    row = cursor.fetchone()
    if row is not None:
        temperature = row[0] / 10
    else:
        temperature = None
    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def all_data(station):
    connection = sqlite3.connect('data.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    station = int(station)
    query = f"SELECT * FROM temperatures WHERE staid=({station})"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [dict(station=row['staid'], date=row["date"], temperature=row["tg"] / 10) for row in rows]


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    connection = sqlite3.connect('data.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    station = int(station)
    query = f"SELECT * FROM temperatures WHERE staid=({station}) AND date LIKE ('{year}-__-__')"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [dict(station=row['staid'], date=row["date"], temperature=row["tg"] / 10) for row in rows]


sample_query = temperature(10, "1992-10-08")
if sample_query['temperature'] is None:
    print("populating database...")
    populate_database()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
