from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
#from model.post import Post
from __init__ import db
from api.jwt_authorize import token_required

class Analytics(db.Model):
    __tablename__ = 'analytics'

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('frostbytes.id'), nullable=False)    
    stars = db.Column(db.Integer, nullable=False)

    user = relationship('Frostbyte')
    channel = relationship('Channel', back_populates='channel_analytics')

    __table_args__ = (db.UniqueConstraint('user_id', 'channel_id', name='unique_user_channel_analytics'),)

    def __init__(self, channel_id, user_id, stars):
        self.channel_id = channel_id
        self.user_id = user_id
        self.stars = stars


    def create(self):
        db.session.add(self)
        db.session.commit()

    def read(self):
       
        return {
            'id': self.id,
            'channel_id': self.channel_id,
            "user_id": self.user_id,
            'stars': self.stars,
        }

    def update(self):
       
        db.session.add(self)
        db.session.commit()

    def delete(self):
       
        db.session.delete(self)
        db.session.commit()
        

def initAnalytics():
        from model.analytics import Analytics
        sample_analytics = [
            {"user_id": 1, "channel_id": 1, "stars": 5},
            {"user_id": 2, "channel_id": 2, "stars": 3},
            {"user_id": 3, "channel_id": 3, "stars": 4},
        ]
        for data in sample_analytics:
            analytics = Analytics(user_id=data["user_id"], channel_id=data["channel_id"], stars=data["stars"])
            db.session.add(analytics)
        db.session.commit()
