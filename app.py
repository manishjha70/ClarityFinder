from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_core.agents import AgentFinish
from langgraph.graph import END, Graph
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64

# Load environment variables from a .env file
load_dotenv()

# Create the static directory if it does not exist
if not os.path.exists("static"):
    os.makedirs("static")

# Define the tools for retrieving search results
tools = [TavilySearchResults(max_results=1)]

# Pull the prompt template for the OpenAI function agent
prompt = hub.pull("hwchase17/openai-functions-agent")

# Initialize the Google Generative AI model (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # Specify the model to use
    temperature=0.7,         # Control the randomness of responses
    max_tokens=8192          # Maximum token limit for responses
)

# Create an OpenAI function agent using the specified tools and prompt
agent_runnable = create_openai_functions_agent(llm, tools, prompt)

# Assign the agent's outcome to a RunnablePassthrough for easy invocation
agent = RunnablePassthrough.assign(
    agent_outcome=agent_runnable
)

def execute_tools(data):
    """
    Execute the tools based on the agent's action.
    """
    # Retrieve the agent's action and remove it from data
    agent_action = data.pop('agent_outcome')
    tool_to_use = {t.name: t for t in tools}[agent_action.tool]
    
    # Invoke the selected tool with the provided input
    observation = tool_to_use.invoke(agent_action.tool_input)
    
    # Append the agent's action and observation to the intermediate steps
    data['intermediate_steps'].append((agent_action, observation))
    return data

def should_continue(data):
    """
    Determine whether the workflow should continue or exit.
    """
    return "exit" if isinstance(data['agent_outcome'], AgentFinish) else "continue"

# Create a directed graph for the workflow
workflow = Graph()

# Add nodes to the graph
workflow.add_node("agent", agent)
workflow.add_node("tools", execute_tools)

# Set the entry point for the workflow
workflow.set_entry_point("agent")

# Define conditional edges based on the outcome of the agent
workflow.add_conditional_edges(
    "agent",  # Start node
    should_continue,
    {
        "continue": "tools",  # Continue to tools if the agent hasn't finished
        "exit": END           # Exit the workflow if finished
    }
)

# Connect the tools node back to the agent node
workflow.add_edge('tools', 'agent')

# Compile the workflow into a chain for execution
chain = workflow.compile()

def make_serializable(obj):
    """
    Recursively convert objects to a serializable format.
    """
    if isinstance(obj, dict):
        return {key: make_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(element) for element in obj]
    elif isinstance(obj, set):
        return list(obj)
    elif hasattr(obj, "__dict__"):
        # Convert custom objects to strings for serialization
        return str(obj)
    else:
        return obj

# Initialize FastAPI application
app = FastAPI()

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
    """
    Render the homepage template.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_query")
async def process_query(query: str = Form(...)):
    """
    Process a user's query and return the summarized result.
    """
    intermediate_steps = []
    
    # Invoke the workflow chain with the user's query
    raw_data = chain.invoke({"input": query, "intermediate_steps": intermediate_steps})
    
    # Encode the raw data in base64 for safe transmission
    encoded_raw_data = base64.b64encode(str(raw_data).encode()).decode()
    
    # Extract the desired output from the agent's response
    desired_output = raw_data["agent_outcome"].return_values['output']
    
    # Navigate through the intermediate steps to extract the URL
    url = raw_data["intermediate_steps"][0][1][0]["url"]
    
    return JSONResponse(content={"raw_data": encoded_raw_data, "desired_output": desired_output, "url": url})
