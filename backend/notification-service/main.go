package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"

	"terrapulse/backend/notification-service/internal/models"
	"terrapulse/backend/notification-service/internal/websocket"

	"github.com/redis/go-redis/v9"
)

func main() {
	// Create a new WebSocket pool and start it
	pool := websocket.NewPool()
	go pool.Start()

	// Connect to Redis and start listening for notifications
	go listenToRedis(pool)

	// --- Setup HTTP Server ---
	http.HandleFunc("/ws", func(w http.ResponseWriter, r *http.Request) {
		serveWs(pool, w, r)
	})

	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("Notification service is healthy"))
	})

	// Start the server
	log.Println("Notification service started on :8082")
	if err := http.ListenAndServe(":8082", nil); err != nil {
		log.Fatalf("FATAL: failed to start server: %v", err)
	}
}

// serveWs handles incoming WebSocket requests.
func serveWs(pool *websocket.Pool, w http.ResponseWriter, r *http.Request) {
	conn, err := websocket.Upgrade(w, r)
	if err != nil {
		log.Printf("ERROR: Failed to upgrade connection: %v", err)
		return
	}

	client := &websocket.Client{
		Conn: conn,
		Pool: pool,
	}

	pool.Register <- client
	client.Read()
}

// listenToRedis connects to Redis and broadcasts messages to the WebSocket pool.
func listenToRedis(pool *websocket.Pool) {
	redisURL := os.Getenv("REDIS_URL")
	if redisURL == "" {
		redisURL = "localhost:6379" // Default for local development
		log.Printf("WARN: REDIS_URL not set, defaulting to %s", redisURL)
	}

	redisClient := redis.NewClient(&redis.Options{
		Addr: redisURL,
	})

	ctx := context.Background()

	if _, err := redisClient.Ping(ctx).Result(); err != nil {
		log.Fatalf("FATAL: Could not connect to Redis: %v", err)
	}
	log.Println("Successfully connected to Redis.")

	pubsub := redisClient.Subscribe(ctx, "notifications")
	defer pubsub.Close()

	ch := pubsub.Channel()

	for msg := range ch {
		var notification models.Notification
		if err := json.Unmarshal([]byte(msg.Payload), &notification); err != nil {
			log.Printf("ERROR: Could not parse notification from Redis: %v", err)
			continue
		}

		message, err := json.Marshal(notification)
		if err != nil {
			log.Printf("ERROR: Could not marshal notification for broadcast: %v", err)
			continue
		}
		pool.Broadcast <- message
	}
}