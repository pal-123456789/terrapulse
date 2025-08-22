import { derived, writable } from 'svelte/store';
import type { Category, Event } from '../types/event'; // Note: Capital 'E' in Event

// Store for events - FIXED: Changed 'event[]' to 'Event[]'
export const events = writable<Event[]>([]);
export const loading = writable(false);
export const error = writable<string | null>(null);

// Derived store for events grouped by category
export const eventsByCategory = derived(events, $events => {
    const grouped: Record<string, Event[]> = {}; // FIXED: Changed 'Event)' to 'Event[]>'
    $events.forEach(event => {
        if (!grouped[event.category_id]) {
            grouped[event.category_id] = [];
        }
        grouped[event.category_id].push(event);
    });
    return grouped;
});

// Fetch events from API
export async function fetchEvents(filters: { category?: string; severity?: string; limit?: number } = {}) {
    loading.set(true);
    error.set(null);
    
    try {
        const params = new URLSearchParams();
        if (filters.category) params.append('category', filters.category);
        if (filters.severity) params.append('severity', filters.severity);
        if (filters.limit) params.append('limit', filters.limit.toString());
        
        const response = await fetch(`/api/ingestion/events?${params}`);
        
        if (!response.ok) {
            throw new Error(`Failed to fetch events: ${response.statusText}`);
        }
        
        const data = await response.json();
        events.set(data);
    } catch (err) {
        error.set((err as Error).message);
        console.error('Error fetching events:', err);
    } finally {
        loading.set(false);
    }
}

// Fetch event categories
export const categories = writable<Category[]>([]);

export async function fetchCategories() {
    try {
        const response = await fetch('/api/ingestion/events/categories');
        
        if (!response.ok) {
            throw new Error(`Failed to fetch categories: ${response.statusText}`);
        }
        
        const data = await response.json();
        categories.set(data);
    } catch (err) {
        console.error('Error fetching categories:', err);
    }
}