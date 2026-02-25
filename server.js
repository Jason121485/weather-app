const express = require('express');
const path = require('path');
const axios = require('axios');
const expressLayouts = require('express-ejs-layouts');

const app = express();

const WEATHER_API_KEY = process.env.WEATHER_API_KEY || 'a31889c0ee9494b8ad43858252304';
const WEATHER_API_URL = 'http://api.weatherapi.com/v1/current.json';

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.set('layout', 'layouts/base');

app.use(expressLayouts);
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/favicon.ico', (req, res) => {
  res.status(204).send();
});

app.get('/', (req, res) => {
  res.render('index', { title: 'Weather Dashboard | Home' });
});

app.all('/weather', async (req, res) => {
  let city;

  if (req.method === 'POST') {
    city = (req.body.city || '').trim();
    if (!city) {
      return res.render('index', { title: 'Weather Dashboard | Home', error: 'Please enter a city name.' });
    }
  } else {
    city = (req.query.city || '').trim();
    if (!city) {
      return res.redirect('/');
    }
  }

  let weatherData = null;
  let error = null;

  try {
    const response = await axios.get(WEATHER_API_URL, {
      params: {
        key: WEATHER_API_KEY,
        q: city,
        aqi: 'yes',
      },
      timeout: 10000,
    });

    const payload = response.data;

    if (payload.error) {
      error = payload.error.message || 'Unable to fetch weather right now.';
    } else {
      weatherData = payload;
    }
  } catch (err) {
    if (axios.isAxiosError(err) && err.response?.data?.error) {
      error = err.response.data.error.message || 'Unable to fetch weather right now.';
    } else {
      error = 'Network error while contacting WeatherAPI. Please try again.';
    }
  }

  res.render('weather', {
    title: `Weather Dashboard | ${city || 'Result'}`,
    weather: weatherData,
    error,
    city,
  });
});

module.exports = app;

if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Weather Dashboard running at http://localhost:${PORT}`);
  });
}
