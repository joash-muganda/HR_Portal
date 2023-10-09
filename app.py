

from flask import Flask, jsonify
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from json import JSONEncoder
from decimal import Decimal
import logging



# Import resources
from controllers.employee_resource import EmployeeResource
from controllers.department_resource import DepartmentResource
from controllers.title_resource import TitleResource
from controllers.department_employee_resource import DepartmentEmployeeResource
from controllers.department_manager_resource import DepartmentManagerResource
from controllers.salary_resource import SalariesResource
from controllers.current_dept_emp_resource import CurrentDeptEmpResource
from controllers.dept_emp_latest_date_resource import DeptEmpLatestDateResource
from controllers.gender_distribution_resource import GenderDistributionResource
from controllers.salary_growth_resource import SalaryGrowthResource
from controllers.average_salary_per_department_resource import AverageSalaryPerDepartmentResource


# Custom JSON Encoder
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJSONEncoder, self).default(obj)

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


app.json_encoder = CustomJSONEncoder  # Set the custom encoder

CORS(app, origins=["http://localhost:3000"])

# This setting allows exceptions to be propagated rather than handled by Flask's default error handling
app.config['PROPAGATE_EXCEPTIONS'] = True

# Adjust Flask-RESTful initialization to not enforce JSON content type for GET requests
api = Api(app, catch_all_404s=True, 
          default_mediatype='application/json', 
          errors={
              'UnsupportedMediaType': {
                  'message': "Did not attempt to load JSON data because the request Content-Type was not 'application/json'.",
                  'status': 415,
              }
          })
# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=str(e)), 500

# Add resources to the API
api.add_resource(EmployeeResource, '/employees', '/employees/<int:emp_no>')
api.add_resource(DepartmentResource, '/departments', '/departments/<string:dept_no>', '/departments/<string:dept_no>/employees')
api.add_resource(DepartmentEmployeeResource, '/department_employee', '/department_employee/<int:emp_no>', '/department_employee/<int:emp_no>/<string:dept_no>')
api.add_resource(DepartmentManagerResource, '/department_manager', '/department_manager/<int:emp_no>', '/department_manager/<string:dept_no>', '/department_manager/<int:emp_no>/<string:dept_no>', '/departments/<string:dept_no>/manager')
api.add_resource(SalariesResource, '/salaries', '/salaries/<int:emp_no>', '/salaries/<int:emp_no>/<string:from_date>')
api.add_resource(TitleResource, '/titles', '/titles/<int:emp_no>', '/titles/<int:emp_no>/<string:title>', '/titles/<int:emp_no>/<string:title>/<string:from_date>')
api.add_resource(CurrentDeptEmpResource, '/current_dept_emp', '/current_dept_emp/<int:emp_no>')
api.add_resource(DeptEmpLatestDateResource, '/dept_emp_latest_date', '/dept_emp_latest_date/<int:emp_no>')
api.add_resource(GenderDistributionResource, '/employees/gender_distribution')
api.add_resource(SalaryGrowthResource, '/salary_growth')
api.add_resource(AverageSalaryPerDepartmentResource, '/average_salary_per_department')



@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error("Server encountered an error: %s", e)
    return jsonify(error="Internal Server Error"), 500


if __name__ == '__main__':
    app.run(debug=True)
