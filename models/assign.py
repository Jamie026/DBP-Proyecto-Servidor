from models.db import db
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Date

class Assign(db.Model):
    __tablename__ = "assign"
    
    id = Column(Integer, primary_key=True)
    state = Column(Integer, default=0, nullable=False)
    date = Column(Date, default=datetime.now)
    task = Column(Integer, ForeignKey("task.id"), nullable=False)
    group = Column(Integer, ForeignKey("group.id"), nullable=False)

    def __init__(self, task, group):
        self.task = task
        self.group = group
        
    def get_data(self):
        return {
            "id": self.id,
            "task": self.task,
            "group": self.group,
            "state": self.state,
            "date": self.date
        }
