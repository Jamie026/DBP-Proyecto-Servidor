from models.db import db
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Rol(db.Model):
    __tablename__ = "rol"
    
    id = Column(Integer, primary_key=True)
    admin = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    
    user = relationship("User", backref="roles", cascade="all, delete")
    group = relationship("Group", backref="roles", cascade="all, delete")

    def __init__(self, user, group, admin):
        self.user = user
        self.group = group
        self.admin = admin
    
    def get_data(self):
        return {
            "id": self.id,
            "user": self.user.get_data(),
            "group": self.group.get_data(),
            "admin": self.admin
        }
