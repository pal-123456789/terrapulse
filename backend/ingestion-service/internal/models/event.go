package models

import (
	"time"
)

type Event struct {
	ID          string    `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	CategoryID  string    `json:"category_id"`
	Latitude    float64   `json:"latitude"`
	Longitude   float64   `json:"longitude"`
	Geometry    string    `json:"geometry"` // GeoJSON string
	Acquired    time.Time `json:"acquired"`
	Updated     time.Time `json:"updated"`
	SourceURL   string    `json:"source_url"`
	Severity    string    `json:"severity"`
	Confidence  float64   `json:"confidence"`
	InsertedAt  time.Time `json:"inserted_at"`
}