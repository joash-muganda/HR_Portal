
from sqlalchemy import Column, Integer, String, Date
from models.base import Base


class CurrentDeptEmp(Base):
    __tablename__ = 'current_dept_emp'

    emp_no = Column(Integer, primary_key=True)
    dept_no = Column(String(4), primary_key=True)
    from_date = Column(Date)
    to_date = Column(Date)
