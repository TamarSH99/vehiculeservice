import requests
import json
from graphqlclient import GraphQLClient

def retrieve_vehicle_properties():
  # Define the GraphQL query
  query = '''
  query vehicleListAll {
    vehicleList {
      id
      naming {
        make
        model
      }
      connectors {
      time
      }
      battery {
        usable_kwh
      }
      body {
        seats
      }
      media {
        image {
          url
        }
      }
    }
  }
  '''

  # Set the request headers
  headers = {
      'x-app-id': '640f38cd75ebf0917938883f',
      'x-client-id': '640f38cd75ebf0917938883d',
      'Content-Type': 'application/json'
  }

  # Set the request payload
  payload = {
      'query': query
  }

  # Send the GraphQL query to the ChargeTrip API endpoint
  response = requests.post('https://api.chargetrip.io/graphql', headers=headers, json=payload)

  # Parse the JSON response into a Python dictionary
  response_dict = json.loads(response.text)

  # Extract the data from the dictionary
  vehicle_list = response_dict['data']['vehicleList']
  optm_list = []
    

  for vehicle in vehicle_list:
    tmp = {"id": vehicle['id'], "model": vehicle['naming']['make'],"time": vehicle['connectors'][0]['time'], "kWh" : vehicle['battery']['usable_kwh'], "seats" : vehicle['body']['seats'], "image": vehicle['media']['image']['url']}
    # print(tmp)
    optm_list.append(tmp)

  with open('./static/vehicle_data/vehicle_data.json', 'w') as f:
       json.dump(optm_list, f)
  

retrieve_vehicle_properties()