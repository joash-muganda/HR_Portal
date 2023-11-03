from sqlalchemy import Column, Integer, String, Date, ForeignKey
from .base import Base

class Title(Base):
    __tablename__ = 'titles'
    
    emp_no = Column(Integer, ForeignKey('employees.emp_no'), primary_key=True)
    title = Column(String)
    from_date = Column(Date, primary_key=True)
    to_date = Column(Date)
