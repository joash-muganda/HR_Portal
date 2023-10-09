from datetime import datetime
from flask_restful import Resource, reqparse
from models.base import Session
from models.dept_emp_latest_date import DeptEmpLatestDate
from .utils import paginate_query

class DeptEmpLatestDateResource(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('emp_no', type=int, location='args', help="Employee number is required")
    parser.add_argument('page', type=int, location='args', default=1, help="Page number")
    parser.add_argument('per_page', type=int, location='args', default=10, help="Number of items per page")

    def get(self, emp_no=None):
        session = Session()
        try:
            args = self.parser.parse_args()
            query = session.query(DeptEmpLatestDate)

            if emp_no:
                query = query.filter_by(emp_no=emp_no)

            employees, pagination_details = paginate_query(query, args['page'], args['per_page'])
            return {
                "data": [{'emp_no': e.emp_no, 'from_date': str(e.from_date), 'to_date': str(e.to_date)} for e in employees],
                "pagination": pagination_details
            }
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()
