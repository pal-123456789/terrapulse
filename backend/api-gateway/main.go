package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"github.com/gorilla/mux"
)

func main() {
	// Define upstream services from environment variables or defaults
	ingestionServiceURL := getEnv("INGESTION_SERVICE_URL", "http://ingestion-service:8081")
	inferenceServiceURL := getEnv("INFERENCE_SERVICE_URL", "http://inference-service:8000")

	// Create reverse proxies
	ingestionProxy := createReverseProxy(ingestionServiceURL)
	inferenceProxy := createReverseProxy(inferenceServiceURL)

	router := mux.NewRouter()

	// WebSocket proxy for notification service
	router.HandleFunc("/api/notifications/ws", func(w http.ResponseWriter, r *http.Request) {
        // Reverse proxy WebSocket connections to notification service
        notificationURL, _ := url.Parse("http://notification-service:8082")
        proxy := httputil.NewSingleHostReverseProxy(notificationURL)
        proxy.ServeHTTP(w, r)
    })

	// Route API requests to the appropriate service
	router.PathPrefix("/api/ingestion/").Handler(ingestionProxy)
	router.PathPrefix("/api/predict/").Handler(inferenceProxy)

	// Health endpoint
	router.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("API Gateway is OK"))
	}).Methods("GET")

	// CORS middleware
	corsMiddleware := func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			w.Header().Set("Access-Control-Allow-Origin", "*")
			w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
			w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
			
			if r.Method == "OPTIONS" {
				w.WriteHeader(http.StatusOK)
				return
			}
			
			next.ServeHTTP(w, r)
		})
	}

	// Add CORS middleware to all routes
	handler := corsMiddleware(router)

	log.Println("TerraPulse API Gateway started on :8080")
	log.Fatal(http.ListenAndServe(":8080", handler))
}

func createReverseProxy(target string) *httputil.ReverseProxy {
	url, _ := url.Parse(target)
	proxy := httputil.NewSingleHostReverseProxy(url)
	
	// Add error handling to the proxy
	proxy.ErrorHandler = func(w http.ResponseWriter, r *http.Request, err error) {
		log.Printf("Proxy error: %v", err)
		w.WriteHeader(http.StatusBadGateway)
		w.Write([]byte("Service temporarily unavailable"))
	}
	
	return proxy
}

func getEnv(key, fallback string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return fallback
}