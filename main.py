from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

DATA_FOLDER = "data_small"

stations_df = pd.read_csv(f'{os.path.dirname(__file__)}/data/stations.txt', skiprows=17)
stations_df = stations_df[['STAID', 'STANAME                                 ']]


@app.route("/")
def home():
    return render_template("home.html", data=stations_df.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = f"{os.path.dirname(__file__)}/{DATA_FOLDER}/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    row = df.loc[df['    DATE'] == date]
    temperature = row['   TG'].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}


@app.route("/api/v1/<station>")
def all_data(station):
    filename = f"{os.path.dirname(__file__)}/{DATA_FOLDER}/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient="records")
    return result


@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = f"{os.path.dirname(__file__)}/{DATA_FOLDER}/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE'] = df["    DATE"].astype(str)
    result = df.loc[df['    DATE'].str.startswith(year)].to_dict(orient="records")
    return result


if __name__ == "__main__":
    app.run(debug=True, port=5001)
