class VotingNotificationSystem {
    constructor() {
        this.notifications = [];
        this.settings = {
            voting_alarms: true,
            ending_reminders: true,
            sound_enabled: true,
            popup_enabled: true,
        };
        this.checkInterval = null;
        this.audioContext = null;
        this.init();
    }

    async init() {
        // Initialize audio context for sound notifications
        if (window.AudioContext || window.webkitAudioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }

        // Load notification settings
        await this.loadSettings();
        
        // Start checking for notifications
        this.startNotificationCheck();
        
        // Request notification permission
        this.requestNotificationPermission();
    }

    async loadSettings() {
        try {
            const response = await fetch('/voting/api/notification-settings/');
            if (response.ok) {
                const settings = await response.json();
                this.settings = { ...this.settings, ...settings };
            }
        } catch (error) {
            console.error('Error loading notification settings:', error);
        }
    }

    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    console.log('Notification permission granted');
                }
            });
        }
    }

    startNotificationCheck() {
        // Check for notifications every 30 seconds
        this.checkInterval = setInterval(() => {
            this.checkNotifications();
        }, 30000);

        // Initial check
        this.checkNotifications();
    }

    async checkNotifications() {
        try {
            const response = await fetch('/voting/api/notifications/');
            if (response.ok) {
                const data = await response.json();
                const newNotifications = data.notifications.filter(n => 
                    !this.notifications.some(existing => existing.id === n.id)
                );

                if (newNotifications.length > 0) {
                    this.notifications = [...data.notifications, ...this.notifications];
                    this.showNotifications(newNotifications);
                    this.updateNotificationBadge(data.unread_count);
                }
            }
        } catch (error) {
            console.error('Error checking notifications:', error);
        }
    }

    showNotifications(notifications) {
        notifications.forEach(notification => {
            if (this.settings.popup_enabled) {
                this.showPopup(notification);
            }
            
            if (this.settings.sound_enabled) {
                this.playAlarmSound(notification.type);
            }

            // Show browser notification if permission granted
            if ('Notification' in window && Notification.permission === 'granted') {
                this.showBrowserNotification(notification);
            }
        });
    }

    showPopup(notification) {
        // Create popup element
        const popup = document.createElement('div');
        popup.className = 'voting-notification-popup';
        popup.innerHTML = `
            <div class="notification-content">
                <div class="notification-header">
                    <span class="notification-title">${this.escapeHtml(notification.title)}</span>
                    <button class="notification-close" onclick="this.closest('.voting-notification-popup').remove()">×</button>
                </div>
                <div class="notification-message">${this.escapeHtml(notification.message)}</div>
                ${notification.poll_id ? `
                    <div class="notification-actions">
                        <button class="btn btn-sm btn-primary" onclick="window.location.href='/voting/poll/${notification.poll_id}/'">
                            View Poll
                        </button>
                        <button class="btn btn-sm btn-secondary" onclick="votingNotifications.markAsRead(${notification.id})">
                            Dismiss
                        </button>
                    </div>
                ` : ''}
            </div>
        `;

        // Add styles
        popup.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            max-width: 400px;
            animation: slideIn 0.3s ease-out;
        `;

        // Add CSS animation
        if (!document.getElementById('notification-styles')) {
            const style = document.createElement('style');
            style.id = 'notification-styles';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                .voting-notification-popup .notification-content {
                    padding: 16px;
                }
                .voting-notification-popup .notification-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 8px;
                }
                .voting-notification-popup .notification-title {
                    font-weight: 600;
                    color: #333;
                }
                .voting-notification-popup .notification-close {
                    background: none;
                    border: none;
                    font-size: 18px;
                    cursor: pointer;
                    color: #999;
                }
                .voting-notification-popup .notification-message {
                    color: #666;
                    margin-bottom: 12px;
                }
                .voting-notification-popup .notification-actions {
                    display: flex;
                    gap: 8px;
                }
            `;
            document.head.appendChild(style);
        }

        document.body.appendChild(popup);

        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (popup.parentNode) {
                popup.remove();
            }
        }, 10000);
    }

    showBrowserNotification(notification) {
        const browserNotification = new Notification(notification.title, {
            body: notification.message,
            icon: '/static/images/vote-icon.png',
            tag: `voting-${notification.id}`,
        });

        browserNotification.onclick = function() {
            if (notification.poll_id) {
                window.location.href = `/voting/poll/${notification.poll_id}/`;
            }
            browserNotification.close();
        };

        // Auto-close after 5 seconds
        setTimeout(() => {
            browserNotification.close();
        }, 5000);
    }

    playAlarmSound(type) {
        if (!this.audioContext) return;

        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);

        // Different sounds for different notification types
        switch (type) {
            case 'voting_alarm':
                // Voting alarm - urgent sound
                oscillator.frequency.setValueAtTime(880, this.audioContext.currentTime); // A5
                oscillator.frequency.setValueAtTime(1046, this.audioContext.currentTime + 0.1); // C6
                gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.5);
                oscillator.start(this.audioContext.currentTime);
                oscillator.stop(this.audioContext.currentTime + 0.5);
                break;

            case 'ending_reminder':
                // Ending reminder - gentle chime
                oscillator.frequency.setValueAtTime(523, this.audioContext.currentTime); // C5
                oscillator.frequency.setValueAtTime(659, this.audioContext.currentTime + 0.1); // E5
                oscillator.frequency.setValueAtTime(784, this.audioContext.currentTime + 0.2); // G5
                gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.8);
                oscillator.start(this.audioContext.currentTime);
                oscillator.stop(this.audioContext.currentTime + 0.8);
                break;

            default:
                // Default notification sound
                oscillator.frequency.setValueAtTime(600, this.audioContext.currentTime);
                gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime);
                gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.3);
                oscillator.start(this.audioContext.currentTime);
                oscillator.stop(this.audioContext.currentTime + 0.3);
        }
    }

    updateNotificationBadge(count) {
        // Update notification badge in navigation
        let badge = document.querySelector('.notification-badge');
        if (!badge) {
            const navLink = document.querySelector('a[href*="dashboard"]');
            if (navLink) {
                badge = document.createElement('span');
                badge.className = 'notification-badge';
                badge.style.cssText = `
                    background: #dc2626;
                    color: white;
                    border-radius: 50%;
                    padding: 2px 6px;
                    font-size: 11px;
                    margin-left: 8px;
                    font-weight: bold;
                `;
                navLink.appendChild(badge);
            }
        }

        if (badge) {
            if (count > 0) {
                badge.textContent = count > 99 ? '99+' : count;
                badge.style.display = 'inline-block';
            } else {
                badge.style.display = 'none';
            }
        }
    }

    async markAsRead(notificationId) {
        try {
            const response = await fetch('/voting/api/notifications/read/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({ notification_id: notificationId }),
            });

            if (response.ok) {
                // Remove notification from list
                this.notifications = this.notifications.filter(n => n.id !== notificationId);
                
                // Update badge
                const unreadCount = this.notifications.filter(n => !n.is_read).length;
                this.updateNotificationBadge(unreadCount);
            }
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    }

    async markAllAsRead() {
        try {
            const response = await fetch('/voting/api/notifications/read-all/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
            });

            if (response.ok) {
                this.notifications = [];
                this.updateNotificationBadge(0);
            }
        } catch (error) {
            console.error('Error marking all notifications as read:', error);
        }
    }

    getCSRFToken() {
        const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    destroy() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
        }
    }
}

// Initialize the notification system when the page loads
let votingNotifications;

document.addEventListener('DOMContentLoaded', function() {
    // Only initialize for authenticated users
    const isAuthenticated = document.body.classList.contains('authenticated') || 
                          document.querySelector('a[href*="logout"]');
    
    if (isAuthenticated) {
        votingNotifications = new VotingNotificationSystem();
    }
});

// Clean up on page unload
window.addEventListener('beforeunload', function() {
    if (votingNotifications) {
        votingNotifications.destroy();
    }
});
