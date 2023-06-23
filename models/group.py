from models.db import db

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    def __init__ (self, name, password, date):
        self.name = name
        self.password = password
        self.date = date
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "date": self.date
        }