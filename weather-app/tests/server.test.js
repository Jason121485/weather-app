/**
 * Jest + Supertest tests for the Express weather dashboard.
 */
const request = require('supertest');

let app;

beforeAll(() => {
  app = require('../server');
});

describe('Home Route', () => {
  test('GET / returns 200', async () => {
    const res = await request(app).get('/');
    expect(res.status).toBe(200);
  });

  test('GET / renders index with search form', async () => {
    const res = await request(app).get('/');
    expect(res.text).toMatch(/Weather|weather/);
    expect(res.text).toMatch(/city|search/i);
    expect(res.text).toMatch(/action="\/weather"/);
    expect(res.text).toMatch(/name="city"/);
  });
});

describe('Weather Route - GET', () => {
  test('GET /weather without city redirects to home', async () => {
    const res = await request(app).get('/weather');
    expect(res.status).toBe(302);
    expect(res.headers.location).toMatch(/\//);
  });

  test('GET /weather?city= redirects to home', async () => {
    const res = await request(app).get('/weather?city=');
    expect(res.status).toBe(302);
  });

  test('GET /weather?city=   (whitespace) redirects to home', async () => {
    const res = await request(app).get('/weather?city=%20%20%20');
    expect(res.status).toBe(302);
  });

  test('GET /weather?city=London returns 200 with weather when API succeeds', async () => {
    const axios = require('axios');
    jest.mock('axios');
    const mockGet = jest.spyOn(axios, 'get').mockResolvedValue({
      data: {
        location: { name: 'London', region: 'City of London', country: 'United Kingdom' },
        current: {
          temp_c: 12,
          temp_f: 53.6,
          condition: { text: 'Partly cloudy', icon: '//cdn.weatherapi.com/weather/64x64/day/116.png' },
          humidity: 75,
          wind_kph: 15,
          wind_dir: 'SW',
          pressure_mb: 1015,
          cloud: 50,
          uv: 4,
          vis_km: 10,
          gust_kph: 20,
          feelslike_c: 10,
          last_updated: '2024-01-15 12:00',
        },
      },
    });

    const res = await request(app).get('/weather?city=London');

    expect(res.status).toBe(200);
    expect(res.text).toContain('London');
    expect(res.text).toContain('12');
    expect(mockGet).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        params: expect.objectContaining({ q: 'London' }),
      })
    );

    mockGet.mockRestore();
  });

  test('GET /weather shows error when API returns error', async () => {
    const axios = require('axios');
    const mockGet = jest.spyOn(axios, 'get').mockResolvedValue({
      data: { error: { message: 'City not found', code: 1006 } },
    });

    const res = await request(app).get('/weather?city=InvalidCity123');

    expect(res.status).toBe(200);
    expect(res.text).toMatch(/City not found|error/i);

    mockGet.mockRestore();
  });

  test('GET /weather shows error on network failure', async () => {
    const axios = require('axios');
    const mockGet = jest.spyOn(axios, 'get').mockRejectedValue(new Error('Connection failed'));

    const res = await request(app).get('/weather?city=London');

    expect(res.status).toBe(200);
    expect(res.text).toMatch(/Network error|try again/i);

    mockGet.mockRestore();
  });
});

describe('Weather Route - POST', () => {
  test('POST /weather without city shows error', async () => {
    const res = await request(app).post('/weather').send({});
    expect(res.status).toBe(200);
    expect(res.text).toContain('Please enter a city name');
  });

  test('POST /weather with empty city shows error', async () => {
    const res = await request(app).post('/weather').send('city=');
    expect(res.status).toBe(200);
    expect(res.text).toContain('Please enter a city name');
  });

  test('POST /weather with whitespace-only city shows error', async () => {
    const res = await request(app).post('/weather').send('city=%20%20%20');
    expect(res.status).toBe(200);
    expect(res.text).toContain('Please enter a city name');
  });

  test('POST /weather with city returns 200 when API succeeds', async () => {
    const axios = require('axios');
    const mockGet = jest.spyOn(axios, 'get').mockResolvedValue({
      data: {
        location: { name: 'Tokyo', region: 'Tokyo', country: 'Japan' },
        current: {
          temp_c: 18,
          temp_f: 64.4,
          condition: { text: 'Clear', icon: '//cdn.weatherapi.com/weather/64x64/day/113.png' },
          humidity: 60,
          wind_kph: 12,
          wind_dir: 'N',
          pressure_mb: 1013,
          cloud: 0,
          uv: 6,
          vis_km: 10,
          gust_kph: 15,
          feelslike_c: 17,
          last_updated: '2024-01-15 14:00',
        },
      },
    });

    const res = await request(app).post('/weather').send('city=Tokyo');

    expect(res.status).toBe(200);
    expect(res.text).toContain('Tokyo');
    expect(res.text).toContain('18');
    expect(mockGet).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        params: expect.objectContaining({ q: 'Tokyo' }),
      })
    );

    mockGet.mockRestore();
  });

  test('POST /weather strips whitespace from city', async () => {
    const axios = require('axios');
    const mockGet = jest.spyOn(axios, 'get').mockResolvedValue({
      data: {
        location: { name: 'Paris', region: 'Île-de-France', country: 'France' },
        current: {
          temp_c: 10,
          temp_f: 50,
          condition: { text: 'Cloudy', icon: '' },
          humidity: 70,
          wind_kph: 12,
          wind_dir: 'NW',
          pressure_mb: 1015,
          cloud: 80,
          uv: 2,
          vis_km: 10,
          gust_kph: 18,
          feelslike_c: 9,
          last_updated: '2024-01-15 12:00',
        },
      },
    });

    const res = await request(app).post('/weather').send('city=  Paris  ');

    expect(res.status).toBe(200);
    expect(mockGet).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        params: expect.objectContaining({ q: 'Paris' }),
      })
    );

    mockGet.mockRestore();
  });
});

describe('Favicon', () => {
  test('GET /favicon.ico returns 204', async () => {
    const res = await request(app).get('/favicon.ico');
    expect(res.status).toBe(204);
  });
});
