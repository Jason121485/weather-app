# Weather Dashboard

A modern web application for real-time weather lookups using [WeatherAPI.com](https://www.weatherapi.com/). Features a responsive glassmorphism UI with blue and gold accents.

**Available in two implementations:**
- **JavaScript** (Node.js + Express) – default
- **Python** (Flask) – see `app.py` and `requirements.txt`

---

## Tech Stack (JavaScript)

| Component | Technology |
|-----------|------------|
| Backend | Express.js |
| HTTP Client | Axios |
| Templating | EJS + express-ejs-layouts |
| Styling | Vanilla CSS (glassmorphism, gradients) |
| Icons | Font Awesome 6 |
| Testing | Jest + Supertest |

---

## Project Structure (JavaScript)

```
├── server.js              # Express application entry point
├── package.json
├── jest.config.js
├── public/
│   └── css/
│       └── style.css      # Application styles
├── views/
│   ├── layouts/
│   │   └── base.ejs       # Layout template
│   ├── index.ejs          # Home page (search form)
│   └── weather.ejs        # Weather results page
└── tests/
    ├── server.test.js     # Jest + Supertest tests
    └── conftest.py        # (Python pytest - legacy)
```

---

## Features

- **Home page** – Search form for city lookups
- **Weather results** – Current conditions, temperature, humidity, wind, pressure, cloud cover, UV index, visibility, and air quality
- **Responsive layout** – Mobile-friendly design
- **Error handling** – API errors and network failures surfaced to the user
- **GET and POST support** – Weather lookup via form submission or query string

---

## Routes

### `GET /`

Home page with search form.

```javascript
app.get('/', (req, res) => {
  res.render('index', { title: 'Weather Dashboard | Home' });
});
```

### `GET /weather?city=<name>`

Look up weather by city. Redirects to `/` if `city` is missing or empty.

### `POST /weather`

Look up weather via form data (`city` field). Returns index with error if city is empty.

### `GET /favicon.ico`

Returns 204 No Content.

---

## Setup (JavaScript)

### 1. Install dependencies

```bash
npm install
```

### 2. Configure API key (optional)

```bash
# Windows PowerShell
$env:WEATHER_API_KEY = "your_api_key_here"

# macOS / Linux
export WEATHER_API_KEY="your_api_key_here"
```

### 3. Run the application

```bash
npm start
```

Or:

```bash
node server.js
```

Open [http://localhost:3000/](http://localhost:3000/) in your browser.

---

## Testing (JavaScript)

```bash
npm test
```

Tests use Jest and Supertest. External WeatherAPI calls are mocked.

---

## Setup (Python – legacy)

```bash
pip install -r requirements.txt
set FLASK_APP=app.py
flask run
```

Or `python app.py`. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

---

## License & Credits

- Weather data provided by [WeatherAPI.com](https://www.weatherapi.com/)
- Icons by [Font Awesome](https://fontawesome.com/)
