from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .base import Base

class DepartmentEmployee(Base):
    __tablename__ = 'dept_emp'
    
    emp_no = Column(Integer, ForeignKey('employees.emp_no'), primary_key=True)
    dept_no = Column(String, ForeignKey('departments.dept_no'), primary_key=True)
    from_date = Column(Date, primary_key=True)
    to_date = Column(Date)
