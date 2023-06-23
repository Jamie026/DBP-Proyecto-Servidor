from models.db import db

class Rol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    group = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    
    def __init__ (self, user, group, admin):
        self.user = user
        self.group = group
        self.admin = admin