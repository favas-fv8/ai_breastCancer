import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Home() {
  const { user } = useAuth();
  return (
    <div className="home">
      <section className="hero">
        <div className="hero-content">
          <span className="hero-eyebrow">AI · Deep Learning · Histopathology</span>
          <h1>Early Breast Cancer Detection<br />Powered by AI</h1>
          <p>
            BC-Ai uses a convolutional neural network (CancerNet) trained on the IDC
            breast histopathology dataset to classify tissue images as Benign or Malignant.
          </p>
          <div className="hero-actions">
            <Link to="/detect" className="btn btn-primary btn-lg">
              Start Detection
            </Link>
            <Link to="/about" className="btn btn-outline btn-lg">
              Learn More
            </Link>
          </div>
          {user && <p className="hero-greet">Welcome back, {user.username}!</p>}
        </div>
        <div className="hero-stats">
          <div className="stat">
            <span className="stat-value">2</span>
            <span className="stat-label">Classes</span>
          </div>
          <div className="stat">
            <span className="stat-value">50×50</span>
            <span className="stat-label">Image Size</span>
          </div>
          <div className="stat">
            <span className="stat-value">CNN</span>
            <span className="stat-label">CancerNet</span>
          </div>
        </div>
      </section>

      <section className="feature-grid">
        <div className="feature">
          <span className="feature-icon">🩺</span>
          <h3>AI Detection</h3>
          <p>Classify histopathology images with a validated deep learning model.</p>
        </div>
        <div className="feature">
          <span className="feature-icon">📊</span>
          <h3>Instant Results</h3>
          <p>Get confidence scores and clear Benign / Malignant predictions.</p>
        </div>
        <div className="feature">
          <span className="feature-icon">🗂️</span>
          <h3>History</h3>
          <p>All analyses are saved with date, time, result and image.</p>
        </div>
        <div className="feature">
          <span className="feature-icon">🔒</span>
          <h3>Secure</h3>
          <p>Token-based authentication and secure upload handling.</p>
        </div>
      </section>
    </div>
  );
}
