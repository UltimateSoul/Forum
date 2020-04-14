

class NotificationTextMixin:
    # notification purpose, searching for purposes works using these purposes
    SUCCESSFULLY_REGISTERED_PURPOSE = "successfully_registered"
    CONFIRM_EMAIL_PURPOSE = "confirm_email"

    # Notification content
    SUCCESSFULLY_REGISTERED = """Good job {username}, you've been successfully registered!"""
    CONFIRM_EMAIL = """Hi {username}!. 
    In order to use all our functionality you need to confirm your email. 
    We've sent confirmation link to your email, please consider activating all the functionality."""

    @staticmethod
    def get_notification_text(notification, **kwargs):
        return notification.format(**kwargs)
