from sqlalchemy import create_engine, Column, Integer, Date
from sqlalchemy import Column, Integer, String, Date
from models.base import Base

class DeptEmpLatestDate(Base):
    __tablename__ = 'dept_emp_latest_date'

    emp_no = Column(Integer, primary_key=True)
    from_date = Column(Date)
    to_date = Column(Date)
