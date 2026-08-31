import { useCallback, useEffect, useState } from "react";
import { apiGet, apiDelete, extractFieldErrors } from "../api/client";
import { useToast } from "../components/Toast";
import Loader from "../components/Loader";

export default function History() {
  const notify = useToast();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiGet("/history/");
      setItems(data.slice(0, 20));
    } catch (err) {
      setError(extractFieldErrors(err)[0]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this history record?")) return;
    setDeletingId(id);
    try {
      await apiDelete(`/history/${id}/`);
      setItems((prev) => prev.filter((i) => i.id !== id));
      notify("History record deleted.", "success");
    } catch (err) {
      notify(extractFieldErrors(err)[0], "error");
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="page">
      <header className="page-header">
        <h1>Prediction History</h1>
        <p>Review your latest 20 breast cancer detection analyses, newest first.</p>
      </header>

      {loading && <Loader label="Loading history..." />}

      {!loading && error && <div className="alert alert-error">{error}</div>}

      {!loading && !error && items.length === 0 && (
        <div className="empty-state">
          <span className="empty-icon">📋</span>
          <h3>No history yet</h3>
          <p>Run your first breast cancer detection to see results here.</p>
        </div>
      )}

      {!loading && items.length > 0 && (
        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Image</th>
                <th>Date</th>
                <th>Time</th>
                <th>Result</th>
                <th>Confidence</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item, index) => {
                const parts = item.created_at.split(" ");
                const date = parts[0] || item.created_at;
                const time = parts[1] || "";
                const malignant = item.result === "Malignant";
                return (
                  <tr key={item.id}>
                    <td className="row-number">{index + 1}</td>
                    <td>
                      <img
                        src={item.image}
                        alt="Histopathology"
                        className="thumb"
                        loading="lazy"
                      />
                    </td>
                    <td>{date}</td>
                    <td>{time}</td>
                    <td>
                      <span className={`pill${malignant ? " pill-malignant" : " pill-benign"}`}>
                        {item.result}
                      </span>
                    </td>
                    <td>{item.confidence}%</td>
                    <td>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={() => handleDelete(item.id)}
                        disabled={deletingId === item.id}
                      >
                        {deletingId === item.id ? "..." : "Delete"}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
