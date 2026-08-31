import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../components/Toast";
import { extractFieldErrors } from "../api/client";
import { ButtonSpinner } from "../components/Loader";

export default function Login() {
  const { login } = useAuth();
  const notify = useToast();
  const navigate = useNavigate();

  const [form, setForm] = useState({ username: "", password: "" });
  const [errors, setErrors] = useState({});
  const [fieldErrors, setFieldErrors] = useState([]);
  const [busy, setBusy] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
    setErrors((er) => ({ ...er, [name]: "" }));
    setFieldErrors([]);
  };

  const validate = () => {
    const next = {};
    if (!form.username.trim()) next.username = "Username is required.";
    if (!form.password) next.password = "Password is required.";
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    setBusy(true);
    setFieldErrors([]);
    try {
      await login(form.username, form.password);
      notify("Welcome back!", "success");
      navigate("/detect");
    } catch (err) {
      setFieldErrors(extractFieldErrors(err));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-brand">
          <span className="auth-logo">✦</span>
          <h1>BC-Ai</h1>
          <p>AI-Powered Breast Cancer Histopathology Detection</p>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          {fieldErrors.length > 0 && (
            <div className="alert alert-error">
              {fieldErrors.map((msg, i) => (
                <div key={i}>{msg}</div>
              ))}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              name="username"
              type="text"
              autoComplete="username"
              placeholder="Enter your username"
              value={form.username}
              onChange={handleChange}
              className={errors.username ? "input-error" : ""}
            />
            {errors.username && <span className="field-error">{errors.username}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              placeholder="Enter your password"
              value={form.password}
              onChange={handleChange}
              className={errors.password ? "input-error" : ""}
            />
            {errors.password && <span className="field-error">{errors.password}</span>}
          </div>

          <button type="submit" className="btn btn-primary btn-block" disabled={busy}>
            {busy ? <ButtonSpinner /> : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}
