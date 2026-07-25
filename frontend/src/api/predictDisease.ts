import type { PredictionResult, ApiError } from "../types/prediction";

const API_URL = `${import.meta.env.VITE_API_URL}/predict`;

export async function predictDisease(file: File): Promise<PredictionResult> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(API_URL, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const err: ApiError = await response.json();
    throw new Error(err.detail || "Prediction failed");
  }

  return response.json();
}
