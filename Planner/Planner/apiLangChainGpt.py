#!/usr/bin/env python
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from typing import List
from typing import Type,Sequence
from langchain.prompts import PromptTemplate
import json
from langchain_core.language_models import BaseLanguageModel
from langchain_core.pydantic_v1 import root_validator
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.tools import BaseTool
from langchain_core.utils.function_calling import convert_to_openai_function

from langchain.agents import BaseSingleActionAgent
from langchain.agents.format_scratchpad.openai_functions import (
    format_to_openai_function_messages,
)
from langchain.agents.output_parsers.openai_functions import (
    OpenAIFunctionsAgentOutputParser,
)

from langchain_core.agents import AgentAction, AgentActionMessageLog, AgentFinish
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from typing import Any, List, Union
from langchain_core.messages import AIMessage, FunctionMessage, HumanMessage
from langchain.tools import BaseTool
from langchain.vectorstores import Chroma
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.messages import BaseMessage
from langserve import add_routes
import requests
from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field

responsa=""
class Response(BaseModel):
    """Final response to the question being asked"""

    answer: str = Field(description="The final answer to respond to the user")
    polyline: str= Field(
        description="the overview polyline json")
    startLocationLatitude : float = Field(description="the start location latitude")
    startLocationLongitude: float = Field(description="start location longitude")
    endLocationLatitude: float = Field(description="end location latitude")
    endLocationLongitude: float  = Field(description="end location longitude")

def parse(output):
    # If no function was invoked, return to user
    if "function_call" not in output.additional_kwargs:
        return AgentFinish(return_values={"output": output.content}, log=output.content)

    # Parse out the function call
    function_call = output.additional_kwargs["function_call"]
    name = function_call["name"]
    inputs = json.loads(function_call["arguments"])

    # If the Response function was invoked, return to the user with the function inputs
    if name == "Response":
        print("chega aqui")
        print(inputs)
        return AgentFinish(return_values={"output":json.dumps(inputs)}, log=str(function_call))
    # Otherwise, return an agent action
    else:
        return AgentActionMessageLog(
            tool=name, tool_input=inputs, log="", message_log=[output]
        )
# 1. Load Retriever
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")

docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings(openai_api_key="key here")
vector = FAISS.from_documents(documents, embeddings)
retriever = vector.as_retriever()

# 2.1 Load PDF Retriever
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("C://Users//ricardo.msousa//Downloads//AYR_CarbonExV0.1.pdf")
pages = loader.load_and_split()



directory = 'index_store'
vector_index = Chroma.from_documents(pages,embeddings, persist_directory=directory)


loader = PyPDFLoader("C://Users//ricardo.msousa//Downloads//AYR3.pdf")
pages_new = loader.load_and_split(text_splitter)
_=  vector_index.add_documents(pages_new)
vector_index.persist()

loader = PyPDFLoader("C://Users//ricardo.msousa//Downloads//Website - News.pdf")
pages_new = loader.load_and_split(text_splitter)
_=  vector_index.add_documents(pages_new)
vector_index.persist()

loader = PyPDFLoader("C://Users//ricardo.msousa//Downloads//Cities website 1.pdf")
pages_new = loader.load_and_split(text_splitter)
_=  vector_index.add_documents(pages_new)
vector_index.persist()

loader = UnstructuredPowerPointLoader("C:\\Users\\ricardo.msousa\\Downloads\\AYR_ 18.pptx")
data = loader.load()
_ = vector_index.add_documents(data)
vector_index.persist()

loader = UnstructuredPowerPointLoader("C:\\Users\\ricardo.msousa\\Downloads\\BE_THE_CHANGE_template_ppt_FINAL 1.pptx")
data = loader.load()
_ = vector_index.add_documents(data)
vector_index.persist()

loader = UnstructuredPowerPointLoader("C:\\Users\\ricardo.msousa\\Downloads\\AYR_V17.2_PT.pptx")
data = loader.load()
_ = vector_index.add_documents(data)
vector_index.persist()

loader = UnstructuredPowerPointLoader("C:\\Users\\ricardo.msousa\\Downloads\\AYR Wallet & 3rd party.pptx")
data = loader.load()
_ = vector_index.add_documents(data)
vector_index.persist()

retriever2 = vector_index.as_retriever(search_type="similarity", search_kwargs={"k":6})
retriever_tool2 = create_retriever_tool(
    retriever2,
    "AYR_Retriever",
    "Search for information about AYR. For any questions about AYR, you must use this tool!",
)
print("chegaaqui")


def get_directions(origin, destination,mode):
    origin= origin
    destination=destination
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
          print(route_data)
          return route_data
    
    except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None
class ApplicationProperties:
    def __init__(self, emissions_mts, mix_energy_pt):
        self.emissionsMTS = emissions_mts
        self.mixEnergyPT = mix_energy_pt
def calculate_saved_emissions(distance, transport_type):
    print(distance)
    print(transport_type)
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
class GetDirectionsInput(BaseModel):
    """Inputs for my_profile function"""
    origin: str = Field(description="origin of the trip")
    destination: str = Field(description="destination of the trip")
    mode: str = Field(description="means of transportation of the trip, it can be one of driving,walking, bicycling,transit. if no means is given, use transit.")


