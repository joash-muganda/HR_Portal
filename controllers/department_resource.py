# from flask_restful import Resource, reqparse
# from sqlalchemy import or_
# from sqlalchemy.sql import func
# from models.department import Department
# from models.department_employee import DepartmentEmployee  # Import the DepartmentEmployee model
# from models.base import Session
# from .utils import paginate_query
# from flask import request

# class DepartmentResource(Resource):

#     parser = reqparse.RequestParser(bundle_errors=True)
#     parser.add_argument('dept_no', type=str, location='args', help="Department number is required")
#     parser.add_argument('page', type=int, location='args', default=1, help="Page number")
#     parser.add_argument('per_page', type=int, location='args', default=10, help="Number of items per page")
#     parser.add_argument('search_term', type=str, location='args', default='', help="Search term for departments")
#     parser.add_argument('count_employees', type=bool, location='args', default=False, help="Flag to count employees per department")

#     def get(self, dept_no=None):
#         session = Session()
#         try:
#             args = self.parser.parse_args()
#             query = session.query(Department)

#             if dept_no:
#                 query = query.filter_by(dept_no=dept_no)

#             if args['search_term']:
#                 search = f"%{args['search_term']}%"
#                 query = query.filter(Department.dept_name.ilike(search))

#             if args['count_employees']:
#                 query = session.query(Department.dept_no, Department.dept_name, func.count(DepartmentEmployee.emp_no).label('employee_count')).join(DepartmentEmployee, Department.dept_no == DepartmentEmployee.dept_no).group_by(Department.dept_no, Department.dept_name)
#                 departments = query.all()
#                 return {
#                     "data": [{'dept_no': dept[0], 'dept_name': dept[1], 'employee_count': dept[2]} for dept in departments]
#                 }

#             departments, pagination_details = paginate_query(query, args['page'], args['per_page'])
#             return {
#                 "data": [{'dept_no': dept.dept_no, 'dept_name': dept.dept_name} for dept in departments],
#                 "pagination": pagination_details
#             }

#         except Exception as e:
#             return {"error": str(e)}, 500
#         finally:
#             session.close()

#     def get_employees_by_department(dept_no):
#         session = Session()
#         try:
#             department = session.query(Department).filter_by(dept_no=dept_no).first()
#             if not department:
#                 return {"message": "Department not found."}, 404

#             employees = department.employees  # This uses the relationship defined in your ORM model
#             return {"data": [{"emp_no": emp.emp_no, "from_date": emp.from_date, "to_date": emp.to_date} for emp in employees]}

#         except Exception as e:
#             return {"error": str(e)}, 500
#         finally:
#             session.close()

from flask_restful import Resource, reqparse
from sqlalchemy import or_
from sqlalchemy.sql import func
from models.department import Department
# Import the DepartmentEmployee model
from models.department_employee import DepartmentEmployee
from models.base import Session
from .utils import paginate_query
from flask import request


class DepartmentResource(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('dept_no', type=str, location='args',
                        help="Department number is required")
    parser.add_argument('page', type=int, location='args',
                        default=1, help="Page number")
    parser.add_argument('per_page', type=int, location='args',
                        default=10, help="Number of items per page")
    parser.add_argument('search_term', type=str, location='args',
                        default='', help="Search term for departments")
    parser.add_argument('count_employees', type=bool, location='args',
                        default=False, help="Flag to count employees per department")

    def get(self, dept_no=None):
        if dept_no and "employees" in request.path:
            return self.get_employees_by_department(dept_no)

        session = Session()
        try:
            args = self.parser.parse_args()
            query = session.query(Department)

            if dept_no:
                query = query.filter_by(dept_no=dept_no)

            if args['search_term']:
                search = f"%{args['search_term']}%"
                query = query.filter(Department.dept_name.ilike(search))

            if args['count_employees']:
                query = session.query(Department.dept_no, Department.dept_name, func.count(DepartmentEmployee.emp_no).label('employee_count')).join(
                    DepartmentEmployee, Department.dept_no == DepartmentEmployee.dept_no).group_by(Department.dept_no, Department.dept_name)
                departments = query.all()
                return {
                    "data": [{'dept_no': dept[0], 'dept_name': dept[1], 'employee_count': dept[2]} for dept in departments]
                }

            departments, pagination_details = paginate_query(
                query, args['page'], args['per_page'])
            return {
                "data": [{'dept_no': dept.dept_no, 'dept_name': dept.dept_name} for dept in departments],
                "pagination": pagination_details
            }

        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()

    def get_employees_by_department(self, dept_no):
        session = Session()
        try:
            department = session.query(Department).filter_by(
                dept_no=dept_no).first()
            if not department:
                return {"message": "Department not found."}, 404

            # This uses the relationship defined in your ORM model
            employees = department.employees
            # return {"data": [{"emp_no": emp.emp_no, "from_date": emp.from_date, "to_date": emp.to_date} for emp in employees]}
            return {
                "data": [
                    {
                        "emp_no": emp.emp_no,
                        "from_date": emp.from_date.strftime('%Y-%m-%d'),
                        "to_date": emp.to_date.strftime('%Y-%m-%d')
                    } for emp in employees
                ]
            }

        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()

    def post(self):
        session = Session()
        data = self.parser.parse_args()

        # Check if department name or department number already exists
        existing_department_name = session.query(
            Department).filter_by(dept_name=data['dept_name']).first()
        existing_department_no = session.query(
            Department).filter_by(dept_no=data['dept_no']).first()

        if existing_department_name:
            return {"message": "A department with that name already exists."}, 400
        if existing_department_no:
            return {"message": "A department with that number already exists."}, 400

        new_department = Department(
            dept_no=data['dept_no'], dept_name=data['dept_name'])
        try:
            session.add(new_department)
            session.commit()
            return {"message": "Department created successfully."}, 201
        except:
            session.rollback()
            return {"message": "An error occurred while creating the department."}, 500
        finally:
            session.close()

    def put(self, dept_no):
        session = Session()
        data = self.parser.parse_args()

        department = session.query(Department).filter_by(
            dept_no=dept_no).first()
        if department:
            department.dept_name = data['dept_name']
            try:
                session.commit()
                return {"message": "Department updated successfully."}
            except:
                session.rollback()
                return {"message": "An error occurred while updating the department."}, 500
            finally:
                session.close()
        return {"message": "Department not found."}, 404

    def delete(self, dept_no):
        session = Session()
        department = session.query(Department).filter_by(
            dept_no=dept_no).first()
        if department:
            try:
                session.delete(department)
                session.commit()
                return {"message": "Department deleted successfully."}
            except:
                session.rollback()
                return {"message": "An error occurred while deleting the department."}, 500
            finally:
                session.close()
        return {"message": "Department not found."}, 404
