from flask import Flask, render_template, request
from local_date_stamp import main
from weather import get_current_weather, get_forecast
from antarctica_research_stations import stations_list

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    date = main()
    current_weather = None
    if request.method == 'POST':
        location_name = request.form['location-name']
        current_weather = get_current_weather(location_name)

        if current_weather.location == '':
            location_name = request.form['location-name']

        forecast = get_forecast(location_name)
            
    else:
        location_name = 'Edinburgh' # Default location
        current_weather = get_current_weather(location_name)
        forecast = get_forecast(location_name)


    return render_template('index.html', date=date, current_weather=current_weather, location_name=location_name, forecast=forecast, stations=stations_list)
