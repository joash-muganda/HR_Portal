from flask_restful import Resource, reqparse
from models.base import Session
from .utils import paginate_query
from sqlalchemy import or_
from flask import request
from models.employee import Employee
from models.department_manager import DepartmentManager
from models.department_employee import DepartmentEmployee
from flask import current_app as app

def positive_int(value):
    if value == '':
        return 1
    try:
        int_value = int(value)
        if int_value < 1:
            raise ValueError
        return int_value
    except ValueError:
        raise ValueError("The 'page' parameter must be a positive integer.")

class EmployeeResource(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('emp_no', type=int, location='args', help="Employee number is required")
    parser.add_argument('page', type=positive_int, location='args', default=1, help="Page number")
    parser.add_argument('per_page', type=int, location='args', default=10, help="Number of items per page")
    parser.add_argument('search_term', type=str, location='args', default='', help="Search term for employees")


    def get(self, emp_no=None):
        session = Session()
        manager = None
        try:
            args = self.parser.parse_args()
            query = session.query(Employee)
            
            if emp_no:
                query = query.filter_by(emp_no=emp_no)

                # If a specific employee number was provided, fetch the manager's details
                manager_query = session.query(Employee).join(DepartmentManager, Employee.emp_no == DepartmentManager.emp_no).\
                                join(DepartmentEmployee, DepartmentManager.dept_no == DepartmentEmployee.dept_no).\
                                filter(DepartmentEmployee.emp_no == emp_no, DepartmentManager.to_date == '9999-01-01').\
                                first()
                if manager_query:
                    manager = {
                        "emp_no": manager_query.emp_no,
                        "first_name": manager_query.first_name,
                        "last_name": manager_query.last_name
                    }
            
            if args['search_term']:
                # Use `ilike` for case-insensitive search
                search = f"%{args['search_term']}%"
                query = query.filter(or_(
                    Employee.first_name.ilike(search),
                    Employee.last_name.ilike(search)
                ))

            # Filter by hire date if the parameters exist
            hired_after = request.args.get('hired_after')
            hired_before = request.args.get('hired_before')
            if hired_after:
                query = query.filter(Employee.hire_date >= hired_after)
            if hired_before:
                query = query.filter(Employee.hire_date <= hired_before)

            employees, pagination_details = paginate_query(query, args['page'], args['per_page'])
            
            return {
                "data": [emp.to_dict() for emp in employees],
                "pagination": pagination_details,
                "manager": manager
            }
            
        except Exception as e:
            app.logger.error("Error in EmployeeResource GET: %s", e, exc_info=True)
            return {"error": str(e)}, 500

        finally:
            session.close()


    def get_manager(self, emp_no, session):
        manager_query = session.query(Employee).join(DepartmentManager, Employee.emp_no == DepartmentManager.emp_no).\
                        join(DepartmentEmployee, DepartmentManager.dept_no == DepartmentEmployee.dept_no).\
                        filter(DepartmentEmployee.emp_no == emp_no, DepartmentManager.to_date == '9999-01-01').\
                        first()
        if manager_query:
            return {
                "emp_no": manager_query.emp_no,
                "first_name": manager_query.first_name,
                "last_name": manager_query.last_name
            }
        return None

    def post(self):
        session = Session()
        data = request.get_json()
        new_employee = Employee(
            emp_no=data.get('emp_no'),
            birth_date=data.get('birth_date'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            gender=data.get('gender'),
            hire_date=data.get('hire_date')
        )
        try:
            session.add(new_employee)
            session.commit()
            return {"message": "Employee created successfully."}, 201
        except Exception as e:
            session.rollback()
            return {"error": str(e)}, 500
        finally:
            session.close()

    def put(self, emp_no):
        session = Session()
        data = request.get_json()
        employee = session.query(Employee).filter_by(emp_no=emp_no).first()
        if employee:
            employee.birth_date = data.get('birth_date', employee.birth_date)
            employee.first_name = data.get('first_name', employee.first_name)
            employee.last_name = data.get('last_name', employee.last_name)
            employee.gender = data.get('gender', employee.gender)
            employee.hire_date = data.get('hire_date', employee.hire_date)
            try:
                session.commit()
                return {"message": "Employee updated successfully."}
            except Exception as e:
                session.rollback()
                return {"error": str(e)}, 500
            finally:
                session.close()
        return {"message": "Employee not found."}, 404

    def delete(self, emp_no):
        session = Session()
        employee = session.query(Employee).filter_by(emp_no=emp_no).first()
        if employee:
            try:
                session.delete(employee)
                session.commit()
                return {"message": "Employee deleted successfully."}
            except Exception as e:
                session.rollback()
                return {"error": str(e)}, 500
            finally:
                session.close()
        return {"message": "Employee not found."}, 404

