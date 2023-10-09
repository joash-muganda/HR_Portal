from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .title import Title
from .salary import Salary

class Employee(Base):
    __tablename__ = 'employees'
    
    emp_no = Column(Integer, primary_key=True)
    birth_date = Column(Date)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    hire_date = Column(Date)

    titles = relationship('Title', backref='employee')
    salaries = relationship('Salary', backref='employee')
    
    def to_dict(self):
        return {
            'emp_no': self.emp_no,
            'birth_date': str(self.birth_date),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'hire_date': str(self.hire_date),
            # If you want to include titles and salaries too, uncomment the following:
            # 'titles': [title.to_dict() for title in self.titles],
            # 'salaries': [salary.to_dict() for salary in self.salaries]
        }
