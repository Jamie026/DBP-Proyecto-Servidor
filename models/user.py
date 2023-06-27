from models.db import db
from sqlalchemy import Column, Integer, String, Date

class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    birth_date = Column(Date, nullable=False)
    
    def __init__(self, name, username, password, email, birth_date):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.birth_date = birth_date
        
    def get_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "birth_date": self.birth_date.strftime("%d-%m-%y"),
            "password": self.password
        }