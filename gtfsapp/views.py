
# Create your views here.
from django.http import JsonResponse
import requests
from google.transit import gtfs_realtime_pb2

API_KEY_511 = "c25a8a9d-34c9-417c-8662-601d8a7b9c62"
API_KEY_OPEN_WEATHER = '2d5bac3df0a74651eee6337d8db1a33b'

ENDPOINT_511 = "http://api.511.org/transit/vehiclepositions?api_key=" + API_KEY_511 + "&agency=RG"
ENDPOINT_OPEN_WEATHER = f"http://api.openweathermap.org/data/2.5/weather?q=Sonoma&appid={API_KEY_OPEN_WEATHER}&units=metric"

def get_vehicle_positions(request):
    response = requests.get(ENDPOINT_511)
    print(response.content)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    
    positions = []
    for entity in feed.entity:
        if entity.HasField('vehicle'):
            positions.append({
                "latitude": entity.vehicle.position.latitude,
                "longitude": entity.vehicle.position.longitude
            })
    return JsonResponse(positions, safe=False)

def get_weather(request):
    response = requests.get(ENDPOINT_OPEN_WEATHER)
    data = response.json()

    # Extract the needed data from the response
    weather_data = {
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'wind_speed': data['wind']['speed'],
        'clouds': data['clouds']['all'],
        'icon': data['weather'][0]['icon']
    }

    return JsonResponse(weather_data)

def get_geojson_data(request):
    target_url = 'https://incidents.fire.ca.gov/umbraco/api/IncidentApi/GeoJsonList?inactive=true'
    

    response = requests.get(target_url)
    

    if response.status_code == 200:

        data = response.json()
        return JsonResponse(data, safe=False)
    else:

        return JsonResponse({'error': 'Failed to fetch GeoJSON data.'}, status=500)
