export interface PredictionResponse {
    prediction_id: string;
    event_id: string;
    model_type: string;
    forecast_hours: number;
    generated_at: string;
    confidence: number;
    result: any;
    metadata?: Record<string, any>;
}

export interface WildfirePredictionRequest {
    event_id: string;
    wind_speed: number;
    wind_direction: number;
    vegetation_density?: number;
    temperature?: number;
    humidity?: number;
    forecast_hours?: number;
}

export interface Event {
    id: string;
    title: string;
    category_id: string;
    // Add other properties as needed
}