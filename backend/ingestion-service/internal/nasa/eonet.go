package nasa

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strconv"
	"time"
)

// EONETEvent represents the structure of events from NASA's EONET API
type EONETEvent struct {
	ID          string    `json:"id"`
	Title       string    `json:"title"`
	Description string    `json:"description"`
	Link        string    `json:"link"`
	Categories  []struct {
		ID string `json:"id"`
	} `json:"categories"`
	Geometry []struct {
		Date        string      `json:"date"`
		Type        string      `json:"type"`
		Coordinates interface{} `json:"coordinates"` // Can be []float64 or [][][]float64
	} `json:"geometry"`
	Sources []struct {
		ID  string `json:"id"`
		URL string `json:"url"`
	} `json:"sources"`
	Closed *string `json:"closed"` // Events can be closed
}

// EONETResponse represents the full response from the EONET API
type EONETResponse struct {
	Title       string       `json:"title"`
	Description string       `json:"description"`
	Link        string       `json:"link"`
	Events      []EONETEvent `json:"events"`
}

// FetchEONETEvents retrieves recent events from NASA's EONET API
func FetchEONETEvents() ([]EONETEvent, error) {
	client := &http.Client{Timeout: 30 * time.Second}
	
	// Get events from the last 7 days, limit to 50 results
	url := "https://eonet.gsfc.nasa.gov/api/v3/events?limit=50&days=7"
	
	resp, err := client.Get(url)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch EONET data: %v", err)
	}
	defer resp.Body.Close()
	
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("EONET API returned non-200 status: %d", resp.StatusCode)
	}
	
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("failed to read EONET response: %v", err)
	}
	
	var eonetResponse EONETResponse
	err = json.Unmarshal(body, &eonetResponse)
	if err != nil {
		return nil, fmt.Errorf("failed to parse EONET JSON: %v", err)
	}
	
	return eonetResponse.Events, nil
}

// Convert coordinates to GeoJSON based on geometry type
func ConvertToGeoJSON(geometryType string, coordinates interface{}) (string, error) {
	switch geometryType {
	case "Point":
		if coords, ok := coordinates.([]interface{}); ok {
			point := map[string]interface{}{
				"type":        "Point",
				"coordinates": []float64{coords[0].(float64), coords[1].(float64)},
			}
			geoJSON, err := json.Marshal(point)
			return string(geoJSON), err
		}
	case "Polygon":
		if coords, ok := coordinates.([]interface{}); ok {
			polygon := map[string]interface{}{
				"type":        "Polygon",
				"coordinates": coords,
			}
			geoJSON, err := json.Marshal(polygon)
			return string(geoJSON), err
		}
	}
	
	return "", fmt.Errorf("unsupported geometry type or coordinate format: %s", geometryType)
}

// GetSeverityFromEvent estimates severity based on event properties
func GetSeverityFromEvent(event EONETEvent) string {
	// Simple heuristic - in a real implementation, this would be more sophisticated
	if event.Closed != nil {
		return "low"
	}
	
	// Check if it's a recent event (last 24 hours)
	for _, geometry := range event.Geometry {
		if eventTime, err := time.Parse(time.RFC3339, geometry.Date); err == nil {
			if time.Since(eventTime) < 24*time.Hour {
				return "high"
			}
		}
	}
	
	return "medium"
}