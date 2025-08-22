package websocket

import "github.com/gorilla/websocket"

// Client represents a single WebSocket connection
type Client struct {
	Conn *websocket.Conn
	Pool *Pool
}

// Read listens for messages from the client
func (c *Client) Read() {
	defer func() {
		c.Pool.Unregister <- c
		c.Conn.Close()
	}()

	for {
		// We can read messages here if needed, but for now, we just keep the connection open
		if _, _, err := c.Conn.ReadMessage(); err != nil {
			// Connection closed by client
			break
		}
	}
}