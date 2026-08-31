import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../components/Toast";
import { apiPatch, apiPost, extractFieldErrors } from "../api/client";
import { ButtonSpinner } from "../components/Loader";

export default function Profile() {
  const { user, updateUser } = useAuth();
  const notify = useToast();
  const navigate = useNavigate();
  const [tab, setTab] = useState("info");

  const [profileForm, setProfileForm] = useState({
    first_name: user?.first_name || "",
    last_name: user?.last_name || "",
    email: user?.email || "",
  });
  const [profileErrors, setProfileErrors] = useState([]);
  const [savingProfile, setSavingProfile] = useState(false);

  const [passForm, setPassForm] = useState({
    old_password: "",
    new_password: "",
    confirm_password: "",
  });
  const [passFieldErrors, setPassFieldErrors] = useState({});
  const [passErrors, setPassErrors] = useState([]);
  const [savingPass, setSavingPass] = useState(false);

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileForm((f) => ({ ...f, [name]: value }));
    setProfileErrors([]);
  };

  const saveProfile = async (e) => {
    e.preventDefault();
    setSavingProfile(true);
    setProfileErrors([]);
    try {
      const data = await apiPatch("/auth/profile/update/", profileForm);
      updateUser(data);
      notify("Profile updated.", "success");
    } catch (err) {
      setProfileErrors(extractFieldErrors(err));
    } finally {
      setSavingProfile(false);
    }
  };

  const handlePassChange = (e) => {
    const { name, value } = e.target;
    setPassForm((f) => ({ ...f, [name]: value }));
    setPassFieldErrors((er) => ({ ...er, [name]: "" }));
    setPassErrors([]);
  };

  const validatePass = () => {
    const next = {};
    if (!passForm.old_password) next.old_password = "Current password is required.";
    if (!passForm.new_password) next.new_password = "New password is required.";
    else if (passForm.new_password.length < 8)
      next.new_password = "New password must be at least 8 characters.";
    if (!passForm.confirm_password) next.confirm_password = "Please confirm the new password.";
    else if (passForm.new_password !== passForm.confirm_password)
      next.confirm_password = "Passwords do not match.";
    setPassFieldErrors(next);
    return Object.keys(next).length === 0;
  };

  const changePassword = async (e) => {
    e.preventDefault();
    if (!validatePass()) return;
    setSavingPass(true);
    setPassErrors([]);
    try {
      await apiPost("/auth/password/change/", passForm);
      notify("Password changed. Please log in again.", "success");
      setPassForm({ old_password: "", new_password: "", confirm_password: "" });
      navigate("/login");
    } catch (err) {
      setPassErrors(extractFieldErrors(err));
    } finally {
      setSavingPass(false);
    }
  };

  return (
    <div className="page page-narrow">
      <header className="page-header">
        <h1>My Profile</h1>
        <p>Manage your account information and security.</p>
      </header>

      <div className="profile-card">
        <div className="profile-head">
          <span className="avatar avatar-lg">{user?.username?.[0]?.toUpperCase() || "A"}</span>
          <div>
            <h2>{user?.username}</h2>
            <p className="muted">{user?.email}</p>
          </div>
        </div>

        <div className="tabs">
          <button
            className={`tab${tab === "info" ? " tab-active" : ""}`}
            onClick={() => setTab("info")}
          >
            Account Info
          </button>
          <button
            className={`tab${tab === "security" ? " tab-active" : ""}`}
            onClick={() => setTab("security")}
          >
            Change Password
          </button>
        </div>

        {tab === "info" && (
          <form onSubmit={saveProfile} className="tab-panel">
            {profileErrors.length > 0 && (
              <div className="alert alert-error">
                {profileErrors.map((msg, i) => (
                  <div key={i}>{msg}</div>
                ))}
              </div>
            )}
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="first_name">First Name</label>
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  value={profileForm.first_name}
                  onChange={handleProfileChange}
                />
              </div>
              <div className="form-group">
                <label htmlFor="last_name">Last Name</label>
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  value={profileForm.last_name}
                  onChange={handleProfileChange}
                />
              </div>
            </div>
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={profileForm.email}
                onChange={handleProfileChange}
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={savingProfile}>
              {savingProfile ? <ButtonSpinner /> : "Save Changes"}
            </button>
          </form>
        )}

        {tab === "security" && (
          <form onSubmit={changePassword} className="tab-panel" noValidate>
            {passErrors.length > 0 && (
              <div className="alert alert-error">
                {passErrors.map((msg, i) => (
                  <div key={i}>{msg}</div>
                ))}
              </div>
            )}
            <div className="form-group">
              <label htmlFor="old_password">Current Password</label>
              <input
                id="old_password"
                name="old_password"
                type="password"
                autoComplete="current-password"
                value={passForm.old_password}
                onChange={handlePassChange}
                className={passFieldErrors.old_password ? "input-error" : ""}
              />
              {passFieldErrors.old_password && (
                <span className="field-error">{passFieldErrors.old_password}</span>
              )}
            </div>
            <div className="form-group">
              <label htmlFor="new_password">New Password</label>
              <input
                id="new_password"
                name="new_password"
                type="password"
                autoComplete="new-password"
                value={passForm.new_password}
                onChange={handlePassChange}
                className={passFieldErrors.new_password ? "input-error" : ""}
              />
              {passFieldErrors.new_password && (
                <span className="field-error">{passFieldErrors.new_password}</span>
              )}
            </div>
            <div className="form-group">
              <label htmlFor="confirm_password">Confirm New Password</label>
              <input
                id="confirm_password"
                name="confirm_password"
                type="password"
                autoComplete="new-password"
                value={passForm.confirm_password}
                onChange={handlePassChange}
                className={passFieldErrors.confirm_password ? "input-error" : ""}
              />
              {passFieldErrors.confirm_password && (
                <span className="field-error">{passFieldErrors.confirm_password}</span>
              )}
            </div>
            <button type="submit" className="btn btn-primary" disabled={savingPass}>
              {savingPass ? <ButtonSpinner /> : "Change Password"}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
