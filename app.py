# app.py - Complete single file application
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
import requests
import uuid
from datetime import datetime
import os

# All classes in one file
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

# HTML template as string (no external files needed)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🌤 MCP Weather Tool</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #f0f0f0;
            background: linear-gradient(135deg, #0c1445 0%, #1a1a2e 50%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem;
            margin: 0;
        }
        h1 {
            color: #00ffff;
            text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            text-align: center;
        }
        .container {
            background: rgba(30, 30, 30, 0.9);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 255, 255, 0.2);
            width: 100%;
            max-width: 400px;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        input[type="text"] {
            padding: 1rem;
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.1);
            color: #f0f0f0;
            font-size: 1.1rem;
            outline: none;
        }
        button {
            padding: 1rem;
            background: linear-gradient(45deg, #00ffff, #0080ff);
            color: #000;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            cursor: pointer;
        }
        .weather-box {
            margin-top: 2rem;
            padding: 2rem;
            border-radius: 15px;
            background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 128, 255, 0.1));
            border: 1px solid rgba(0, 255, 255, 0.2);
            text-align: center;
            font-size: 1.2rem;
        }
        .weather-box h3 {
            color: #00ffff;
            margin: 0 0 1rem 0;
            font-size: 1.5rem;
        }
    </style>
</head>
<body>
    <h1>🌦 MCP Weather Tool</h1>
    <div class="container">
        <form method="post">
            <input type="text" name="city" placeholder="Enter city name" required />
            <button type="submit">Get Weather ⛅</button>
        </form>
        {weather_result}
    </div>
</body>
</html>
"""

# Initialize FastAPI
app = FastAPI(title="MCP Weather Tool")

# Initialize components
memory = Memory()
agent = Agent()

@app.get("/", response_class=HTMLResponse)
async def form_get():
    return HTMLResponse(HTML_TEMPLATE.format(weather_result=""))

@app.post("/", response_class=HTMLResponse)
async def form_post(city: str = Form(...)):
    try:
        weather_result = gweather(city)
        
        # Add to memory
        user_message = Massage("User", f"weather {city}")
        weather_msg = Massage("weatherTool", weather_result)
        memory.add(user_message)
        memory.add(weather_msg)
        
        weather_html = f"""
        <div class="weather-box">
            <h3>📍 {city.title()}</h3>
            <div>{weather_result}</div>
        </div>
        """
        
        return HTMLResponse(HTML_TEMPLATE.format(weather_result=weather_html))
    except Exception as e:
        error_html = f"""<div class="weather-box"><h3>Error</h3><div>{str(e)}</div></div>"""
        return HTMLResponse(HTML_TEMPLATE.format(weather_result=error_html))

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/history")
async def get_history():
    return {"history": [str(m) for m in memory.get()]}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)