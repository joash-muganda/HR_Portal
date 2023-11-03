from flask_restful import Resource, reqparse
from models.department_manager import DepartmentManager
from models.base import Session
from .utils import paginate_query  # Import the utility function

class DepartmentManagerResource(Resource):

    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('emp_no', type=int, location='args', help="Employee number is required")
    parser.add_argument('dept_no', type=str, location='args', help="Department number is required")
    parser.add_argument('page', type=int, location='args', default=1, help="Page number")
    parser.add_argument('per_page', type=int, location='args', default=10, help="Number of items per page")

    def get(self, emp_no=None, dept_no=None):
        session = Session()
        try:
            args = self.parser.parse_args()
            query = session.query(DepartmentManager)
            
            if emp_no:
                query = query.filter_by(emp_no=emp_no)
            
            if dept_no:
                # Order by the to_date in descending order to get the current manager first
                query = query.filter_by(dept_no=dept_no).order_by(DepartmentManager.to_date.desc())
            
            # Use the paginate_query utility to paginate the results
            dept_mgrs, pagination_details = paginate_query(query, args['page'], args['per_page'])
            
            return {
                "data": [{'emp_no': dm.emp_no, 'dept_no': dm.dept_no, 'from_date': str(dm.from_date), 'to_date': str(dm.to_date)} for dm in dept_mgrs],
                "pagination": pagination_details
            }
                
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()



    def post(self):
        session = Session()
        data = self.parser.parse_args()
        existing_dept_mgr = session.query(DepartmentManager).filter_by(emp_no=data['emp_no'], dept_no=data['dept_no'], from_date=data['from_date']).first()
        if existing_dept_mgr:
            return {"message": "A department-manager relation with that employee number, department number, and start date already exists."}, 400

        new_dept_mgr = DepartmentManager(emp_no=data['emp_no'], dept_no=data['dept_no'], from_date=data['from_date'], to_date=data['to_date'])
        try:
            session.add(new_dept_mgr)
            session.commit()
            return {"message": "Department-Manager relation created successfully."}, 201
        except:
            session.rollback()
            return {"message": "An error occurred while creating the department-manager relation."}, 500
        finally:
            session.close()

    def put(self, emp_no, dept_no, from_date):
        session = Session()
        data = self.parser.parse_args()
        dept_mgr = session.query(DepartmentManager).filter_by(emp_no=emp_no, dept_no=dept_no, from_date=from_date).first()
        if dept_mgr:
            dept_mgr.dept_no = data['dept_no']
            dept_mgr.to_date = data['to_date']
            try:
                session.commit()
                return {"message": "Department-Manager relation updated successfully."}
            except:
                session.rollback()
                return {"message": "An error occurred while updating the department-manager relation."}, 500
            finally:
                session.close()
        return {"message": "Department-Manager relation not found for the given employee number, department number, and start date."}, 404

    def delete(self, emp_no, dept_no, from_date):
        session = Session()
        dept_mgr = session.query(DepartmentManager).filter_by(emp_no=emp_no, dept_no=dept_no, from_date=from_date).first()
        if dept_mgr:
            try:
                session.delete(dept_mgr)
                session.commit()
                return {"message": "Department-Manager relation deleted successfully."}
            except:
                session.rollback()
                return {"message": "An error occurred while deleting the department-manager relation."}, 500
            finally:
                session.close()
        return {"message": "Department-Manager relation not found for the given employee number, department number, and start date."}, 404
