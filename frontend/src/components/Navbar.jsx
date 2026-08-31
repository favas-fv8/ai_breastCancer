import { useState } from "react";
import { NavLink, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "./Toast";

export default function Navbar() {
  const { user, logout } = useAuth();
  const notify = useToast();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);

  const navItems = [
    { to: "/detect", label: "Detection" },
    { to: "/history", label: "History" },
    { to: "/about", label: "About" },
  ];

  const handleLogout = async () => {
    setBusy(true);
    await logout();
    setBusy(false);
    setOpen(false);
    notify("Logged out successfully.", "success");
    navigate("/login");
  };

  const linkClass = ({ isActive }) =>
    `nav-link${isActive ? " nav-link-active" : ""}`;

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="brand" onClick={() => setOpen(false)}>
          <span className="brand-logo">✦</span>
          <span className="brand-text">
            <span className="brand-title">BC-Ai</span>
            <span className="brand-sub">Cancer Detection</span>
          </span>
        </Link>

        <nav className={`nav-menu${open ? " nav-menu-open" : ""}`}>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={linkClass}
              onClick={() => setOpen(false)}
            >
              {item.label}
            </NavLink>
          ))}
          <div className="nav-user-zone">
            <Link to="/profile" className="nav-user" onClick={() => setOpen(false)}>
              <span className="avatar">{user?.username?.[0]?.toUpperCase() || "A"}</span>
              <span className="nav-user-name">{user?.username}</span>
            </Link>
            <button
              className="btn btn-ghost btn-sm"
              onClick={handleLogout}
              disabled={busy}
            >
              {busy ? "..." : "Logout"}
            </button>
          </div>
        </nav>

        <button
          className="hamburger"
          aria-label="Toggle menu"
          aria-expanded={open}
          onClick={() => setOpen((v) => !v)}
        >
          <span className={`hamburger-line${open ? " hamburger-open" : ""}`} />
          <span className={`hamburger-line${open ? " hamburger-open" : ""}`} />
          <span className={`hamburger-line${open ? " hamburger-open" : ""}`} />
        </button>
      </div>
    </header>
  );
}
