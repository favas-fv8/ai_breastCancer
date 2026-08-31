const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

const TOKEN_KEY = "ai_bc_token";
const USER_KEY = "ai_bc_user";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setAuth(token, user) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function getUser() {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function setStoredUser(user) {
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

function authHeaders(json = true) {
  const headers = {};
  const token = getToken();
  if (token) headers.Authorization = `Token ${token}`;
  if (json) headers["Content-Type"] = "application/json";
  return headers;
}

export function isAuthenticated() {
  return Boolean(getToken());
}

export async function apiGet(url) {
  const res = await fetch(`${API_BASE_URL}${url}`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
}

export async function apiPost(url, body, formData = false) {
  const res = await fetch(`${API_BASE_URL}${url}`, {
    method: "POST",
    headers: formData ? authHeaders(false) : authHeaders(),
    body: formData ? body : JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function apiPatch(url, body) {
  const res = await fetch(`${API_BASE_URL}${url}`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify(body),
  });
  return handleResponse(res);
}

export async function apiDelete(url) {
  const res = await fetch(`${API_BASE_URL}${url}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  if (res.status === 204) {
    return { ok: true };
  }
  return handleResponse(res);
}

async function handleResponse(res) {
  const contentType = res.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await res.json() : await res.text();
  if (!res.ok) {
    const error = new Error(
      typeof data === "object" && data.detail ? data.detail : "Something went wrong."
    );
    error.status = res.status;
    error.data = data;
    throw error;
  }
  return data;
}

/** Convert backend field errors into a flat friendly list. */
export function extractFieldErrors(error) {
  if (!error || !error.data) return ["Request failed. Please try again."];
  const data = error.data;
  if (data.detail) return [data.detail];
  const errors = [];
  for (const value of Object.values(data)) {
    const messages = Array.isArray(value) ? value : [value];
    for (const msg of messages) {
      errors.push(String(msg));
    }
  }
  return errors.length ? errors : ["Request failed. Please try again."];
}
