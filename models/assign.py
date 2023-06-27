from models.db import db
from sqlalchemy import Column, Integer, ForeignKey

class Assign(db.Model):
    __tablename__ = "assign"
    
    id = Column(Integer, primary_key=True)
    state = Column(Integer, default=0, nullable=False)
    task = Column(Integer, ForeignKey("task.id"), nullable=False)
    group = Column(Integer, ForeignKey("group.id"), nullable=False)

    def __init__(self, task, group):
        self.task = task
        self.group = group
        
    def get_data(self):
        return {
            "id": self.id,
            "task": self.task,
            "group": self.group
        }
