from flask_restful import Resource
from models.base import Session
from models.employee import Employee
from models.salary import Salary  # Assuming you have a Salary model
from sqlalchemy import func, extract, and_
from models.salary import Salary

from models.salary import Salary  # Assuming this is the correct import for your salary model

class SalaryGrowthResource(Resource):
    def get(self):
        session = Session()
        try:
            # Query to get the average salary by month
            salary_growth = session.query(
                extract('month', Salary.from_date).label('month'), 
                func.avg(Salary.salary).label('avg_salary')
            )\
            .group_by(extract('month', Salary.from_date))\
            .order_by('month')\
            .all()

            # Convert the result into a list of dictionaries for easier processing on the frontend
            result = [{"month": month, "avg_salary": float(avg_salary)} for month, avg_salary in salary_growth]

            return {"data": result}
            
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()
