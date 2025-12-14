import os
import requests
from datetime import datetime
from dotenv import load_dotenv


def load_api_key():
    """Load API key from .env file"""
    load_dotenv()
    api_key = os.getenv("OWM_API_KEY")
    if not api_key:
        raise ValueError("No API key found. Please set OWM_API_KEY in .env file.")
    return api_key


def get_units():
    """Prompt user for temperature units"""
    while True:
        choice = input("Choose units (C for Celsius, F for Fahrenheit): ").strip().upper()
        if choice == "C":
            return "metric", "°C"
        elif choice == "F":
            return "imperial", "°F"
        else:
            print("Invalid choice. Please enter C or F.")


def fetch_weather(city, api_key, units):
    """Fetch weather data from OpenWeatherMap API"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": units
    }

    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        raise ValueError("City not found.")
    if response.status_code == 401:
        raise ValueError("Invalid API key.")
    response.raise_for_status()

    return response.json()


def display_weather(data, unit_symbol):
    """Parse and display weather information"""
    city = data.get("name", "Unknown")
    country = data.get("sys", {}).get("country", "N/A")

    temp = data.get("main", {}).get("temp", "N/A")
    humidity = data.get("main", {}).get("humidity", "N/A")
    wind_speed = data.get("wind", {}).get("speed", "N/A")

    weather_desc = data.get("weather", [{}])[0].get("description", "N/A").title()

    sunrise = data.get("sys", {}).get("sunrise")
    sunset = data.get("sys", {}).get("sunset")

    if sunrise:
        sunrise = datetime.fromtimestamp(sunrise).strftime("%H:%M:%S")
    if sunset:
        sunset = datetime.fromtimestamp(sunset).strftime("%H:%M:%S")

    print("\n=== Current Weather ===")
    print(f"Location: {city}, {country}")
    print(f"Condition: {weather_desc}")
    print(f"Temperature: {temp} {unit_symbol}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed}")
    print(f"Sunrise: {sunrise}")
    print(f"Sunset: {sunset}")
    print("=======================\n")


def main():
    print("🌦️ Console Weather App (OpenWeatherMap)\n")

    try:
        api_key = load_api_key()
    except ValueError as e:
        print(f"❌ {e}")
        return

    while True:
        city = input("Enter a city name (or type 'exit' to quit): ").strip()
        if city.lower() == "exit":
            print("Goodbye!")
            break

        units, unit_symbol = get_units()

        try:
            weather_data = fetch_weather(city, api_key, units)
            display_weather(weather_data, unit_symbol)
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
