from fastapi import FastAPI, Request
import requests
from langserve import RemoteRunnable
from langchain_core.messages import HumanMessage, AIMessage
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


app = FastAPI()
remote_runnable = RemoteRunnable("http://localhost:8001/agent")
# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5000"],  # Update this with your frontend's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

chats={}

class Message(BaseModel):
    content: str
    threadId: str
 
@app.post("/create-chat/")
async def create_chat():
    thread_id=generate_unique_identifier()
    chats[thread_id]=[]
    return thread_id

@app.post("/send-message/") 
async def send_message(request: Request, message: Message ):
    chat_history=chats[message.threadId]
    print(chat_history)
    ai =  remote_runnable.invoke({"input": message.content, "chat_history": chat_history})
    mes={}
    print(ai["output"])
    if "answer" in str(ai["output"]):
        a = json.loads(ai['output'])
        mes["message"]=a["answer"]
        mes["display"]=a["polyline"]
        mes["startLocationLat"]=a["startLocationLatitude"]
        mes["startLocationLong"]=a["startLocationLongitude"]
        mes["endLocationLat"]=a["endLocationLatitude"]
        mes["endLocationLong"]=a["endLocationLongitude"]
        chat_history.extend([HumanMessage(content=message.content), AIMessage(content=a["answer"])])
    else: 
        mes["message"]=ai["output"]
        chat_history.extend([HumanMessage(content=message.content), AIMessage(content=ai["output"])])
    chats[message.threadId]=chat_history
    print(mes)
    return mes