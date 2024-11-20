from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

# Mount static files for CSS and JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# OpenWeatherMap API details
API_KEY = "ENTER THE ACTUAL API KEY HERE"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Serve the UI."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/weather")
def get_weather(
    city: str = Query(None, description="City name to fetch weather for"),
    lat: float = Query(None, description="Latitude coordinate"),
    lon: float = Query(None, description="Longitude coordinate"),
):
    """Fetch weather data based on city name or latitude/longitude."""
    if not city and (lat is None or lon is None):
        raise HTTPException(status_code=400, detail="Provide either city or both lat and lon.")

    # Build query parameters for OpenWeatherMap
    if city:
        params = {"q": city, "appid": API_KEY, "units": "metric"}
    else:
        params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}

    response = requests.get(BASE_URL, params=params)

    # Handle API errors
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("message", "Error fetching weather"))

    weather_data = response.json()
    return {
        "city": weather_data.get("name", "Unknown"),
        "temperature": weather_data["main"]["temp"],
        "weather": weather_data["weather"][0]["description"],
        "humidity": weather_data["main"]["humidity"],
        "wind_speed": weather_data["wind"]["speed"],
    }
