export interface PredictionResult {
  disease: string;
  confidence: number;
  treatment_tip: string;
}

export interface ApiError {
  detail: string;
}
