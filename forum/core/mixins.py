class NotificationPurposes:
    """Handles notification purposes.
     Notifications could be found and deleted using these purposes"""
    SUCCESSFULLY_REGISTERED_PURPOSE = 0
    CONFIRM_EMAIL_PURPOSE = 1
    EMAIL_WAS_CONFIRMED_PURPOSE = 2
    REQUEST_WAS_SENT_PURPOSE = 3
    APPROVED_TEAM_REQUEST_PURPOSE = 4
    REJECTED_TEAM_REQUEST_PURPOSE = 5


class NotificationChoices:
    SUCCESS = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    NOTIFICATION_CHOICES = ((SUCCESS, 'success'),
                            (INFO, 'info'),
                            (WARNING, 'warning'),
                            (ERROR, 'error'))


class NotificationTextMixin(NotificationChoices, NotificationPurposes):

    # Notification content
    SUCCESSFULLY_REGISTERED = """Good job {username}, you've been successfully registered!"""
    CONFIRM_EMAIL = """Hi {username}!
    In order to use all our functionality you need to confirm your email. 
    We've sent confirmation link to your email, please consider activating all the functionality."""
    EMAIL_CONFIRMED = """Hi {username}!
    Your email was successfully confirmed. Now you are able create and join teams and do a lot more stuff. 
    Please enjoy our awesome forum, see you soon!"""
    TEAM_REQUEST_WAS_SENT_WITH_ACTIVATED_EMAIL = """Hi {username}! Your team request was successfully created!
    We will send you email message as soon as your request will be accepted or rejected."""
    TEAM_REQUEST_WAS_SENT_WITH_DEACTIVATED_EMAIL = """Hi {username}! Your team request was successfully created!"""
    ACCEPTED_TEAM_REQUEST = """Congratulations {username}!
    Your team request into {team_name} was accepted!"""
    REJECTED_TEAM_REQUEST = """Your team request into {team_name} was rejected."""

    @staticmethod
    def get_notification_text(notification, **kwargs):
        return notification.format(**kwargs)