class GetDirectionsTool(BaseTool):
    name = "get_directions"
    description = """
        Useful to get google maps directions
        """
    args_schema: Type[BaseModel] = GetDirectionsInput

    def _run(self, origin: str,destination:str,mode:str):
        profile_detail_attribute = get_directions(origin,destination,mode)
        return profile_detail_attribute

class CalculateSavedEmissionsInput(BaseModel):
    """Inputs for my_profile function"""
    distance: int = Field(description="distance of the trip")
    transport_type: str = Field(description="transport type of the trip")


class CalculateSavedEmissionsTool(BaseTool):
    name = "calculate_saved_emissions"
    description = """
        calculate saved emissons from the data from google maps. you need to use the get_directions tool before this one if you do not know the distance.
        """
    args_schema: Type[BaseModel] = CalculateSavedEmissionsInput

    def _run(self, distance: int,transport_type:str):
        profile_detail_attribute = calculate_saved_emissions(distance,transport_type)
        return profile_detail_attribute

class BuyTicketInput(BaseModel):
    """Inputs for my_profile function"""
    transport_type: int = Field(description="type of transport")
    transport_number: str = Field(description="the identifier of the line")


class BuyTicketTool(BaseTool):
    name = "buy_ticket"
    description = """
        buys the ticket
        """
    args_schema: Type[BaseModel] = BuyTicketInput

    def _run(self, transport_number: int,transport_type:str):
        profile_detail_attribute = buy_ticket()
        return profile_detail_attribute

def buy_ticket():
    return "Ticket can be bought here: https://www.lipsum.com/"
tools = [retriever_tool2,BuyTicketTool(),GetDirectionsTool(),CalculateSavedEmissionsTool(),Response]
tools2 = [retriever_tool2,GetDirectionsTool(),CalculateSavedEmissionsTool(),BuyTicketTool()]


# 3. Create Agent
prompt = hub.pull("ricardohmsousa/openai-functions-agent")
llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0,openai_api_key="key here")
def create_openai_functions_agent_with_parser(
    llm: BaseLanguageModel, tools: Sequence[BaseTool], prompt: ChatPromptTemplate
) -> Runnable:
    """Create an agent that uses OpenAI function calling.

    Args:
        llm: LLM to use as the agent. Should work with OpenAI function calling,
            so either be an OpenAI model that supports that or a wrapper of
            a different model that adds in equivalent support.
        tools: Tools this agent has access to.
        prompt: The prompt to use. See Prompt section below for more.

    Returns:
        A Runnable sequence representing an agent. It takes as input all the same input
        variables as the prompt passed in does. It returns as output either an
        AgentAction or AgentFinish.

    Example:

        Creating an agent with no memory

        .. code-block:: python

            from langchain_community.chat_models import ChatOpenAI
            from langchain.agents import AgentExecutor, create_openai_functions_agent
            from langchain import hub

            prompt = hub.pull("hwchase17/openai-functions-agent")
            model = ChatOpenAI()
            tools = ...

            agent = create_openai_functions_agent(model, tools, prompt)
            agent_executor = AgentExecutor(agent=agent, tools=tools)

            agent_executor.invoke({"input": "hi"})

            # Using with chat history
            from langchain_core.messages import AIMessage, HumanMessage
            agent_executor.invoke(
                {
                    "input": "what's my name?",
                    "chat_history": [
                        HumanMessage(content="hi! my name is bob"),
                        AIMessage(content="Hello Bob! How can I assist you today?"),
                    ],
                }
            )

    Prompt:

        The agent prompt must have an `agent_scratchpad` key that is a
            ``MessagesPlaceholder``. Intermediate agent actions and tool output
            messages will be passed in here.

        Here's an example:

        .. code-block:: python

            from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", "You are a helpful assistant"),
                    MessagesPlaceholder("chat_history", optional=True),
                    ("human", "{input}"),
                    MessagesPlaceholder("agent_scratchpad"),
                ]
            )
    """
    if "agent_scratchpad" not in prompt.input_variables:
        raise ValueError(
            "Prompt must have input variable `agent_scratchpad`, but wasn't found. "
            f"Found {prompt.input_variables} instead."
        )
    llm_with_tools = llm.bind(functions=[convert_to_openai_function(t) for t in tools])
    agent = (
        RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            )
        )
        | prompt
        | llm_with_tools
        | parse
    )
    return agent
agent = create_openai_functions_agent_with_parser(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools2, verbose=True)


# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

# We need to add these input/output schemas because the current AgentExecutor
# is lacking in schemas.

class Input(BaseModel):
    input: str
    chat_history: List[Union[HumanMessage, AIMessage, FunctionMessage]] = Field(
        ...,
        extra={"widget": {"type": "chat", "input": "location"}},
    )


class Output(BaseModel):
    output: str

add_routes(
    app,
    agent_executor.with_types(input_type=Input, output_type=Output),
    path="/agent",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001)
    print("Ready")