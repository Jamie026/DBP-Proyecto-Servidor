from models.db import db
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from datetime import datetime

class Group(db.Model):
    __tablename__ = "group"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    date = Column(Date, default=datetime.now)

    assigns = relationship("Assign", cascade="delete")
    roles = relationship("Rol", cascade="delete")
    
    def __init__(self, name, password):
        self.name = name
        self.password = password
        
    def get_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "date": self.date
        }
