from datetime import datetime
from __init__ import db  

class Analytics(db.Model):
    __tablename__ = 'analytics'

    id = db.Column(db.Integer, primary_key=True) 
    park_id = db.Column(db.String(50), nullable=False)  
    stars = db.Column(db.Float, nullable=False)  
    total_reviews = db.Column(db.Integer, nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow) 

    def __init__(self, park_id, stars, total_reviews):
        self.park_id = park_id
        self.stars = stars
        self.total_reviews = total_reviews

    def to_dict(self):
        """Serialize the model data to a dictionary."""
        return {
            'id': self.id,
            'park_id': self.park_id,
            'stars': self.stars,
            'total_reviews': self.total_reviews,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }