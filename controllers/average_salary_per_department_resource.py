from flask_restful import Resource
from models.base import Session
from models.department import Department
from models.department_employee import DepartmentEmployee as DeptEmp
from models.salary import Salary
from sqlalchemy import func


class AverageSalaryPerDepartmentResource(Resource):
    def get(self):
        session = Session()
        try:
            result = session.query(Department.dept_name, func.avg(Salary.salary).label('averageSalary'))\
                            .join(DeptEmp, DeptEmp.dept_no == Department.dept_no)\
                            .join(Salary, Salary.emp_no == DeptEmp.emp_no)\
                            .group_by(Department.dept_name)\
                            .all()

            return {
                "data": [{"dept_name": r[0], "averageSalary": float(r[1])} for r in result]
            }

        except Exception as e:
            print(e)  # Log the error for debugging
            return {"error": "An internal error occurred."}, 500
        finally:
            session.close()
