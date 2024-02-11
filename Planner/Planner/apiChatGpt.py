from fastapi import FastAPI, Request
# Import necessary libraries
from urllib.parse import unquote
from openai import OpenAI
import json
from ipyleaflet import Map, Marker, basemaps, basemap_to_tiles, Polyline
from geopy.geocoders import Nominatim
from polyline import decode
import folium
from IPython.display import clear_output
from pydantic import BaseModel
import requests
from fastapi.middleware.cors import CORSMiddleware  # Add this line
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],  # Update this with your frontend's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = OpenAI(
    api_key="key here",
)
assistant = client.beta.assistants.retrieve("asst_keWqWObB2DahzbLW5obPHnDr") #asst_keWqWObB2DahzbLW5obPHnDr
#asst_69tFvRrVShTpYuEDdFcQRQlJ
class Message(BaseModel):
    content: str
    threadId: str

def get_directions(origin, destination,mode):
    origin= unquote(origin)
    destination=unquote(destination)
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': origin,
        'destination': destination,
        'key': 'key here',
        'mode':mode
    }

    try:
          response = requests.get(base_url, params=params)
          print(origin)
          print(destination)
          print(mode)
          response.raise_for_status()  # Raise an HTTPError for bad responses
          route_data = response.json()
         
          return route_data
    except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None
def calculate_Ayrs(co2):
    print(co2)
    return co2/100
class ApplicationProperties:
    def __init__(self, emissions_mts, mix_energy_pt):
        self.emissionsMTS = emissions_mts
        self.mixEnergyPT = mix_energy_pt
def calculate_saved_emissions(distance, transport_type):
    # Hardcoded constant values
    properties = ApplicationProperties(emissions_mts=122.5, mix_energy_pt=173.7)
 
    distance_km = distance / 1000
 
    if transport_type == 'ebike' or transport_type == 'escooter':
        vehicle_emissions = 3.47
    elif transport_type == 'electric vehicle':
        vehicle_emissions = 39.95
    elif transport_type == 'metro':
        vehicle_emissions = 62
    elif transport_type == 'bus':
        vehicle_emissions = 119
    elif transport_type == 'combustion engine vehicle':
        vehicle_emissions = 122.5
    elif transport_type=='walking':
        vehicle_emissions=0
    else:
        # Handle unknown transport type
        raise ValueError("Unknown transport type")
 
    saved_emissions_per_km = properties.emissionsMTS - vehicle_emissions
 
    return str(saved_emissions_per_km * distance_km) + " g"

 
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}

@app.post("/create-chat/")
async def create_chat():
    thread = client.beta.threads.create()
    return thread.id

@app.post("/send-message/")
async def send_message(request: Request, message: Message ):
    thread = client.beta.threads.retrieve(message.threadId)
    user_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message.content,
    )

    # Run the OpenAI assistant
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
    # Wait for the assistant's response
    mes={}
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        if run.status == "requires_action" and run.required_action.type == "submit_tool_outputs":
            tool_outputs = []

            for call in run.required_action.submit_tool_outputs.tool_calls:
              print(call.function.name)
              if call.function.name=="get_directions":
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
                mes["display"]=b
                mes["mode"]=mode


              if call.function.name=="buy_ticket":
                json_data = call.function.arguments
                data = json.loads(json_data)
                type=data["type"]
                tool_outputs.append({
                  "tool_call_id": call.id,
                  #"output": "Ticket Bought for " + type,
                  "output": "Ticket can be bought here: https://www.lipsum.com/"
                })
              if call.function.name=="calculate_saved_emissions":
                json_data = call.function.arguments
                data = json.loads(json_data)
                distance=data["distance"]
                transport=data["transport"]
                a = calculate_saved_emissions(distance,transport)
                print(a)
                tool_outputs.append({
                  "tool_call_id": call.id,
                  "output": a,
                })
              if call.function.name=="calculate_ayrs":
                json_data = call.function.arguments
                data = json.loads(json_data)
                co2=data["co2"]
                a = calculate_Ayrs(co2)
                print(a)
                tool_outputs.append({
                  "tool_call_id": call.id,
                  "output": a,
                })
            run = client.beta.threads.runs.submit_tool_outputs(
                  thread_id=thread.id,
                  run_id=run.id,
                  tool_outputs=tool_outputs,
            )


    # Display the conversation
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    mes["message"]=messages.data[0].content[0].text.value
    return mes
