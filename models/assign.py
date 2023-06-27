from models.db import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Assign(db.Model):
    __tablename__ = "assign"
    
    id = Column(Integer, primary_key=True)
    state = Column(Integer, default=0, nullable=False)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    
    task = relationship("Task", backref="assigns", cascade="all, delete")
    group = relationship("Group", backref="assigns", cascade="all, delete")

    def __init__(self, task, group):
        self.task = task
        self.group = group
        
    def get_data(self):
        return {
            "id": self.id,
            "task": self.task.get_data(),
            "group": self.group.get_data()
        }
