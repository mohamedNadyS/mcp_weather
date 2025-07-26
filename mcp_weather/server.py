"""
import fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mcp_weather.weather import gweather
from mcp_weather.agent import Agent
from mcp_weather.memory import Memory
from mcp_weather.massage import Massage

templates = Jinja2Templates(directory="templates")
app = fastapi.FastAPI()
memory= Memory()
agent = Agent()
print(dir(Memory))

@app.get("/", response_class=HTMLResponse)
def form_get(request: fastapi.Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.post("/",response_class=HTMLResponse)
async def form_post(request: fastapi.Request,city: str = fastapi.Form(...)):
    weather_result = gweather(city)
    user_massage = Massage("User", f"weather {city}")
    weather_msg = Massage("weatherTool", weather_result)
    memory.add(weather_msg)
    memory.add(user_massage)
    memory.saveFile()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": weather_result,
        "result_city": city.title()  
    })

@app.post("/message")
async def rmassage(request: fastapi.Request):
    data = await request.json()
    content = data["content"]
    user_msg = Massage("User",content)
    memory.add(user_msg)
    if content.lower().startswith("weather"):
        city = content.split("weather")[-1].strip()
        result = gweather(city)
        toolMassage = Massage("weatherTool", result)
        memory.add(toolMassage)
        memory.saveFile()
        return {"from": "weatherTool",
                "city": city.title(),
                "weather": result
        }
    reply = agent.respond(memory.get())
    replyMassage = Massage(agent.name, reply)
    memory.add(replyMassage)
    memory.saveFile()
    return {"response": reply}

@app.get("/history")
async def Ghistory():
    return {"history": [str(m) for m in memory.get()]}

"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import uuid
from datetime import datetime
import os

# Simple classes defined directly in server.py
class Massage:
    def __init__(self, sender, content, metadata=None):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()
        self.sender = sender
        self.content = content
        self.metadata = metadata or {}

    def __repr__(self):
        return f"[{self.timestamp}] {self.sender}: {self.content} (ID: {self.id})"

class Memory:
    def __init__(self):
        self.history = []
    
    def add(self, item):
        self.history.append(item)
    
    def get(self):
        return self.history

class Agent:
    def __init__(self, name="Agent"):
        self.name = name
    
    def respond(self, context):
        last = context[-1].content if context else ""
        return f"Echo: '{last}' understood"

def gweather(city: str) -> str:
    """Get the weather for a given city"""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize FastAPI
app = FastAPI(title="MCP Weather Tool")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize components
memory = Memory()
agent = Agent()

@app.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def form_post(request: Request, city: str = Form(...)):
    weather_result = gweather(city)
    
    # Add to memory
    user_message = Massage("User", f"weather {city}")
    weather_msg = Massage("weatherTool", weather_result)
    memory.add(user_message)
    memory.add(weather_msg)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": weather_result,
        "result_city": city.title()
    })

@app.post("/message")
async def receive_message(request: Request):
    data = await request.json()
    content = data["content"]
    user_msg = Massage("User", content)
    memory.add(user_msg)
    
    if content.lower().startswith("weather"):
        city = content.split("weather")[-1].strip()
        result = gweather(city)
        tool_message = Massage("weatherTool", result)
        memory.add(tool_message)
        return {
            "from": "weatherTool",
            "city": city.title(),
            "weather": result
        }
    
    reply = agent.respond(memory.get())
    reply_message = Massage(agent.name, reply)
    memory.add(reply_message)
    return {"response": reply}

@app.get("/history")
async def get_history():
    return {"history": [str(m) for m in memory.get()]}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}