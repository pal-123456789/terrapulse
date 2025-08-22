import { writable } from 'svelte/store';

export const notifications = writable<any[]>([]);
export const isConnected = writable(false);

class WebSocketService {
    private socket: WebSocket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/api/notifications/ws`;
        
        try {
            this.socket = new WebSocket(wsUrl);
            
            this.socket.onopen = () => {
                console.log('WebSocket connected');
                isConnected.set(true);
                this.reconnectAttempts = 0;
                
                // Subscribe to notification categories
                this.subscribe(['wildfires', 'floods', 'severeStorms']);
            };
            
            this.socket.onmessage = (event) => {
                try {
                    const notification = JSON.parse(event.data);
                    notifications.update(notifs => [notification, ...notifs.slice(0, 49)]); // Keep last 50
                    
                    // Show browser notification if permitted
                    if (Notification.permission === 'granted') {
                        this.showBrowserNotification(notification);
                    }
                } catch (error) {
                    console.error('Error parsing notification:', error);
                }
            };
            
            this.socket.onclose = () => {
                console.log('WebSocket disconnected');
                isConnected.set(false);
                this.attemptReconnect();
            };
            
            this.socket.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
            this.attemptReconnect();
        }
    }
    
    subscribe(categories: string[]) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                action: 'subscribe',
                categories
            }));
        }
    }
    
    showBrowserNotification(notification: any) {
        const title = `TerraPulse Alert: ${notification.title}`;
        const options = {
            body: notification.message,
            icon: '/favicon.png',
            tag: notification.id,
            requireInteraction: notification.severity === 'critical',
            data: {
                eventId: notification.event_id,
                url: `/events/${notification.event_id}`
            }
        };
        
        new Notification(title, options).onclick = function(event) {
            window.focus();
            // @ts-ignore
            if (event.target && event.target.data && event.target.data.url) {
                // @ts-ignore
                window.location.href = event.target.data.url;
            }
        };
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.pow(2, this.reconnectAttempts) * 1000; // Exponential backoff
            
            console.log(`Attempting to reconnect in ${delay}ms...`);
            setTimeout(() => this.connect(), delay);
        }
    }
    
    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }
}

export const websocketService = new WebSocketService();