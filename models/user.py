from models.db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    birthDate = db.Column(db.Date, nullable=False)
    
    def __init__ (self, name, user, password, email, birthDate):
        self.name = name
        self.user = user
        self.password = password
        self.email = email
        self.birthDate = birthDate
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "user": self.user,
            "email": self.email,
            "birthDate": self.birthDate.strftime("%d-%m-%y"),
            "password": self.password
        }