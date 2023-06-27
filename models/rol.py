from models.db import db
from sqlalchemy import Column, Integer, Boolean, ForeignKey

class Rol(db.Model):
    __tablename__ = "rol"
    
    id = Column(Integer, primary_key=True)
    admin = Column(Boolean, nullable=False)
    user = Column(Integer, ForeignKey("user.id"), nullable=False)
    group = Column(Integer, ForeignKey("group.id"), nullable=False)

    def __init__(self, user, group, admin):
        self.user = user
        self.group = group
        self.admin = admin
    
    def get_data(self):
        return {
            "id": self.id,
            "user": self.user,
            "group": self.group,
            "admin": self.admin
        }
