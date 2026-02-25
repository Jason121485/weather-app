"""
Pytest tests for the Flask weather dashboard application.
Tests each route with GET and POST methods where applicable.
"""
import pytest
from unittest.mock import patch, Mock


class TestHomeRoute:
    """Tests for the home route (GET /)."""

    def test_get_home_returns_200(self, client):
        """GET / returns status 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_get_home_renders_index(self, client):
        """GET / renders the index template."""
        response = client.get("/")
        assert b"Weather" in response.data or b"weather" in response.data
        assert b"city" in response.data.lower() or b"search" in response.data.lower()

    def test_get_home_includes_search_form(self, client):
        """GET / includes the search form."""
        response = client.get("/")
        assert b'action="/weather"' in response.data or b'action=\"/weather\"' in response.data
        assert b'name="city"' in response.data


class TestWeatherRouteGet:
    """Tests for the weather lookup route (GET /weather)."""

    def test_get_weather_without_city_redirects_home(self, client):
        """GET /weather with no city query param redirects to home."""
        response = client.get("/weather")
        assert response.status_code == 302
        assert response.headers["Location"] in ("/", "http://localhost/")

    def test_get_weather_with_empty_city_redirects_home(self, client):
        """GET /weather?city=  redirects to home."""
        response = client.get("/weather?city=")
        assert response.status_code == 302
        assert "/" in response.headers["Location"]

    def test_get_weather_with_whitespace_only_redirects_home(self, client):
        """GET /weather?city=   redirects to home."""
        response = client.get("/weather?city=   ")
        assert response.status_code == 302
        assert "/" in response.headers["Location"]

    @patch("app.requests.get")
    def test_get_weather_with_city_success(self, mock_get, client):
        """GET /weather?city=London returns 200 with weather data when API succeeds."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "location": {"name": "London", "region": "City of London", "country": "United Kingdom"},
            "current": {
                "temp_c": 12,
                "temp_f": 53.6,
                "condition": {"text": "Partly cloudy", "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png"},
                "humidity": 75,
                "wind_kph": 15,
                "wind_dir": "SW",
                "pressure_mb": 1015,
                "cloud": 50,
                "uv": 4,
                "vis_km": 10,
                "gust_kph": 20,
                "feelslike_c": 10,
                "last_updated": "2024-01-15 12:00",
            },
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.get("/weather?city=London")

        assert response.status_code == 200
        assert b"London" in response.data
        assert b"12" in response.data
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]["params"]["q"] == "London"

    @patch("app.requests.get")
    def test_get_weather_api_error_shows_message(self, mock_get, client):
        """GET /weather shows error when API returns error payload."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"error": {"message": "City not found", "code": 1006}}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.get("/weather?city=InvalidCity123")

        assert response.status_code == 200
        assert b"City not found" in response.data or b"error" in response.data.lower()

    @patch("app.requests.get")
    def test_get_weather_network_error_shows_message(self, mock_get, client):
        """GET /weather shows error when API request fails."""
        import requests
        mock_get.side_effect = requests.RequestException("Connection failed")

        response = client.get("/weather?city=London")

        assert response.status_code == 200
        assert b"Network error" in response.data or b"try again" in response.data.lower()


class TestWeatherRoutePost:
    """Tests for the weather lookup route (POST /weather)."""

    def test_post_weather_without_city_shows_error(self, client):
        """POST /weather with no city returns index with error."""
        response = client.post("/weather", data={})
        assert response.status_code == 200
        assert b"Please enter a city name" in response.data

    def test_post_weather_with_empty_city_shows_error(self, client):
        """POST /weather with empty city string shows error."""
        response = client.post("/weather", data={"city": ""})
        assert response.status_code == 200
        assert b"Please enter a city name" in response.data

    def test_post_weather_with_whitespace_only_city_shows_error(self, client):
        """POST /weather with whitespace-only city shows error."""
        response = client.post("/weather", data={"city": "   "})
        assert response.status_code == 200
        assert b"Please enter a city name" in response.data

    @patch("app.requests.get")
    def test_post_weather_with_city_success(self, mock_get, client):
        """POST /weather with city form data returns 200 with weather when API succeeds."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "location": {"name": "Tokyo", "region": "Tokyo", "country": "Japan"},
            "current": {
                "temp_c": 18,
                "temp_f": 64.4,
                "condition": {"text": "Clear", "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png"},
                "humidity": 60,
                "wind_kph": 12,
                "wind_dir": "N",
                "pressure_mb": 1013,
                "cloud": 0,
                "uv": 6,
                "vis_km": 10,
                "gust_kph": 15,
                "feelslike_c": 17,
                "last_updated": "2024-01-15 14:00",
            },
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.post("/weather", data={"city": "Tokyo"})

        assert response.status_code == 200
        assert b"Tokyo" in response.data
        assert b"18" in response.data
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]["params"]["q"] == "Tokyo"

    @patch("app.requests.get")
    def test_post_weather_strips_whitespace(self, mock_get, client):
        """POST /weather trims leading/trailing whitespace from city."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "location": {"name": "Paris", "region": "Île-de-France", "country": "France"},
            "current": {
                "temp_c": 10,
                "temp_f": 50,
                "condition": {"text": "Cloudy", "icon": ""},
                "humidity": 70,
                "wind_kph": 12,
                "wind_dir": "NW",
                "pressure_mb": 1015,
                "cloud": 80,
                "uv": 2,
                "vis_km": 10,
                "gust_kph": 18,
                "feelslike_c": 9,
                "last_updated": "2024-01-15 12:00",
            },
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response = client.post("/weather", data={"city": "  Paris  "})

        assert response.status_code == 200
        call_args = mock_get.call_args
        assert call_args[1]["params"]["q"] == "Paris"
