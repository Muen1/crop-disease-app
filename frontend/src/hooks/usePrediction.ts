import { useState, useCallback } from "react";
import { predictDisease } from "../api/predictDisease";
import type { PredictionResult } from "../types/prediction";

interface UsePredictionState {
  result: PredictionResult | null;
  error: string | null;
  loading: boolean;
}

export function usePrediction() {
  const [state, setState] = useState<UsePredictionState>({
    result: null,
    error: null,
    loading: false,
  });

  const runPrediction = useCallback(async (file: File) => {
    setState({ result: null, error: null, loading: true });
    try {
      const result = await predictDisease(file);
      setState({ result, error: null, loading: false });
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unknown error";
      setState({ result: null, error: message, loading: false });
    }
  }, []);

  const reset = useCallback(() => {
    setState({ result: null, error: null, loading: false });
  }, []);

  return { ...state, runPrediction, reset };
}
