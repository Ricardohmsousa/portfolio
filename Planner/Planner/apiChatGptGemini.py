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
import pathlib
import textwrap
import uuid
from google.protobuf.json_format import Parse

from vertexai.preview.generative_models import (
    Content,
    FunctionDeclaration,
    GenerativeModel,
    Part,
    Tool,
    GenerationConfig
)
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from utils import generate_unique_identifier, to_markdown,get_directions,calculate_Ayrs,calculate_saved_emissions,getDataFromPDF,getRoutes
# Used to securely store your API key
from IPython.display import display
from IPython.display import Markdown
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\ricardo.msousa\\Downloads\\master-chariot-325508-45cfc29cdd73.json"

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],  # Update this with your frontend's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vertexai.init(project="master-chariot-325508", location="us-central1")
get_directions_dec = FunctionDeclaration(
    name="get_directions",
    description="Determine directions",
    parameters={
    "type": "object",
    "properties": {
      "origin": {
        "type": "string",
        "description": "The place of origin"
      },
      "destination": {
        "type": "string",
        "description": "The place of destination"
      },
      "mode": {
        "type": "string",
        "enum": [
          "driving",
          "walking",
          "bicycling",
          "transit"
        ],
        "description": "The transportation mode of the travel. it can ONLY be one of driving walking bicycling or transit"
      }
    },
    "required": [
      "origin",
      "destination",
      "mode"
    ]
  },
)

buy_ticket_dec = FunctionDeclaration(
    name="buy_ticket",
    description="Buy the ticket when , after sugested the users accepts it",
    parameters={
    "type": "object",
    "properties": {
      "type": {
        "type": "string",
        "enum": [
          "bus",
          "metro"
        ]
      }
    },
    "required": [
      "type"
    ]
  },
)
get_routes_dec = FunctionDeclaration(
    name="get_routes",
    description="get the routes existing in matosinhos",
    parameters={
    "type": "object",
    "properties": {
    },
    "required": [
    ]
  },
)
calculate_saved_emissions_dec = FunctionDeclaration(
    name="calculate_saved_emissions",
    description="calculate saved emissions based on the distance and transport type used. The transport types can only be ebike, escooter,eletric vehicle, metro, bus,combustion engine vehicle and walking",
    parameters={
    "type": "object",
    "properties": {
      "distance": {
        "type": "number",
        "description": "the distance to travel in meters"
      },
      "transport": {
        "type": "string",
        "enum": [
          "ebike",
          "escooter",
          "electric vehicle",
          "metro",
          "bus",
          "combustion engine vehicle",
          "walking"
        ]
      }
    },
    "required": [
      "transport"
    ]
  },
)


calculate_ayrs_dec = FunctionDeclaration(
    name="calculate_ayrs",
    description="Buy the ticket when , after sugested the users accepts it",
    parameters={
    "type": "object",
    "properties": {
      "co2": {
        "type": "number",
        "description": "grams of co2 saved"
      }
    },
    "required": [
      "co2"
    ]
  },
)
getDataFromPDF_dec = FunctionDeclaration(
    name="getDataFromPDF",
    description="answers about the what is sustainability pdf",
    parameters={
    "type": "object",
    "properties": {
      "prompt": {
        "type": "string",
        "description": "the prompt made by the user"
      }
    },
    "required": [
      "prompt"
    ]
  },
)

planner = Tool(
    function_declarations=[get_directions_dec,calculate_saved_emissions_dec,calculate_ayrs_dec,calculate_ayrs_dec,calculate_saved_emissions_dec,buy_ticket_dec,getDataFromPDF_dec,get_routes_dec]
)
generation_config = GenerationConfig(
    temperature=0.1,
    top_p=1.0,
    top_k=32,
    candidate_count=1,
    max_output_tokens=8192,
)

model = GenerativeModel('gemini-pro', tools=[planner],generation_config=generation_config)

class Message(BaseModel):
    content: str
    threadId: str
 
@app.get("/")
def read_root():
    return {"Hello": "World"}

chats={}

