const API_URL = "http://127.0.0.1:8000/weather";

// Select elements
const cityInput = document.getElementById("city-input");
const searchBtn = document.getElementById("search-btn");
const weatherResult = document.getElementById("weather-result");
const cityNameElem = document.getElementById("city-name");
const temperatureElem = document.getElementById("temperature");
const weatherDescriptionElem = document.getElementById("weather-description");
const humidityElem = document.getElementById("humidity");
const windSpeedElem = document.getElementById("wind-speed");

// Fetch weather data
async function fetchWeather(city) {
    try {
        const response = await fetch(`${API_URL}?city=${city}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "City not found");
        }

        displayWeather(data);
    } catch (error) {
        alert(error.message);
        weatherResult.classList.add("hidden");
    }
}

// Display weather data
function displayWeather(data) {
    cityNameElem.textContent = `City: ${data.city}`;
    temperatureElem.textContent = `Temperature: ${data.temperature}°C`;
    weatherDescriptionElem.textContent = `Weather: ${data.weather}`;
    humidityElem.textContent = `Humidity: ${data.humidity}%`;
    windSpeedElem.textContent = `Wind Speed: ${data.wind_speed} m/s`;

    weatherResult.classList.remove("hidden");
}

// Add event listener to search button
searchBtn.addEventListener("click", () => {
    const city = cityInput.value.trim();
    if (city === "") {
        alert("Please enter a city name.");
        return;
    }
    fetchWeather(city);
});
