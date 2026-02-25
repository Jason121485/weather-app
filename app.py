import os
import requests
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


# You can also override this via an environment variable
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "a31889c0ee9494b8ad43858252304")
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"


@app.route("/favicon.ico")
def favicon():
    """Serve favicon to avoid 404s in logs."""
    return "", 204


@app.route("/", methods=["GET"])
def home():
    """
    Home page with search form.
    """
    return render_template("index.html")


@app.route("/weather", methods=["GET", "POST"])
def weather_lookup():
    """
    Weather lookup endpoint. Accepts a city name via form POST or query string.
    """
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if not city:
            return render_template("index.html", error="Please enter a city name.")
    else:
        city = request.args.get("city", "").strip()
        if not city:
            # No city provided, redirect back home
            return redirect(url_for("home"))

    params = {
        "key": WEATHER_API_KEY,
        "q": city,
        "aqi": "yes",
    }

    weather_data = None
    error = None

    try:
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)
        response.raise_for_status()
        payload = response.json()

        if "error" in payload:
            error = payload["error"].get("message", "Unable to fetch weather right now.")
        else:
            weather_data = payload
    except requests.RequestException:
        error = "Network error while contacting WeatherAPI. Please try again."

    return render_template("weather.html", weather=weather_data, error=error, city=city)


if __name__ == "__main__":
    app.run(debug=True)

