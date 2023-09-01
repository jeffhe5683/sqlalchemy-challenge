from flask import Flask, jsonify
import pandas as pd
import datetime as dt

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Welcome to homepage!"

data_1_path = 'hawaii_measurements.csv'  
data_2_path='hawaii_stations.csv'
data_3_path='most_active_station.csv'

data_1 = pd.read_csv(data_1_path)
data_2=pd.read_csv(data_2_path)
data_3=pd.read_csv(data_3_path)

@app.route('/api/v1.0/precipitation')
def precipitation():
    prcp_dict = {}
    for index, row in data_1.iterrows():
        prcp_dict[row['date']] = row['prcp']

   
    return jsonify(prcp_dict)

@app.route('/api/v1.0/stations')
def stations():
    stations_dict = {}
    for index, row in data_2.iterrows():
        stations_dict[row['station']] = row['name']

    
    return jsonify(stations_dict)

@app.route('/api/v1.0/tobs')
def tobs():
    tobs_dict = {}
    for index, row in data_3.iterrows():
        tobs_dict[row['date']] = row['temperature']

    
    return jsonify(tobs_dict)

@app.route('/api/v1.0/<start>')
def temp_stats_start(start):
    
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    
    data_3['date'] = pd.to_datetime(data_3['date'])

    new_data = data_3[data_3['date'] >= start_date]

    
    lowest_temp_1 = new_data['temperature'].min()
    highest_temp_1 = new_data['temperature'].max()
    average_temp_1 = new_data['temperature'].mean()

    
    temp_stats_1 = {
        "Lowest Temperature": lowest_temp_1,
        "Highest Temperature": highest_temp_1,
        "Average Temperature": average_temp_1
    }

    
    return jsonify(temp_stats_1)


@app.route('/api/v1.0/<start>/<end>')
def temp_stats_start_end(start, end):
    
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    
    data_3['date'] = pd.to_datetime(data_3['date'])

    
    new_data_1 = data_3[(data_3['date'] >= start_date) & (data_3['date'] <= end_date)]

    # Calculate lowest, highest, and average temperatures
    lowest_temp_2 = new_data_1['temperature'].min()
    highest_temp_2 = new_data_1['temperature'].max()
    average_temp_2 = new_data_1['temperature'].mean()

    
    temp_stats_2 = {
        "Lowest Temperature": lowest_temp_2,
        "Highest Temperature": highest_temp_2,
        "Average Temperature": average_temp_2
    }

    
    return jsonify(temp_stats_2)





if __name__ == '__main__':
    app.run(debug=True)
