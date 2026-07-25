import { useState } from "react";
import { FileUpload } from "./components/FileUpload";
import { ResultCard } from "./components/ResultCard";
import { ErrorBanner } from "./components/ErrorBanner";
import { usePrediction } from "./hooks/usePrediction";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { result, error, loading, runPrediction } = usePrediction();

  const handleDiagnose = () => {
    if (selectedFile) runPrediction(selectedFile);
  };

  return (
    <div className="app">
      <div className="eyebrow">Field Diagnostic Tool</div>
      <h1>Crop Disease Detector</h1>
      <p className="subtitle">
        Upload a photo of a leaf. Get a diagnosis and a treatment note, on the spot.
      </p>

      <FileUpload onFileSelect={setSelectedFile} disabled={loading} />

      <button onClick={handleDiagnose} disabled={!selectedFile || loading}>
        {loading ? "Diagnosing..." : "Run Diagnosis"}
      </button>

      {error && <ErrorBanner message={error} />}
      {result && <ResultCard result={result} />}
    </div>
  );
}

export default App;
