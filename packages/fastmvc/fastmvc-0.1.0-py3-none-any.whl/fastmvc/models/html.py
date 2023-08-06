class Alert:
    """Use this class to make alerts on any page"""
    def __init__(self, message = None, alert_type = 'danger'):
        self.type = alert_type
        self.message = message