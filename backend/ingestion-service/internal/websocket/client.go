package websocket

import (
    "encoding/json"
    "log"
    "sync"
    "time"

    "github.com/gorilla/websocket"
)

type Client struct {
    ID          string
    Conn        *websocket.Conn
    Pool        *Pool
    mu          sync.Mutex
    Subscriptions map[string]bool // Map of subscribed categories
}

type Pool struct {
    Register   chan *Client
    Unregister chan *Client
    Clients    map[*Client]bool
    Broadcast  chan []byte
}

func NewPool() *Pool {
    return &Pool{
        Register:   make(chan *Client),
        Unregister: make(chan *Client),
        Clients:    make(map[*Client]bool),
        Broadcast:  make(chan []byte),
    }
}

func (pool *Pool) Start() {
    for {
        select {
        case client := <-pool.Register:
            pool.Clients[client] = true
            log.Printf("Client %s registered. Size of connection pool: %d", client.ID, len(pool.Clients))
        case client := <-pool.Unregister:
            delete(pool.Clients, client)
            log.Printf("Client %s unregistered. Size of connection pool: %d", client.ID, len(pool.Clients))
        case message := <-pool.Broadcast:
            for client := range pool.Clients {
                if err := client.Conn.WriteMessage(websocket.TextMessage, message); err != nil {
                    log.Printf("WebSocket write error: %v", err)
                    client.Conn.Close()
                    delete(pool.Clients, client)
                }
            }
        }
    }
}

func (c *Client) Read() {
    defer func() {
        c.Pool.Unregister <- c
        c.Conn.Close()
    }()

    c.Conn.SetReadLimit(512)
    c.Conn.SetReadDeadline(time.Now().Add(60 * time.Second))
    c.Conn.SetPongHandler(func(string) error {
        c.Conn.SetReadDeadline(time.Now().Add(60 * time.Second))
        return nil
    })

    for {
        _, message, err := c.Conn.ReadMessage()
        if err != nil {
            if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
                log.Printf("WebSocket read error: %v", err)
            }
            break
        }

        // Handle subscription messages
        var sub struct {
            Action string   `json:"action"`
            Categories []string `json:"categories"`
        }
        
        if err := json.Unmarshal(message, &sub); err == nil && sub.Action == "subscribe" {
            c.mu.Lock()
            if c.Subscriptions == nil {
                c.Subscriptions = make(map[string]bool)
            }
            for _, category := range sub.Categories {
                c.Subscriptions[category] = true
            }
            c.mu.Unlock()
        }
    }
}

func (c *Client) ShouldReceive(category string) bool {
    c.mu.Lock()
    defer c.mu.Unlock()
    
    // If no specific subscriptions, receive all notifications
    if len(c.Subscriptions) == 0 {
        return true
    }
    
    return c.Subscriptions[category]
}