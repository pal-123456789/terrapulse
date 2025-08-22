<script lang="ts">
    import { notifications } from '$lib/services/websocket';
    import { fade } from 'svelte/transition';
    
    let expanded = false;
    
    function clearAll() {
        notifications.set([]);
    }
    
    function markAsRead(id: string) {
        notifications.update(notifs => 
            notifs.map(notif => 
                notif.id === id ? { ...notif, read: true } : notif
            )
        );
    }
</script>

<div class="notification-center">
    <button 
        class="notification-toggle"
        on:click={() => expanded = !expanded}
        class:has-unread={$notifications.some(n => !n.read)}
        aria-label="Notifications"
        aria-expanded={expanded}
    >
        🔔
        {#if $notifications.filter(n => !n.read).length > 0}
            <span class="badge">{$notifications.filter(n => !n.read).length}</span>
        {/if}
    </button>
    
    {#if expanded}
        <div class="notification-panel" transition:fade role="dialog" aria-label="Notifications panel">
            <div class="panel-header">
                <h3>Notifications</h3>
                <button on:click={clearAll} class="clear-btn" aria-label="Clear all notifications">Clear All</button>
            </div>
            
            <div class="notification-list">
                {#if $notifications.length === 0}
                    <div class="empty-state">No notifications</div>
                {:else}
                    {#each $notifications as notification (notification.id)}
                        <div 
                            class="notification-item {notification.severity} {notification.read ? 'read' : 'unread'}"
                            on:click={() => markAsRead(notification.id)}
                            role="button"
                            tabindex="0"
                            aria-label={`Notification: ${notification.title}. ${notification.message}. Click to mark as read.`}
                            on:keypress={(e) => e.key === 'Enter' || e.key === ' ' ? markAsRead(notification.id) : null}
                        >
                            <div class="notification-icon">
                                {#if notification.category === 'wildfires'}🔥
                                {:else if notification.category === 'floods'}🌊
                                {:else if notification.category === 'severeStorms'}🌀
                                {:else}🌍
                                {/if}
                            </div>
                            <div class="notification-content">
                                <div class="notification-title">{notification.title}</div>
                                <div class="notification-message">{notification.message}</div>
                                <div class="notification-time">
                                    {new Date(notification.created_at).toLocaleTimeString()}
                                </div>
                            </div>
                            {#if !notification.read}
                                <div class="unread-indicator" aria-hidden="true"></div>
                            {/if}
                        </div>
                    {/each}
                {/if}
            </div>
        </div>
    {/if}
</div>

<style>
    .notification-center {
        position: relative;
        display: inline-block;
    }
    
    .notification-toggle {
        position: relative;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .notification-toggle:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    .notification-toggle.has-unread {
        box-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
    }
    
    .badge {
        position: absolute;
        top: -5px;
        right: -5px;
        background: #ff6b6b;
        color: white;
        border-radius: 50%;
        width: 18px;
        height: 18px;
        font-size: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .notification-panel {
        position: absolute;
        top: 50px;
        right: 0;
        width: 350px;
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        overflow: hidden;
    }
    
    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .panel-header h3 {
        margin: 0;
        font-size: 16px;
    }
    
    .clear-btn {
        background: transparent;
        border: none;
        color: #8b5cf6;
        cursor: pointer;
        font-size: 12px;
    }
    
    .notification-list {
        max-height: 400px;
        overflow-y: auto;
    }
    
    .empty-state {
        padding: 20px;
        text-align: center;
        color: rgba(255, 255, 255, 0.5);
    }
    
    .notification-item {
        display: flex;
        padding: 12px 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        cursor: pointer;
        transition: background 0.2s ease;
        position: relative;
    }
    
    .notification-item:hover {
        background: rgba(255, 255, 255, 0.05);
    }
    
    .notification-item.unread {
        background: rgba(99, 102, 241, 0.05);
    }
    
    .notification-item.critical {
        background: rgba(239, 68, 68, 0.1);
    }
    
    .notification-item.critical:hover {
        background: rgba(239, 68, 68, 0.15);
    }
    
    .notification-icon {
        font-size: 20px;
        margin-right: 12px;
        flex-shrink: 0;
    }
    
    .notification-content {
        flex: 1;
        min-width: 0;
    }
    
    .notification-title {
        font-weight: 600;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .notification-message {
        font-size: 13px;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 4px;
        line-height: 1.4;
    }
    
    .notification-time {
        font-size: 11px;
        color: rgba(255, 255, 255, 0.4);
    }
    
    .unread-indicator {
        width: 8px;
        height: 8px;
        background: #8b5cf6;
        border-radius: 50%;
        margin-left: 10px;
        flex-shrink: 0;
        align-self: center;
    }
</style>