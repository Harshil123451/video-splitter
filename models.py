from flask_login import UserMixin
from datetime import datetime

class User(UserMixin):
    def __init__(self):
        self.id = None
        self.email = None
        self.subscription_tier = 'free'
        self.subscription_end = None
        self.stripe_customer_id = None

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def is_premium(self):
        return (self.subscription_tier == 'premium' and 
                self.subscription_end and 
                self.subscription_end > datetime.utcnow()) 