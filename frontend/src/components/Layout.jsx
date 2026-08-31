import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

export default function Layout() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="main-content">
        <Outlet />
      </main>
      <footer className="app-footer">
        <p>© {new Date().getFullYear()} BreastAI · AI-powered breast cancer detection</p>
      </footer>
    </div>
  );
}
