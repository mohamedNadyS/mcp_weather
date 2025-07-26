import fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from weather import gweather
from agent import Agent
from memory import Memory
from massage import Massage

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

