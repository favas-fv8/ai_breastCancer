export default function Loader({ label = "Loading..." }) {
  return (
    <div className="loader-wrap" role="status" aria-live="polite">
      <div className="spinner" />
      <span className="loader-label">{label}</span>
    </div>
  );
}

export function ButtonSpinner() {
  return <span className="spinner spinner-sm" />;
}
