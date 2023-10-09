from datetime import datetime
from flask_restful import Resource, reqparse
from models.base import Session
from models.current_dept_emp import CurrentDeptEmp
from .utils import paginate_query

class CurrentDeptEmpResource(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('emp_no', type=int, location='args', help="Employee number is required")
    parser.add_argument('dept_no', type=str, location='args', help="Department number is required")
    parser.add_argument('from_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d').date(), location='args', help="Start date is required in YYYY-MM-DD format")
    parser.add_argument('to_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d').date(), location='args', help="End date is required in YYYY-MM-DD format")
    parser.add_argument('page', type=int, location='args', default=1, help="Page number")
    parser.add_argument('per_page', type=int, location='args', default=10, help="Number of items per page")


    def get(self, emp_no=None):
        session = Session()
        try:
            args = self.parser.parse_args()
            query = session.query(CurrentDeptEmp)
            if emp_no:
                query = query.filter_by(emp_no=emp_no)
            departments, pagination_details = paginate_query(query, args['page'], args['per_page'])
            return {
                "data": [{'emp_no': d.emp_no, 'dept_no': d.dept_no, 'from_date': str(d.from_date), 'to_date': str(d.to_date)} for d in departments],
                "pagination": pagination_details
            }
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()
