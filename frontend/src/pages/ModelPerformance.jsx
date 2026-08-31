import { useCallback, useEffect, useState } from "react";
import { apiGet, extractFieldErrors } from "../api/client";
import { useToast } from "../components/Toast";
import Loader from "../components/Loader";

/* Renders the latest model training performance: metrics, confusion matrix,
   per-class metrics and training history. Data is refreshed each time the
   page loads and updates whenever a new model/dataset is trained. */

function MetricCard({ label, value, suffix = "%", hint, tone = "primary" }) {
  return (
    <div className={`metric-card metric-${tone}`}>
      <span className="metric-label">{label}</span>
      <span className="metric-value">
        {value}
        {suffix && <small>{suffix}</small>}
      </span>
      {hint && <span className="metric-hint">{hint}</span>}
    </div>
  );
}

function ConfusionMatrix({ matrix, labels }) {
  const [[tn, fp], [fn, tp]] = matrix;
  const total = tn + fp + fn + tp;
  const pct = (n) => (total ? ((n / total) * 100).toFixed(1) : "0.0");

  const cells = [
    { label: "True Positive", cls: "cm-tp", value: tp, y: "Malignant", x: "Malignant" },
    { label: "False Positive", cls: "cm-fp", value: fp, y: "Benign", x: "Malignant" },
    { label: "False Negative", cls: "cm-fn", value: fn, y: "Malignant", x: "Benign" },
    { label: "True Negative", cls: "cm-tn", value: tn, y: "Benign", x: "Benign" },
  ];

  return (
    <div className="cm-wrap">
      <div className="cm-axis">
        <span className="cm-axis-label">Actual →</span>
      </div>
      <table className="cm-table">
        <thead>
          <tr>
            <th />
            <th className="cm-col-label" colSpan={2}>
              Predicted
            </th>
          </tr>
          <tr>
            <th />
            {labels.map((l) => (
              <th key={l} className="cm-col-label">
                {l}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {[
            ["Benign"],
            ["Malignant"],
          ].map(([actual]) => (
            <tr key={actual}>
              <th className="cm-row-label">{actual}</th>
              {labels.map((_, ci) => {
                const cell = cells.find((c) => c.y === actual && c.x === labels[ci]);
                if (!cell) return <td key={ci} />;
                return (
                  <td key={ci} className={cell.cls}>
                    <span className="cm-cell-value">{cell.value}</span>
                    <span className="cm-cell-label">{cell.label}</span>
                    <span className="cm-cell-pct">{pct(cell.value)}%</span>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <p className="cm-total">Evaluated on {total} samples</p>
    </div>
  );
}

function HistoryChart({ history }) {
  if (!history || !history.accuracy?.length) return null;

  const renderLine = (key, color) => {
    const values = history[key] || [];
    if (!values.length) return null;
    const max = Math.max(...values, 1);
    return (
      <div className="chart-row">
        <span className="chart-key">{key}</span>
        <div className="bars">
          {values.map((v, i) => (
            <div
              key={i}
              className="bar"
              title={`epoch ${i + 1}: ${v.toFixed(3)}`}
              style={{ height: `${(v / max) * 100}%`, background: color }}
            />
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="chart">
      {renderLine("accuracy", "var(--primary)")}
      {renderLine("val_accuracy", "var(--secondary)")}
      {renderLine("loss", "var(--danger)")}
      {renderLine("val_loss", "#f59e0b")}
      <div className="chart-legend">
        <span><i style={{ background: "var(--primary)" }} /> accuracy</span>
        <span><i style={{ background: "var(--secondary)" }} /> val_accuracy</span>
        <span><i style={{ background: "var(--danger)" }} /> loss</span>
        <span><i style={{ background: "#f59e0b" }} /> val_loss</span>
      </div>
    </div>
  );
}

export default function ModelPerformance() {
  const notify = useToast();
  const [models, setModels] = useState([]);
  const [latest, setLatest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [list, current] = await Promise.all([
        apiGet("/models/"),
        apiGet("/models/latest/"),
      ]);
      setModels(list);
      setLatest(current);
    } catch (err) {
      const msg = extractFieldErrors(err)[0];
      setError(msg);
      notify(msg, "error");
    } finally {
      setLoading(false);
    }
  }, [notify]);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <Loader label="Loading model performance..." />;

  if (error && !latest) {
    return (
      <div className="page">
        <header className="page-header">
          <h1>Model Performance</h1>
        </header>
        <div className="empty-state">
          <span className="empty-icon">📊</span>
          <h3>No model data yet</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  const labels = latest?.class_labels?.length ? latest.class_labels : ["Benign", "Malignant"];
  const matrix =
    latest?.confusion_matrix && Array.isArray(latest.confusion_matrix[0])
      ? latest.confusion_matrix
      : [[0, 0], [0, 0]];

  return (
    <div className="page">
      <header className="page-header model-header">
        <div>
          <h1>Model Performance</h1>
          <p>
            Performance of the latest trained model. This page updates automatically after
            each new training run.
          </p>
        </div>
        {latest && (
          <div className="model-version">
            <span className="model-version-name">{latest.name}</span>
            <span className="model-version-tag">{latest.version}</span>
          </div>
        )}
      </header>

      <section className="metric-grid">
        <MetricCard label="Accuracy" value={latest.accuracy_pct} hint="Test accuracy" tone="primary" />
        <MetricCard label="Precision" value={latest.precision_pct} hint="Macro average" tone="secondary" />
        <MetricCard label="Recall" value={latest.recall_pct} hint="Macro average" tone="info" />
        <MetricCard label="F1 Score" value={latest.f1_pct} hint="Macro average" tone="success" />
        <MetricCard label="Loss" value={latest.loss} suffix="" hint={`VAL ${latest.val_loss}`} tone="danger" />
      </section>

      <div className="perf-grid">
        <section className="card">
          <h2 className="card-title">Confusion Matrix</h2>
          <ConfusionMatrix matrix={matrix} labels={labels} />
        </section>

        <section className="card">
          <h2 className="card-title">Per-Class Metrics</h2>
          <div className="table-wrap table-inset">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Class</th>
                  <th>Precision</th>
                  <th>Recall</th>
                  <th>F1</th>
                  <th>Samples</th>
                </tr>
              </thead>
              <tbody>
                {(latest.per_class_metrics || []).map((m, i) => (
                  <tr key={i}>
                    <td className="class-name">{m.class}</td>
                    <td>{(m.precision * 100).toFixed(2)}%</td>
                    <td>{(m.recall * 100).toFixed(2)}%</td>
                    <td>{(m.f1 * 100).toFixed(2)}%</td>
                    <td>{m.support}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>

      <div className="perf-grid">
        <section className="card">
          <h2 className="card-title">Training History</h2>
          <HistoryChart history={latest.history} />
        </section>

        <section className="card">
          <h2 className="card-title">Training Details</h2>
          <dl className="details-list">
            <div><dt>Model Name</dt><dd>{latest.name}</dd></div>
            <div><dt>Version</dt><dd>{latest.version}</dd></div>
            <div><dt>Dataset</dt><dd>{latest.dataset_name}</dd></div>
            <div><dt>Image Size</dt><dd>{latest.image_size}×{latest.image_size}</dd></div>
            <div><dt>Classes</dt><dd>{latest.classes}</dd></div>
            <div><dt>Batch Size</dt><dd>{latest.batch_size}</dd></div>
            <div><dt>Epochs</dt><dd>{latest.epochs_run} / {latest.epochs_total}</dd></div>
            <div><dt>Train / Val / Test</dt><dd>{latest.train_samples} / {latest.val_samples} / {latest.test_samples}</dd></div>
            <div><dt>Model File</dt><dd>{latest.model_file}</dd></div>
            <div><dt>Trained At</dt><dd>{latest.trained_at}</dd></div>
          </dl>
          {latest.notes && <p className="model-notes">{latest.notes}</p>}
        </section>
      </div>

      {models.length > 1 && (
        <section className="card">
          <h2 className="card-title">All Training Runs ({models.length})</h2>
          <div className="table-wrap table-inset">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Version</th>
                  <th>Model</th>
                  <th>Accuracy</th>
                  <th>Loss</th>
                  <th>Precision</th>
                  <th>Recall</th>
                  <th>F1</th>
                  <th>Trained At</th>
                </tr>
              </thead>
              <tbody>
                {models.map((m) => (
                  <tr key={m.id} className={m.id === latest?.id ? "row-current" : ""}>
                    <td className="class-name">{m.version}{m.id === latest?.id && <span className="badge-current">latest</span>}</td>
                    <td>{m.name}</td>
                    <td>{m.accuracy_pct}%</td>
                    <td>{m.loss}</td>
                    <td>{m.precision_pct}%</td>
                    <td>{m.recall_pct}%</td>
                    <td>{m.f1_pct}%</td>
                    <td>{m.trained_at}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </div>
  );
}
