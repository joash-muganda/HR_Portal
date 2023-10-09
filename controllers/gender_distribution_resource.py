from flask_restful import Resource
from models.employee import Employee
from models.base import Session
from sqlalchemy import func


class GenderDistributionResource(Resource):
    def get(self):
        session = Session()
        try:
            # Query to get the gender distribution
            gender_distribution = session.query(Employee.gender, func.count(Employee.gender))\
                                         .group_by(Employee.gender)\
                                         .all()

            # Convert the result into a dictionary for easier processing on the frontend
            distribution_dict = {gender: count for gender, count in gender_distribution}

            return {"data": distribution_dict}
            
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()
