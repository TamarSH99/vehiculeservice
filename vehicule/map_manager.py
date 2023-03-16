import openrouteservice
from openrouteservice import convert
import folium
import json
import routes as Routes
from geopy.geocoders import Nominatim
import charger as charger
from haversine import haversine, Unit
from folium import Map, Marker, Popup
from geopy.distance import distance



def find_chargers(charger_lst):
    with open('./static/vehicle_data/parse_charger.json', 'r') as f:
        json_data = json.load(f)
    # list to hold the close coordinates
    close_coords = []

    # iterate through the list of charger coordinates
    for charger_coord in charger_lst:
        tmp = []
        # iterate through the JSON file coordinates
        for json_coord in json_data:
            # calculate the distance between the charger coordinate and the JSON coordinate using haversine
            dist = haversine(charger_coord, (json_coord['lat'], json_coord['lon']), unit=Unit.METERS)
            # if the distance is less than or equal to 3km, add the JSON coordinate to the list of close coordinates
            if dist <= 5000:
                tmp.append(json_coord)
        close_coords.append({charger_coord : tmp})
    return close_coords



def retrieve_properties(carId):
    count = 0
    jsonfile = open('./static/vehicle_data/vehicle_data.json')
    data = json.load(jsonfile)
    for entry in data:
        if count == carId:
            jsonfile.close()
            return {'img': entry['image'], 'chargeMn': entry['time'], 'chargeKm':entry['kWh'] }
        count +=1

    jsonfile.close()
    return None

def validate_cities(city_1, city_2):
    print(city_1, city_2)
    geolocator = Nominatim(user_agent="my_app")
    location_1 = geolocator.geocode(city_1)
    location_2 = geolocator.geocode(city_2)
    if location_1 and location_2:
        return [location_1, location_2 ]
    return False



def map_manager( city_1='-', city_2='-', carId = '0'):
    #actual API_KEY 
    api_key = '5b3ce3597851110001cf6248c657bdca154e429bbe142b1c567a62c3'
    client = openrouteservice.Client(key=api_key)
    
    result = validate_cities( city_1, city_2)
    if result is False:
        map = folium.Map()
        map.save('./templates/main.html')
        return False 
    location_1 = result[0]
    location_2 = result[1]



    start_point = (location_1.longitude, location_1.latitude)
    end_point = (location_2.longitude, location_2.latitude)
    coords = (start_point, end_point)

    my_routes = Routes.Routes(start_point=start_point, end_point=end_point)
    my_routes.find_route(client=client)
    my_routes.print_route_data()

    map = folium.Map(location=(location_1.latitude, location_1.longitude), zoom_start=7, control_scale=True)

    properties =  retrieve_properties(int(carId))
    full_charge_time = int(my_routes.directions['routes'][0]['summary']['distance'])/60/int(properties['chargeKm'])*int(properties['chargeMn'])
    trevel_time = full_charge_time+ int(my_routes.directions['routes'][0]['summary']['duration'])
    
    distance_txt = "<div style='border: 2px solid dodgerblue; border-radius: 5px; padding: 5px;'>" \
                    "<h4 style='margin: 0; color: dodgerblue;'>Distance: " \
                    "<strong>" + str(round(my_routes.directions['routes'][0]['summary']['distance'] / 1000, 1)) + " Km</strong></h4>" \
                    "</div>"

    duration_txt = "<div style='border: 2px solid dodgerblue; border-radius: 5px; padding: 5px;'>" \
                    "<h4 style='margin: 0; color: dodgerblue;'>Duration: " \
                    "<strong>" + str(round(trevel_time / 60 / 60, 1)) + " hours</strong></h4>" \
                    "</div>"


    carIcon = folium.features.CustomIcon(properties['img'], icon_size=(120,67), icon_anchor=(0, 0))
    pushpinIcon = folium.features.CustomIcon('./static/images/pushpin.png', icon_size=(60,60), )
    folium.Marker(
        location=list(coords[0][::-1]),
        popup=city_1,
        icon=carIcon,
    ).add_to(map)

    folium.Marker(
        location=list(coords[1][::-1]),
        popup=city_2,
        icon=pushpinIcon,
    ).add_to(map)


    folium.map.Marker(
        location=(location_1.latitude, location_1.longitude),
        icon=folium.DivIcon(html=distance_txt+duration_txt, icon_size=(200,200), icon_anchor=(200,0)),
    ).add_to(map)


    charger_lst = charger.charger_coord(start_point, end_point, properties['chargeKm'])
    available_chargers_coord = find_chargers(charger_lst)
    stationIcon = folium.features.CustomIcon('./static/images/charging_station.png', icon_size=(100,100),)

    for chargers_dict in available_chargers_coord:
        chargers_coord = list(chargers_dict.keys())[0]
        chargers_data = chargers_dict[chargers_coord]
        if not chargers_data:
            folium.Marker(location=[chargers_coord[0], chargers_coord[1]], icon=folium.Icon(color='red'), popup='Il n\'y a pas de Borne').add_to(map)
        else:
            for coord in chargers_data:
                lat = coord['lat']
                lon = coord['lon']
                folium.Marker(location=[lat, lon], popup='Borne', icon=folium.Icon(color='green')).add_to(map)



   
    folium.GeoJson(my_routes.decoded).add_to(map)
    # Adjust the zoom level and position of the map to fit the specified bounds
    map.fit_bounds(my_routes.bounds)

    map.save('./templates/main.html')

