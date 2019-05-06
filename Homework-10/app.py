import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date")

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.\
    Return the JSON representation of your dictionary."""

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], "%Y-%m-%d").date()
    last_date

    one_year_ago = last_date - dt.timedelta(days=365)
    one_year_ago

    result = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    precip_df = pd.DataFrame(result).set_index('date').sort_values('date')

    precip_dict = precip_df['prcp'].to_dict()

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    """
    Return a JSON list of stations from the dataset.
    """

    stations = session.query(Station.station, Station.name, func.count(Measurement.station)).filter(Measurement.station == Station.station).group_by(Station.station).all()

    stations_list = []
    for i in range(len(stations)):
        stations_list.append(list(stations[i]))

    stations_dict = pd.DataFrame(stations_list, columns=["Station", "Name", "Count"]).set_index('Station').to_dict('index')

    return jsonify(stations_dict)


@app.route("/api/v1.0/tobs")
def temperature():
    """query for the dates and temperature observations from a year from the last data point.\
    Return a JSON list of Temperature Observations (tobs) for the previous year."""

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], "%Y-%m-%d").date()

    one_year_ago = last_date - dt.timedelta(days=365)

    result = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).all()

    tobs_df = pd.DataFrame(result).set_index('date').sort_values('date')

    tobs_dict = tobs_df.to_dict('index')

    return jsonify(tobs_dict)


@app.route("/api/v1.0/<start>")
def start_date_only(start):
    """When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for\
     all dates greater than and equal to the start date."""

    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()

    tmin, tavg, tmax = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()[0]

    stats = {"Minimum Temperature": tmin, "Average Temperature": tavg, "Maximum Temperature": tmax}

    return jsonify(stats)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end_dates(start, end):
    """ Return a JSON list of the minimum temperature, the average temperature, \
    and the max temperature for a given start or start-end range."""

    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()

    tmin, tavg, tmax = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()[0]

    stats = {"Minimum Temperature": tmin, "Average Temperature": tavg, "Maximum Temperature": tmax}

    return jsonify(stats)



if __name__ == '__main__':
    app.run(debug=True)
