import { writable } from 'svelte/store';
import type { PredictionResponse, WildfirePredictionRequest } from '../types/prediction';

export const predictions = writable<Record<string, PredictionResponse>>({});
export const loading = writable(false);
export const error = writable<string | null>(null);

export async function generatePrediction(request: WildfirePredictionRequest): Promise<PredictionResponse> {
    loading.set(true);
    error.set(null);
    
    try {
        const response = await fetch('/api/predict/wildfire', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request),
        });
        
        if (!response.ok) {
            throw new Error(`Prediction failed: ${response.statusText}`);
        }
        
        const prediction: PredictionResponse = await response.json();
        
        // Update store
        predictions.update(preds => ({
            ...preds,
            [prediction.prediction_id]: prediction
        }));
        
        return prediction;
    } catch (err) {
        const message = err instanceof Error ? err.message : 'An unknown error occurred';
        error.set(message);
        throw err;
    } finally {
        loading.set(false);
    }
}

export async function getPrediction(predictionId: string): Promise<PredictionResponse> {
    try {
        const response = await fetch(`/api/predictions/${predictionId}`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch prediction: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (err) {
        const message = err instanceof Error ? err.message : 'An unknown error occurred';
        error.set(message);
        throw err;
    }
}

export async function getEventPredictions(eventId: string): Promise<PredictionResponse[]> {
    try {
        const response = await fetch(`/api/events/${eventId}/predictions`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch event predictions: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (err) {
        const message = err instanceof Error ? err.message : 'An unknown error occurred';
        error.set(message);
        throw err;
    }
}