import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("weather")

def get_weather(city: str) -> dict:
    """
    Retrieves current weather for a given city using OpenWeather API.
    
    Args:
        city (str): Name of the city.
    
    Returns:
        dict: status and weather info or error message.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather = {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }
            return {"status": "success", "result": weather}
        else:
            return {"status": "error", "error": data.get("message", "Unknown error")}
    except Exception as e:
        return {"status": "error", "error": str(e)}
