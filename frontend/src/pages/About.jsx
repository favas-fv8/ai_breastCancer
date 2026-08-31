export default function About() {
  return (
    <div className="page about-page">
      <header className="page-header">
        <h1>About This Project</h1>
      </header>

      <section className="card">
        <h2 className="card-title">Overview</h2>
        <p>
          BreastAI is a full-stack web application that leverages a custom-built deep
          learning model to assist in the detection of Invasive Ductal Carcinoma (IDC) —
          the most common type of breast cancer — from histopathology tissue images.
        </p>
        <p>
          The model, styled <strong>CancerNet</strong>, is a convolutional neural network
          (CNN) trained on the <em>IDC_regular_ps50_idx5</em> dataset containing 50×50
          pixel patches extracted from digitized breast tissue samples. Each image is
          classified into one of two categories:
        </p>
        <ul className="check-list">
          <li><strong>Benign</strong> — No invasive ductal carcinoma present (Non-cancerous)</li>
          <li><strong>Malignant</strong> — Invasive ductal carcinoma present (Cancerous)</li>
        </ul>
      </section>

      <section className="card">
        <h2 className="card-title">How It Works</h2>
        <ol className="steps">
          <li>You upload a histopathology image (PNG, JPG, BMP or WEBP).</li>
          <li>The image is resized to 50×50 and normalized to [0, 1].</li>
          <li>The CancerNet model produces a probability score.</li>
          <li>The result is classified as Benign or Malignant with a confidence score.</li>
          <li>The prediction is saved to your history for future reference.</li>
        </ol>
      </section>

      <section className="card">
        <h2 className="card-title">Technology Stack</h2>
        <ul className="tech-list">
          <li><strong>Backend:</strong> Python · Django · Django REST Framework · TensorFlow / Keras</li>
          <li><strong>Frontend:</strong> React · Vite · React Router</li>
          <li><strong>Database:</strong> PostgreSQL</li>
          <li><strong>ML Model:</strong> CancerNet CNN (.h5)</li>
        </ul>
      </section>

      <section className="card">
        <h2 className="card-title">Disclaimer</h2>
        <p className="disclaimer">
          This application is intended for research and educational purposes only. It is
          not a medical device and does not provide a clinical diagnosis. Always consult a
          qualified healthcare professional for any medical decision.
        </p>
      </section>
    </div>
  );
}
