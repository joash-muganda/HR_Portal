from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import relationship

from sqlalchemy import Column, String
from .base import Base
from .department_employee import DepartmentEmployee
from .department_manager import DepartmentManager

class Department(Base):
    __tablename__ = 'departments'
    
    dept_no = Column(String, primary_key=True)
    dept_name = Column(String)

    employees = relationship('DepartmentEmployee', backref='department')
    managers = relationship('DepartmentManager', backref='department')
