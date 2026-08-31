# BreastAI — Frontend (React + Vite)

React single-page application for the BreastAI breast cancer detection system.
It consumes the Django REST API described in the project root README.

## Stack

- React 19
- Vite 8
- React Router 7
- Plain CSS design system (see `src/index.css`)

## Scripts

```bash
npm install      # install dependencies
npm run dev      # start dev server on http://localhost:3000
npm run build    # production build
npm run lint     # run Oxlint
npm run preview  # preview production build
```

## Env Configuration

Copy `.env.example` to `.env`:

```bash
Copy-Item .env.example .env
```

Set `VITE_API_BASE_URL` to the location of the Django API
(e.g. `http://localhost:8000/api`).

## Structure

```
src/
├── api/client.js          # API client (auth headers, error handling)
├── components/            # Navbar, Layout, Toast, Loader, ProtectedRoute
├── context/AuthContext.jsx# auth state + login/logout
└── pages/                 # Home, Login, Detect, History, Profile, About, NotFound
```
