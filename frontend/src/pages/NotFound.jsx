import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="notfound">
      <h1>404</h1>
      <p>The page you are looking for does not exist.</p>
      <Link to="/" className="btn btn-primary">Go Home</Link>
    </div>
  );
}
