import fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from mcp_weather.weather import gweather
from mcp_weather.agent import Agent
from mcp_weather.memory import Memory
from mcp_weather.massage import Massage

templates = Jinja2Templates(directory="mcp_weather/templates")
app = fastapi.FastAPI()
memory= Memory()
agent = Agent()
print(dir(Memory))

@app.get("/", response_class=HTMLResponse)
def form_get(request: fastapi.Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.post("/",response_class=HTMLResponse)
def form_post(request: fastapi.Request):
    result = request.form()

@app.post("/message")
async def rmassage(request: fastapi.Request):
    datat = await request.json()
    content = datat["content"]
    Umasg = Massage("User",content)
    memory.add(Umasg)
    if content.lower().startswith("weather"):
        city = content.split("weather")[-1].strip()
        result = gweather(city)
        toolMassage = Massage("weatherTool", result)
        memory.add(toolMassage)
        return {"from": "weatherTool",
                "city": city.title(),
                "weather": result}
    reply = agent.respond(memory.get())
    replyMassage = Massage(agent.name, reply)
    memory.add(replyMassage)
    return {"response": reply}
    saveFile()

@app.get("/history")
async def Ghistory():
    return {"history": [str(m) for m in memory.get()]}

