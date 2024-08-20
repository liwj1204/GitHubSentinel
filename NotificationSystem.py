class NotificationSystem:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def send_notification(self, message):
        method = self.config_manager.get('notification').get('method')
        if method == 'email':
            email = self.config_manager.get('notification').get('email')
            print(f"Sending email to {email}: {message}")
        else:
            print(f"Notification: {message}")
