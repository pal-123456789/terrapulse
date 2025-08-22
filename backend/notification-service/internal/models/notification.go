package models

// Notification represents the structure of a notification message
type Notification struct {
	ID      string `json:"id"`
	EventID string `json:"eventId"`
	Type    string `json:"type"`    // e.g., "new_prediction", "event_update"
	Message string `json:"message"`
}