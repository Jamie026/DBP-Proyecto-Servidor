from models.db import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

class Task(db.Model):
    __tablename__ = "task"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date = Column(Date, default=datetime.now)
    description = Column(String(200), nullable=False)
    user = Column(Integer, ForeignKey("user.id"), nullable=False)

    assigns = relationship("Assign", cascade="delete")
        
    def __init__(self, name, description, user):
        self.name = name
        self.description = description
        self.user = user
        
    def get_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "date": self.date,
            "user": self.user
        }
