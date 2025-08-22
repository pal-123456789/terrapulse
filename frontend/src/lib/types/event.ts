export interface Event {
    id: string;
    title: string;
    description: string;
    category_id: string;
    geometry: string; // GeoJSON string
    acquired: string;
    updated: string;
    source_url: string;
    severity: string;
    confidence: number;
    category_name?: string;
    category_color?: string;
    category_icon?: string;
}

export interface Category {
    id: string;
    name: string;
    description: string;
    color: string;
    icon: string;
}

export interface EventFilters {
    category?: string;
    severity?: string;
    limit?: number;
}