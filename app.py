import dash
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objs as go

weather = pd.read_csv('road-weather-information-stations.csv')

weather_group = weather.groupby('StationName').RecordId.count()
weather_group = pd.DataFrame(weather_group)

weather_pivot = pd.pivot_table(weather, index='StationName', values=['RoadSurfaceTemperature','AirTemperature'], aggfunc='sum')

weather_air_mean = weather['AirTemperature'].mean()
weather_air_mean_above = weather[weather.AirTemperature > weather_air_mean][['StationName','AirTemperature']]
weather_air_mean_below = weather[weather.AirTemperature < weather_air_mean][['StationName','AirTemperature']]

weather_road_mean = weather['RoadSurfaceTemperature'].mean()
weather_road_mean_above = weather[weather.RoadSurfaceTemperature > weather_road_mean][['StationName','RoadSurfaceTemperature']]
weather_road_mean_below = weather[weather.RoadSurfaceTemperature < weather_road_mean][['StationName','RoadSurfaceTemperature']]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Road Weather Information Stations'),

    html.Div(children='''
        A few weather stations recorded air temperature and road surface temperature over a period of time.
        In this dashboard, the data recorded from the different weather stations is compared against each 
        other according to station.
    '''),

    html.Div(children='''
        We will start by displaying the sum of all temperatures recorded for air and road surface per station.
    '''),

    dcc.Graph(
        id='total-temperature-per-station',
        figure={
            'data': [
                {'x': weather_pivot.index, 'y': weather_pivot['AirTemperature'], 'type': 'scatter', 'name': 'Air Temperature'},
                {'x': weather_pivot.index, 'y': weather_pivot['RoadSurfaceTemperature'], 'type': 'scatter', 'name': u'Road Surface Temperature'},
            ],
            'layout': {
                'title': 'Total Number of Air and Road Surface Temperature per Station',
            }
        }
    ),

    html.Div(children='''
        Next we look at the total number of records each station gathered in the data provided.
    '''),

    dcc.Graph(
        id='total-count-report-per-station',
        figure={
            'data': [
                {'x': weather_group.index, 'y': weather_group['RecordId'], 'type': 'scatter', 'name': 'Total Count'},
            ],
            'layout': {
                'title': 'Total Count of Weather Reports per Station',
            }
        }
    ),

    html.Div(children=f'''
        By calculating the mean average for air ({weather_air_mean}) and road surface temperature 
        ({weather_road_mean}) seperately. A comparison for the temperature that is above the air 
        temperature mean average along with the temperature that is above the road surface temperature 
        mean average.
    '''),

    dcc.Graph(
        id='temperature-above-mean',
        figure={
            'data': [
                {'x': weather_air_mean_above['StationName'], 'y': weather_air_mean_above['AirTemperature'], 'type': 'bar', 'name': 'Air Temperature Above Mean'},
                {'x': weather_road_mean_above['StationName'], 'y': weather_road_mean_above['RoadSurfaceTemperature'], 'type': 'bar', 'name': 'Road Surface Temperature Above Mean'},
            ],
            'layout': {
                'title': 'Temperature Above Mean',
            }
        }
    ),

    html.Div(children=f'''
        A comparison for the temperature that is below the air temperature mean average along with 
        the temperature that is below the road surface temperature mean average.
    '''),

    dcc.Graph(
        id='temperature-below-mean',
        figure={
            'data': [
                {'x': weather_air_mean_below['StationName'], 'y': weather_air_mean_below['AirTemperature'], 'type': 'bar', 'name': 'Air Temperature Below Mean'},
                {'x': weather_road_mean_below['StationName'], 'y': weather_road_mean_below['RoadSurfaceTemperature'], 'type': 'bar', 'name': 'Road Surface Temperature Below Mean'},
            ],
            'layout': {
                'title': 'Temperature Below Mean',
            }
        }
    )

])


if __name__ == '__main__':
    app.run_server(debug=True)