import { useRef, useState } from "react";
import { apiPost, extractFieldErrors } from "../api/client";
import { useToast } from "../components/Toast";
import { ButtonSpinner } from "../components/Loader";

const MAX_SIZE = 5 * 1024 * 1024; // 5 MB

export default function Detect() {
  const notify = useToast();
  const fileInputRef = useRef(null);

  const [preview, setPreview] = useState(null);
  const [fileName, setFileName] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const [busy, setBusy] = useState(false);
  const [fieldErrors, setFieldErrors] = useState([]);
  const [result, setResult] = useState(null);

  const resetResult = () => {
    setResult(null);
    setFieldErrors([]);
  };

  const acceptFile = (file) => {
    if (!file) return;
    resetResult();
    const allowed = ["image/png", "image/jpeg", "image/jpg", "image/bmp", "image/webp"];
    if (!allowed.includes(file.type)) {
      setFieldErrors(["Unsupported file type. Please upload a PNG, JPG, BMP or WEBP image."]);
      return;
    }
    if (file.size > MAX_SIZE) {
      setFieldErrors(["Image size must not exceed 5 MB."]);
      return;
    }
    setFileName(file.name);
    setPreview(URL.createObjectURL(file));
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    acceptFile(e.dataTransfer.files?.[0]);
  };

  const onSelect = (e) => {
    acceptFile(e.target.files?.[0]);
  };

  const handleSubmit = async () => {
    if (!preview) {
      setFieldErrors(["Please select an image to analyze."]);
      return;
    }
    setBusy(true);
    setFieldErrors([]);
    setResult(null);
    const fd = new FormData();
    fd.append("image", fileInputRef.current.files[0]);
    try {
      const data = await apiPost("/predict/", fd, true);
      setResult(data);
      notify("Prediction completed.", "success");
    } catch (err) {
      setFieldErrors(extractFieldErrors(err));
    } finally {
      setBusy(false);
    }
  };

  const malignant = result?.result === "Malignant";

  return (
    <div className="page">
      <header className="page-header">
        <h1>AI Breast Cancer Detection</h1>
        <p>
          Upload a histopathology image and our deep learning model will classify it as
          Benign or Malignant.
        </p>
      </header>

      <div className="detect-grid">
        <section className="card">
          <h2 className="card-title">Upload Image</h2>

          <div
            className={`dropzone${dragOver ? " dropzone-over" : ""}${preview ? " dropzone-filled" : ""}`}
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={onDrop}
            onClick={() => fileInputRef.current?.click()}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") fileInputRef.current?.click();
            }}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="image/png,image/jpeg,image/bmp,image/webp"
              onChange={onSelect}
              hidden
            />
            {preview ? (
              <img src={preview} alt="Uploaded preview" className="dropzone-preview" />
            ) : (
              <div className="dropzone-empty">
                <span className="dropzone-icon">☁️</span>
                <p>
                  <strong>Click to upload</strong> or drag and drop
                </p>
                <p className="muted">PNG, JPG, BMP or WEBP · max 5 MB</p>
              </div>
            )}
          </div>

          {fileName && <p className="file-name">{fileName}</p>}

          {fieldErrors.length > 0 && (
            <div className="alert alert-error">
              {fieldErrors.map((msg, i) => (
                <div key={i}>{msg}</div>
              ))}
            </div>
          )}

          <button
            className="btn btn-primary btn-block"
            onClick={handleSubmit}
            disabled={busy || !preview}
          >
            {busy ? <ButtonSpinner /> : "🔬 Run Analysis"}
          </button>
        </section>

        <section className="card">
          <h2 className="card-title">Prediction Result</h2>

          {busy && (
            <div className="result-placeholder">
              <span className="spinner" />
              <p>Analyzing image with CancerNet model...</p>
            </div>
          )}

          {!busy && !result && (
            <div className="result-placeholder">
              <span className="result-icon">🩺</span>
              <p>No prediction yet. Upload an image and run the analysis.</p>
            </div>
          )}

          {!busy && result && (
            <div className={`result-card${malignant ? " result-malignant" : " result-benign"}`}>
              <div className="result-badge">
                {malignant ? "⚠️ Malignant" : "✅ Benign"}
              </div>
              <p className="result-desc">
                {malignant
                  ? "Cancerous cells detected. Please consult a medical professional."
                  : "Non-cancerous cells detected. No malignant indicators found."}
              </p>
              <div className="result-metric-row">
                <div className="result-metric">
                  <span className="result-metric-label">Confidence</span>
                  <span className="result-metric-value">{result.confidence}%</span>
                </div>
              </div>
              <div className="confidence-bar">
                <div
                  className={`confidence-fill${malignant ? " fill-malignant" : " fill-benign"}`}
                  style={{ width: `${Math.min(100, result.confidence)}%` }}
                />
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
