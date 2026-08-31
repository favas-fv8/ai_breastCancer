# BreastAI — AI-Powered Breast Cancer Histopathology Detection

A full-stack web application that uses a convolutional neural network
(**CancerNet**) to classify breast histopathology images as **Benign**
(non-cancerous) or **Malignant** (cancerous).

The deep learning model is trained on the IDC breast histopathology dataset
(50×50 image patches). Inference is served by a **Django REST API** and consumed
by a modern, responsive **React** single-page application backed by **PostgreSQL**.

---

## ✨ Features

- **Authentication** — single-user admin login/logout with token-based auth
- **Profile page** — view/edit account details
- **Change password** — validated, securely hashed
- **AI Detection** — upload a histopathology image and run the CancerNet model
  - Live image preview (drag-and-drop + click to upload)
  - Clear **Benign / Malignant** result with confidence score
  - Friendly loading states and notifications
- **History page** — date, time, result, image and delete, persisted in PostgreSQL
- **About page** — project background, methodology and technology stack
- **Professional UI** — modern dashboard/navigation, fully responsive, reusable components
- **Security** — env-based secrets, secure file upload validation, per-user data scoping

---

## 🧱 Tech Stack

| Layer      | Technology                                                        |
| ---------- | ----------------------------------------------------------------- |
| Backend    | Python · Django · Django REST Framework · TensorFlow / Keras       |
| Frontend   | React · Vite · React Router                                        |
| Database   | PostgreSQL                                                         |
| ML Model   | CancerNet CNN (`.h5`)                                              |

---

## 📁 Project Structure

```
ai_breastCancer/
├── backend/                  # Django REST API
│   ├── config/               # Django project settings/urls
│   ├── accounts/             # authentication app (login, profile, password)
│   ├── predictions/          # detection + history app
│   ├── ml/                   # ML inference service
│   │   ├── predictor.py      # loads model, preprocesses, predicts
│   │   └── model/            # CancerNet_Model.h5
│   ├── requirements.txt
│   ├── .env.example
│   └── manage.py
├── frontend/                 # React single-page app
│   ├── src/
│   │   ├── api/              # API client + error handling
│   │   ├── components/       # Navbar, Layout, Toast, Loader, ProtectedRoute
│   │   ├── context/          # AuthContext
│   │   └── pages/            # Home, Login, Detect, History, Profile, About
│   ├── .env.example
│   └── package.json
├── ml/                       # Original ML training script
│   └── cancer_detection.py
├── docs/                     # documentation
├── CancerNet_Model.h5        # source model weights
└── README.md
```

> The raw dataset (`IDC_regular_ps50_idx5/`, ~1.5 GB) and `archive.zip` are kept
> **local-only** and excluded from version control. See `.gitignore`.

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.12
- Node.js 18+
- PostgreSQL (running locally)

### 2. Database

Ensure PostgreSQL is running on `localhost:5432` and that the database
`ai_breastcancer_db` exists. Credentials are read from environment variables.

### 3. Backend setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate         # Windows
# source venv/bin/activate      # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
Copy-Item .env.example .env     # then edit values as needed

# Apply migrations (creates tables in PostgreSQL)
python manage.py migrate

# Create the admin user
python manage.py createsuperuser

# Start the API server
python manage.py runserver 8000
```

The API is served at `http://localhost:8000/api/`.

### 4. Frontend setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
Copy-Item .env.example .env

# Start the development server
npm run dev
```

The app is served at `http://localhost:3000`.

---

## 🔐 API Endpoints

All endpoints (except `login`) require an `Authorization: Token <token>` header.

| Method | Endpoint                        | Description                    |
| ------ | ------------------------------- | ------------------------------ |
| POST   | `/api/auth/login/`              | Authenticate, get token        |
| POST   | `/api/auth/logout/`             | Invalidate token               |
| GET    | `/api/auth/profile/`            | Get current user profile       |
| PATCH  | `/api/auth/profile/update/`     | Update profile                 |
| POST   | `/api/auth/password/change/`    | Change password                |
| POST   | `/api/predict/`                 | Upload image, run model        |
| GET    | `/api/history/`                 | List my predictions            |
| GET    | `/api/history/<id>/`            | Retrieve a prediction          |
| DELETE | `/api/history/<id>/`            | Delete a prediction            |

---

## 🧠 The Model

`CancerNet` is a sequential CNN with three convolutional blocks
(32 → 64 → 128 filters), max pooling, dropout and a sigmoid output head. Inputs
are 50×50 RGB patches; outputs are probabilities where **≥0.5 = Malignant** and
**<0.5 = Benign**. The training pipeline is documented in
[`ml/cancer_detection.py`](ml/cancer_detection.py).

## ⚠️ Disclaimer

This project is for **research and educational purposes only**. It is not a
medical device and does not provide a clinical diagnosis. Always consult a
qualified healthcare professional for medical decisions.

---

## 🗂️ Version Control

```bash
git init
git add .
git commit -m "Build full-stack breast cancer detection app (Django + React + PostgreSQL)"
git branch -M main
git remote add origin https://github.com/favas-fv8/ai_breastCancer.git
git push -u origin main
```
