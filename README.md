# 🌦 MCP Weather Tool

A simple and elegant weather application built with FastAPI that provides real-time weather information for any city worldwide.

![Weather App Preview](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🌍 **Global Weather Data** - Get weather information for any city worldwide
- 🎨 **Modern UI** - Beautiful gradient design with cyan/blue theme
- 📱 **Responsive Design** - Works perfectly on desktop and mobile devices
- 💾 **History Tracking** - Keeps track of all weather requests
- 🚀 **Fast & Lightweight** - Built with FastAPI for optimal performance
- 🔌 **REST API** - JSON endpoints for programmatic access

## 🌐 Live Demo

**[View Live Application](https://mcpweather-production.up.railway.app)**

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohamedNadyS/mcp_weather.git
   cd mcp_weather
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn mcp_weather.server:app --reload
   ```

4. **Open your browser:**
   ```
   http://localhost:8000
   ```

### Using Docker

1. **Build the image:**
   ```bash
   docker build -t mcp-weather .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 mcp-weather
   ```

## 🔧 API Endpoints

### Web Interface
- `GET /` - Main weather application interface
- `POST /` - Submit weather request via form

### REST API
- `GET /health` - Health check endpoint
- `GET /history` - Get request history
- `POST /message` - Send message to weather agent

### Example API Usage

```bash
# Get weather via API
curl -X POST "http://localhost:8000/message" \
     -H "Content-Type: application/json" \
     -d '{"content": "weather London"}'
```

Response:
```json
{
  "from": "weatherTool",
  "city": "London",
  "weather": "London: ⛅️  +8°C"
}
```

## 🌡️ Weather Data

Weather information is provided by [wttr.in](https://wttr.in/), a simple weather service that provides:
- Current temperature
- Weather conditions with emojis
- Location-based data
- No API key required

## 📖 Usage Examples

### Web Interface
1. Open the application in your browser
2. Enter a city name (e.g., "Cairo", "New York", "Tokyo")
3. Click "Get Weather ⛅"
4. View the current weather information

### API Integration
```python
import requests

# Get weather for a city
response = requests.post("http://localhost:8000/message", 
                        json={"content": "weather Paris"})
weather_data = response.json()
print(f"Weather in {weather_data['city']}: {weather_data['weather']}")
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Mohamed Nady**
- GitHub: [@mohamedNadyS](https://github.com/mohamedNadyS)
- Project Link: [https://github.com/mohamedNadyS/mcp_weather](https://github.com/mohamedNadyS/mcp_weather)

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [wttr.in](https://wttr.in/) - Weather data provider
- [Railway](https://railway.app/) - Deployment platform
- [Uvicorn](https://www.uvicorn.org/) - ASGI server

---

**⭐ If you found this project helpful, please give it a star!**

Made with ❤️ using FastAPI and Python