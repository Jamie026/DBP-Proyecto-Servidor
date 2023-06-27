from models.db import db
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

class Group(db.Model):
    __tablename__ = "group"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)

    assigns = relationship("Assign", cascade="delete")
    roles = relationship("Rol", cascade="delete")
    
    def __init__(self, name, password, date):
        self.name = name
        self.password = password
        self.date = date
        
    def get_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "date": self.date
        }
