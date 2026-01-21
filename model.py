from sqlalchemy import Column, Integer, String, Boolean, ForeignKey  
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique = True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default = True)

    employees = relationship("Employee",back_populates="owner")

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    department = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"),nullable=True)

    owner = relationship("User", back_populates="employees")