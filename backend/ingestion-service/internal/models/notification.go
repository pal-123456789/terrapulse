package models

import "time"

type Notification struct {
    ID          string    `json:"id"`
    UserID      string    `json:"user_id,omitempty"` // For targeted notifications
    Type        string    `json:"type"`              // alert, prediction, info
    Category    string    `json:"category"`          // wildfire, flood, etc.
    Title       string    `json:"title"`
    Message     string    `json:"message"`
    Severity    string    `json:"severity"`          // info, warning, critical
    EventID     string    `json:"event_id,omitempty"`
    Coordinates []float64 `json:"coordinates,omitempty"` // [lon, lat]
    CreatedAt   time.Time `json:"created_at"`
    Read        bool      `json:"read"`
}

type Subscription struct {
    UserID      string   `json:"user_id"`
    Categories  []string `json:"categories"`
    Severities  []string `json:"severities"`
    Coordinates []float64 `json:"coordinates,omitempty"` // For location-based alerts
    Radius      float64  `json:"radius,omitempty"`       // In kilometers
}