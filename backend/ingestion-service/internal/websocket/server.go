package websocket

import (
    "log"
    "net/http"
    "time"

    "github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
    CheckOrigin: func(r *http.Request) bool {
        return true // Allow all origins in development
    },
}

func ServeWs(pool *Pool, w http.ResponseWriter, r *http.Request) {
    conn, err := upgrader.Upgrade(w, r, nil)
    if err != nil {
        log.Printf("WebSocket upgrade failed: %v", err)
        return
    }

    client := &Client{
        ID:   r.RemoteAddr,
        Conn: conn,
        Pool: pool,
    }

    pool.Register <- client

    go client.Read()
}

// Keepalive function to maintain connections
func Keepalive(pool *Pool) {
    ticker := time.NewTicker(30 * time.Second)
    defer ticker.Stop()

    for {
        <-ticker.C
        for client := range pool.Clients {
            if err := client.Conn.WriteMessage(websocket.PingMessage, nil); err != nil {
                client.Conn.Close()
                delete(pool.Clients, client)
            }
        }
    }
}