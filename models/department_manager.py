from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .base import Base

class DepartmentManager(Base):
    __tablename__ = 'dept_manager'
    
    emp_no = Column(Integer, ForeignKey('employees.emp_no'), primary_key=True)
    dept_no = Column(String, ForeignKey('departments.dept_no'), primary_key=True)
    from_date = Column(Date, primary_key=True)
    to_date = Column(Date)
