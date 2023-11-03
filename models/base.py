from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'mysql+mysqlconnector://joash:Faryl%402023@localhost:3306/employees'

engine = create_engine(DATABASE_URI, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()
