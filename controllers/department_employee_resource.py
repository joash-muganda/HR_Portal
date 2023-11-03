

from flask_restful import Resource, reqparse
from models.department_employee import DepartmentEmployee
from models.base import Session
from .utils import paginate_query
from datetime import datetime
from flask import request

class DepartmentEmployeeResource(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('emp_no', type=int, location='args', help="Employee number is required")
    parser.add_argument('dept_no', type=str, location='args', help="Department number is required")
    parser.add_argument('from_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d').date(), location='args', help="Start date is required in YYYY-MM-DD format")
    parser.add_argument('to_date', type=lambda x: datetime.strptime(x, '%Y-%m-%d').date(), location='args', help="End date is required in YYYY-MM-DD format")
    parser.add_argument('page', type=int, location='args', default=1, help="Page number")
    parser.add_argument('per_page', type=int, location='args', default=10, help="Number of items per page")

    def get(self, emp_no=None, dept_no=None):
        session = Session()
        try:
            args = self.parser.parse_args()
            query = session.query(DepartmentEmployee)
            
            if emp_no:
                query = query.filter_by(emp_no=emp_no)
            if dept_no:
                query = query.filter_by(dept_no=dept_no)

            dept_emps, pagination_details = paginate_query(query, args['page'], args['per_page'])
            return {
                "data": [{'emp_no': de.emp_no, 'dept_no': de.dept_no, 'from_date': str(de.from_date), 'to_date': str(de.to_date)} for de in dept_emps],
                "pagination": pagination_details
            }
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()

    def post(self):
        session = Session()
        data = request.get_json()
        existing_dept_emp = session.query(DepartmentEmployee).filter_by(emp_no=data['emp_no'], dept_no=data['dept_no'], from_date=data['from_date']).first()

        if existing_dept_emp:
            return {"message": "A department-employee relation with that employee number, department number, and start date already exists."}, 400

        new_dept_emp = DepartmentEmployee(emp_no=data['emp_no'], dept_no=data['dept_no'], from_date=data['from_date'], to_date=data['to_date'])
        try:
            session.add(new_dept_emp)
            session.commit()
            return {"message": "Department-Employee relation created successfully."}, 201
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        finally:
            session.close()

    def put(self, emp_no, dept_no, from_date):
        session = Session()
        data = request.get_json()
        dept_emp = session.query(DepartmentEmployee).filter_by(emp_no=emp_no, dept_no=dept_no, from_date=from_date).first()

        if dept_emp:
            dept_emp.dept_no = data['dept_no']
            dept_emp.to_date = data['to_date']
            try:
                session.commit()
                return {"message": "Department-Employee relation updated successfully."}
            except Exception as e:
                session.rollback()
                return {"error": str(e)}, 500
            finally:
                session.close()
        return {"message": "Department-Employee relation not found for the given employee number, department number, and start date."}, 404

    def delete(self, emp_no, dept_no, from_date):
        session = Session()
        dept_emp = session.query(DepartmentEmployee).filter_by(emp_no=emp_no, dept_no=dept_no, from_date=from_date).first()
        
        if dept_emp:
            try:
                session.delete(dept_emp)
                session.commit()
                return {"message": "Department-Employee relation deleted successfully."}
            except Exception as e:
                session.rollback()
                return {"error": str(e)}, 500
            finally:
                session.close()
        return {"message": "Department-Employee relation not found for the given employee number, department number, and start date."}, 404
