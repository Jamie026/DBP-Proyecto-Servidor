from models.db import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    date = db.Column(db.Date, nullable=False)
    user = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    
    def __init__ (self, name, description, date, user):
        self.name = name
        self.description = description
        self.date = date
        self.user = user
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": self.date,
            "user": self.user
        }