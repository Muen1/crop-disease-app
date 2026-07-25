import type { PredictionResult } from "../types/prediction";

export function ResultCard({ result }: { result: PredictionResult }) {
  const isHealthy = result.disease.toLowerCase().includes("healthy");
  const confidencePct = (result.confidence * 100).toFixed(1);

  return (
    <div className="result">
      <div className="stamp">{confidencePct}%<br />CONF.</div>
      <div className="result-label">Diagnosis</div>
      <div className={`diagnosis ${isHealthy ? "healthy" : "disease"}`}>
        {result.disease.replace(/_/g, " ")}
      </div>
      <div className="tip-label">Recommended Action</div>
      <div className="tip-text">{result.treatment_tip}</div>
    </div>
  );
}
