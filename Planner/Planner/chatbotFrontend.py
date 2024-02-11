# Import necessary libraries
from openai import OpenAI
import json
from ipyleaflet import Map, Marker, basemaps, basemap_to_tiles, Polyline
from geopy.geocoders import Nominatim
from polyline import decode
import folium
from IPython.display import clear_output
# Initialize OpenAI client with API key
client = OpenAI(
    api_key="key here",
)

import requests

def get_directions(origin, destination,mode):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': origin,
        'destination': destination,
        'key': 'key here',
        'mode':mode
    }

    try:
          response = requests.get(base_url, params=params)
          response.raise_for_status()  # Raise an HTTPError for bad responses
          route_data = response.json()
          polyline_points = route_data['routes'][0]['overview_polyline']['points']
    # De  coding polyline points to get coordinates
          decoded_points = decode(polyline_points)

          # Initializing the map with the starting location
          start_location = route_data['routes'][0]['legs'][0]['start_location']
          map_center = [start_location['lat'], start_location['lng']]

          # Adding markers for start and end locations
          folium.Marker(
              location=[start_location['lat'], start_location['lng']],
              popup='Start Location',
              icon=folium.Icon(color='green')
          ).add_to(m)

          end_location = route_data['routes'][0]['legs'][0]['end_location']
          folium.Marker(
              location=[end_location['lat'], end_location['lng']],
              popup='End Location',
              icon=folium.Icon(color='red')
          ).add_to(m)

          # Adding the polyline to the map
          folium.PolyLine(
              locations=decoded_points,
              color='blue',
              weight=5,
              opacity=0.7
          ).add_to(m)
          clear_output(wait=True)
          display(m)
          return route_data
    except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None



# Create a map centered at a specific location and with a specified zoom level
initial_center = (41.1579, -8.6291)  # Porto coordinates
initial_zoom = 12
m = folium.Map(location=initial_center, zoom_start=initial_zoom)

# Create a basemap layer
#basemap_layer = basemaps.OpenStreetMap.Mapnik
#m.add_layer(basemap_layer)

# Display the map
#display(m)




# Retrieve OpenAI assistant information
assistant = client.beta.assistants.retrieve("asst_keWqWObB2DahzbLW5obPHnDr")

# Create a new conversation thread
thread = client.beta.threads.create()
user_input = ""

# Conversation loop
while user_input != "q":
    # Get user input
    user_input = input("You: ")

    # Send user input as a message
    user_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )

    # Run the OpenAI assistant
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    # Wait for the assistant's response
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "requires_action" and run.required_action.type == "submit_tool_outputs":
            tool_outputs = []
            
            for call in run.required_action.submit_tool_outputs.tool_calls:
              print(call.function.name)
              json_data = call.function.arguments
              data = json.loads(json_data)
              origin=data["origin"]
              destination=data["destination"]
              mode=data["mode"]
              b=get_directions(origin,destination,mode)
              b = json.dumps(b)
              tool_outputs.append({
                "tool_call_id": call.id,
                "output": b,
              })
              run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs,
              )



    # Display the conversation
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.data[0].role, ":", messages.data[0].content[0].text.value)
