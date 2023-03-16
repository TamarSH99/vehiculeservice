from openrouteservice import convert

class Routes:
    def __init__(self, start_point, end_point):
        self.start_point = start_point # Define start point (longitude, latitude)
        self.end_point = end_point   # Define the end point (longitude, latitude) 
        self.profile = 'driving-car'  # Define the profile of the route (e.g., driving-car, cycling-regular, foot-walking)
        self.directions = None
        self.distance =  None #km
        self.duration = None  #mn
        self.geometry = None
        self.decode = None
        self.bounds = [(start_point[1], start_point[0]) , (end_point[1], end_point[0])] # # Define the bounds of the map using the coordinates of the two cities
        print(self.start_point, self.end_point)

    def find_route(self, client):
        # Get directions between the start and end points
        self.directions = client.directions(coordinates=[self.start_point, self.end_point], profile=self.profile)
        self.geometry = client.directions((self.start_point, self.end_point))['routes'][0]['geometry']
        self.decoded = convert.decode_polyline(self.geometry)

    def print_route_data(self):
       # Print the distance and duration of the route
        route = self.directions['routes'][0]
        self.distance = int(route['summary']['distance']) / 1000  # convert to kilometers
        self.duration = int(route['summary']['duration']) / 60    # convert to minutes
        print(f'The route is {self.distance:.2f} km long and takes {self.duration:.1f} minutes.')

# distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(directions['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
# duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(directions['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
