import requests

def gweather(city:str)-> str:
    """ get the weather for a given city """
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
    
