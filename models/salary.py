from sqlalchemy import Column, Integer, Date, ForeignKey
from .base import Base

class Salary(Base):
    __tablename__ = 'salaries'
    
    emp_no = Column(Integer, ForeignKey('employees.emp_no'), primary_key=True)
    salary = Column(Integer)
    from_date = Column(Date, primary_key=True)
    to_date = Column(Date)
