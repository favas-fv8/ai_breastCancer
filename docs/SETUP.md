# Local Setup Guide (Windows)

Step-by-step instructions to run the full stack on a Windows machine.

## 1. PostgreSQL

- Install PostgreSQL and ensure the service `postgresql-x64-18` is **Running**.
- Create the database (if not already present):

```powershell
$env:PGPASSWORD = "sql@321"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -h localhost -p 5432 -c "CREATE DATABASE ai_breastcancer_db;"
```

## 2. Backend

```powershell
cd backend

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item .env.example .env   # adjust values if needed
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

Verify the API: `http://localhost:8000/api/auth/login/`

## 3. Frontend

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Open `http://localhost:3000` and log in with the superuser you created.

## 4. Smoke test (optional)

```powershell
curl -X POST http://localhost:8000/api/auth/login/ `
  -H "Content-Type: application/json" `
  -d '{"username":"admin","password":"YOUR_PASSWORD"}'
```

Use the returned token to call the protected endpoints (predict, history).

## Troubleshooting

- **`ai_breastcancer_db` does not exist** → create it (step 1) and re-run
  `python manage.py migrate`.
- **CORS errors** → confirm the frontend origin (`http://localhost:3000`) is
  listed in `CORS_ALLOWED_ORIGINS` in `backend/.env`.
- **Model fails to load** → confirm `backend/ml/model/CancerNet_Model.h5`
  exists. If missing, copy the project-root `CancerNet_Model.h5` into it.
