import folium
import openrouteservice as ors
from geopy.geocoders import Nominatim
from geopy import distance
import json

def parse_charger_json():

    # Open the original JSON file and load the data
    with open('./static/vehicle_data/bornes.json', 'r') as f:
        data = json.load(f)

    # Extract 'lon' and 'lat' fields from each JSON object that has a 'geo_point_borne' field
    parsed_data = []
    for item in data:
        if 'geo_point_borne' in item and item['geo_point_borne']:
            parsed_item = {
                'lon': item['geo_point_borne']['lon'],
                'lat': item['geo_point_borne']['lat']
            }
            parsed_data.append(parsed_item)


    with open('./static/vehicle_data/parse_charger.json', 'w') as f:
        json.dump(parsed_data, f)


def charger_coord(start_coords, end_coords, chargeKm):

    # Get the coordinates of the start and end cities
    geolocator = Nominatim(user_agent="my-app")


    # Set up the OpenRouteService client
    client = ors.Client(key='5b3ce3597851110001cf6248c657bdca154e429bbe142b1c567a62c3')

    # Get the route between the start and end coordinates
    route = client.directions(coordinates=[start_coords, end_coords], profile='driving-car', format='geojson')

    # Extract the coordinates from the route
    coords_list = [(coord[1], coord[0]) for coord in route['features'][0]['geometry']['coordinates']]

    # Calculate the total distance of the route
    total_distance = route['features'][0]['properties']['segments'][0]['distance'] / 1000

    # Set up the map
    m = folium.Map(location=[start_coords[1], start_coords[0]], zoom_start=5)

    # Add the start and end markers
    # folium.Marker(location=[start_coords[1], start_coords[0]], popup="Start").add_to(m)
    # folium.Marker(location=[end_coords[1], end_coords[0]], popup="End").add_to(m)

    charger_coords = []
    current_distance = 0
    my_var = 0
    for i, coords in enumerate(coords_list):
        if i == len(coords_list) - 1:
            break
        distance_between = distance.distance(coords, coords_list[i+1]).km
        current_distance += distance_between
        if int(current_distance) == chargeKm*my_var:
            # print(current_distance)
            my_var += 1
            popup = f"{int(current_distance)-100} km - {int(current_distance)} km"
            # folium.Marker(location=coords, popup=popup).add_to(m)
            charger_coords.append(coords)
        if current_distance > total_distance:
            break

    return charger_coords
    # Add the route to the map
    # folium.PolyLine(coords_list, color="blue").add_to(m)

    # Display the map
    # m.save("test.html")
