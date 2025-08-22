package websocket

import (
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

// Upgrader specifies parameters for upgrading an HTTP connection to a WebSocket connection.
var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	// Allow all origins for development purposes
	CheckOrigin: func(r *http.Request) bool { return true },
}

// Upgrade upgrades the HTTP server connection to the WebSocket protocol.
func Upgrade(w http.ResponseWriter, r *http.Request) (*websocket.Conn, error) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("ERROR: Failed to upgrade connection: %v", err)
		return nil, err
	}
	return conn, nil
}