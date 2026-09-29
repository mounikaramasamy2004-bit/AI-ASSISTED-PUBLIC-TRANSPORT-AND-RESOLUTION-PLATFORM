# AI Assisted Public Transport and Resolution Platform

A full-stack student project: transport search, live vehicle tracking, complaint
management with AI classification, delay prediction, route recommendation, a chatbot,
and an admin panel.

The project is split into two independent parts:

| Part | Folder | Runs on | Tech |
|------|--------|---------|------|
| Backend (REST API) | `backend/` | http://127.0.0.1:5000 | Python, Flask, SQLAlchemy, SQLite, JWT, scikit-learn |
| Frontend (website) | `frontend/` | http://127.0.0.1:5500 | HTML, CSS, JavaScript, Bootstrap 5, Leaflet, Chart.js |

## 1. Run the backend

```bash
cd backend
python -m venv venv
# Windows:   venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The first start creates the SQLite database (`transport.db`), loads seed data and trains
the delay model (about 10-20 seconds). Check it at http://127.0.0.1:5000/api/health

- Run the tests: `python -m pytest -q` (26 tests)
- Reset the data: `python database/seed.py --reset`

## 2. Run the frontend

Open a second terminal:

```bash
cd frontend
python -m http.server 5500
```

Then open http://127.0.0.1:5500 in the browser.

## 3. How the frontend connects to the backend

Only one setting connects them: `API_BASE` in `frontend/js/api.js`.

```js
const API_BASE = localStorage.getItem("api_base") || "http://127.0.0.1:5000/api";
```

- Every page calls the backend with `fetch()` through the `api()` helper in that file.
- After login the JWT token is kept in `localStorage` and sent as `Authorization: Bearer <token>`.
- The backend allows the frontend through CORS (`CORS_ORIGINS` in `backend/config.py`).
- If the backend is on another host or port, edit `API_BASE`, or run this in the browser
  console: `localStorage.setItem("api_base", "http://<host>:<port>/api")`
- If the frontend is served from another port, add that origin to `CORS_ORIGINS`.

## Default logins

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@transport.com | Admin@123 |
| User | arun@example.com | User@123 |

Other seeded users use the same `User@123` password. To register as an admin yourself,
use the invite code `ADMIN-2026`.

## Features

- Register / login with JWT and role-based access (USER / ADMIN)
- Route search between places with an AI-ranked best route
- Live vehicle tracking on a Leaflet map (GPS is simulated)
- AI delay prediction (Random Forest)
- Complaint submission with automatic category and priority
- Chatbot: vehicle location, routes, delays, complaint status
- Notifications
- Admin: dashboard, analytics charts, vehicle / route / user management,
  complaint assignment and resolution, CSV reports

## AI / ML

- **Delay prediction** (`backend/ai/delay_prediction.py`): RandomForestRegressor trained on a
  synthetic dataset (`backend/data/sample_transport_data.csv`, 900 rows). R2 about 0.89.
- **Route optimization** (`backend/ai/route_optimization.py`): weighted score over travel time,
  delay, fare, stops, traffic and distance.
- **Complaint classifier** (`backend/ai/complaint_classifier.py`): TF-IDF + Logistic Regression
  with keyword rules for 8 categories, plus a priority heuristic.

## Folder structure

```
AI-Public-Transport-Platform/
  backend/   app.py config.py requirements.txt
             database/ models/ routes/ services/ ai/ data/ tests/
  frontend/  *.html  css/  js/
```

## API summary

`/api/auth/*`, `/api/users/*`, `/api/vehicles`, `/api/tracking/vehicles`, `/api/routes`,
`/api/routes/search`, `/api/complaints`, `/api/notifications`, `/api/chatbot/message`,
`/api/ai/predict-delay`, `/api/ai/recommend-route`, `/api/ai/classify-complaint`,
`/api/admin/dashboard`, `/api/admin/analytics`, `/api/health`.

## Troubleshooting

- **"Failed to fetch":** the backend is not running, or `API_BASE` is wrong.
- **CORS error in the console:** add your frontend origin to `CORS_ORIGINS` in `backend/config.py`.
- **Map is blank:** Leaflet and its tiles load from the internet, so check the connection.
- **Port 5000 in use (macOS):** change the port in `app.py` and in `API_BASE`.
- **Login loops back:** clear the browser's localStorage and log in again.

## Future enhancements

Real GPS device integration, SMS/email alerts, PostgreSQL, a mobile app, and a
model trained on real transport data.
