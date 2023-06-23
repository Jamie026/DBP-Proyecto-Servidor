from models.db import db

class Assign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.Integer, nullable=False)
    group = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Integer, default=0, nullable=False)
    
    def __init__ (self, task, group):
        self.task = task
        self.group = group
        
    def to_dict(self):
        return {
            "id": self.id,
            "task": self.task,
            "group": self.group
        }