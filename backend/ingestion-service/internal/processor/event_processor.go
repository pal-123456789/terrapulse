package processor

import (
	"database/sql"
	"log"
	"terrapulse/internal/nasa"
	"time"
)

// ProcessEONETEvents fetches and processes events from EONET
func ProcessEONETEvents(db *sql.DB) {
	events, err := nasa.FetchEONETEvents()
	if err != nil {
		log.Printf("Error fetching EONET events: %v", err)
		return
	}
	
	log.Printf("Processing %d events from EONET", len(events))
	
	for _, event := range events {
		// Skip closed events
		if event.Closed != nil {
			continue
		}
		
		// Determine category
		categoryID := "other"
		if len(event.Categories) > 0 {
			categoryID = event.Categories[0].ID
		}
		
		// Process each geometry for the event
		for _, geometry := range event.Geometry {
			eventTime, err := time.Parse(time.RFC3339, geometry.Date)
			if err != nil {
				log.Printf("Error parsing event time: %v", err)
				continue
			}
			
			// Convert coordinates to GeoJSON
			geoJSON, err := nasa.ConvertToGeoJSON(geometry.Type, geometry.Coordinates)
			if err != nil {
				log.Printf("Error converting coordinates to GeoJSON: %v", err)
				continue
			}
			
			// Get severity
			severity := nasa.GetSeverityFromEvent(event)
			
			// Insert or update event in database
			_, err = db.Exec(
				`INSERT INTO events (id, title, description, category_id, geometry, acquired, updated, source_url, severity) 
				 VALUES ($1, $2, $3, $4, ST_GeomFromGeoJSON($5), $6, $7, $8, $9)
				 ON CONFLICT (id) DO UPDATE SET 
				 title = EXCLUDED.title,
				 description = EXCLUDED.description,
				 category_id = EXCLUDED.category_id,
				 geometry = EXCLUDED.geometry,
				 acquired = EXCLUDED.acquired,
				 updated = EXCLUDED.updated,
				 source_url = EXCLUDED.source_url,
				 severity = EXCLUDED.severity`,
				event.ID,
				event.Title,
				event.Description,
				categoryID,
				geoJSON,
				eventTime,
				time.Now(),
				event.Link,
				severity,
			)
			
			if err != nil {
				log.Printf("Error inserting event %s: %v", event.ID, err)
				continue
			}
			
			// Insert sources
			for _, source := range event.Sources {
				_, err = db.Exec(
					`INSERT INTO event_sources (event_id, source_id, url)
					 VALUES ($1, $2, $3)
					 ON CONFLICT DO NOTHING`,
					event.ID,
					source.ID,
					source.URL,
				)
				
				if err != nil {
					log.Printf("Error inserting source for event %s: %v", event.ID, err)
				}
			}
		}
	}
	
	log.Printf("Finished processing EONET events")
}