@app.post("/create-chat/")
async def create_chat():
    thread_id=generate_unique_identifier()
    print("chega aqui")
    chat = model.start_chat(history=[])
    response = chat.send_message(
      "És um agente que ajuda em viagens de transporte publico. Responde em PT-PT. Quando recebes a informação do get_directions, anota diretamente no mapa a informação e pergunta se quer comprar a viagem , se for de metro ou autocarro. Sê claro e simples nas direções que dás. para dados do getDataFromPDF, responde apenas o que te é devolvido pela função")
    chats[thread_id]=chat
    return thread_id

@app.post("/send-message/") 
async def send_message(request: Request, message: Message ):
    chat=chats[message.threadId]
    response = chat.send_message(message.content)
    content = response.candidates[0].content
    mes={}
    abcd=content
    print(abcd)
# Check if 'function_call' key is present in the content
    while   'function_call' in str(abcd):
        function_call=content.parts[0].function_call
        name=function_call.name
        if name=="get_directions":

          args=function_call.args.pb
          origin=args.get("origin").string_value
          #origin = bytes(origin, "utf-8").decode("unicode_escape")

          destination=args.get("destination").string_value
          #destination = bytes(destination, "utf-8").decode("unicode_escape")

          mode=args.get("mode").string_value
          b=get_directions(origin,destination,mode)
          b = json.dumps(b)
          mes["display"]=b
          mes["mode"]=mode
          response = chat.send_message(
            Part.from_function_response(
              name=name,
              response={
                "content": b,
              },
            ),
          )
          
          if 'function_call' in str(response.candidates[0].content.parts[0]):
            content = response.candidates[0].content
            abcd=content.parts[0]
          else :
            mes["message"]=response.candidates[0].content.parts[0].text
            return mes
        if name=="get_routes":
          a = getRoutes()
          response = chat.send_message(
            Part.from_function_response(
              name=name,
              response={
                "content": str(a),
              },
            ),
          )
          print("get_routes")
          mes["message"]=response.candidates[0].content.parts[0].text
          return mes
        if name=="calculate_saved_emissions":
          print(calculate_saved_emissions)
          args=function_call.args.pb
          transport=args.get("transport").string_value
          #origin = bytes(origin, "utf-8").decode("unicode_escape")
          distance=args.get("distance").number_value
          #destination = bytes(destination, "utf-8").decode("unicode_escape")
          a = calculate_saved_emissions(distance,transport)
          response = chat.send_message(
            Part.from_function_response(
              name=name,
              response={
                "content": str(a) + " emitions were saved",
              },
            ),
          )
          print(response.candidates[0].content.parts[0])
          
          if 'function_call' in str(response.candidates[0].content.parts[0]):
            content = response.candidates[0].content
            abcd=content.parts[0]
            print("chega aqui")
          else:
            mes["message"]=response.candidates[0].content.parts[0].text
            return mes
        if name=="calculate_ayrs":
          args=function_call.args.pb
          co2=args.get("co2").number_value
          a = calculate_Ayrs(co2)
          response = chat.send_message(
            Part.from_function_response(
              name=name,
              response={
                "content": a,
              },
            ),
          )
          if 'function_call' in str(response.candidates[0].content.parts[0]):
            content = response.candidates[0].content
            abcd=content.parts[0]
            print("chega aqui")
          else:
            print(response.candidates[0].content.parts[0])
            mes["message"]=response.candidates[0].content.parts[0].text
            return mes
        if name=="buy_ticket":
            response = chat.send_message(
            Part.from_function_response(
              name=name,
              response={
                "content": "Ticket can be bought here: https://www.lipsum.com/" ,
              },
            ),
          )
            
            if 'function_call' in str(response.candidates[0].content.parts[0]):
              content = response.candidates[0].content
              abcd=content.parts[0]
            else:
              mes["message"]=response.candidates[0].content.parts[0].text
              return mes
        if name=="getDataFromPDF":
          args=function_call.args.pb
          question=args.get("prompt").string_value
          print(question)
          a = getDataFromPDF(question)
          response = chat.send_message(
            Part.from_function_response(
              name=name,
              response={
                "content": a ,
              },
            ),
          )
            
          if 'function_call' in str(response.candidates[0].content.parts[0]):
              content = response.candidates[0].content
              abcd=content.parts[0]
          else:
              mes["message"]=response.candidates[0].content.parts[0].text
              return mes
    # Wait for the assistant's response
    mes["message"]=response.candidates[0].content.parts[0].text
    return mes