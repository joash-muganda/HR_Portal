
from flask_restful import Resource, reqparse
from models.title import Title
from models.base import Session
from .utils import paginate_query
from datetime import datetime

class TitleResource(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('emp_no', type=int, location='args', help="Employee number")
    parser.add_argument('title', type=str, location='args', help="Title")
    parser.add_argument('from_date', type=str, location='args', help="From date")
    parser.add_argument('page', type=int, location='args', default=1, help="Page number")
    parser.add_argument('per_page', type=int, location='args', default=10, help="Number of items per page")

    def get(self, emp_no=None):
        session = Session()
        try:
            args = self.parser.parse_args()
            query = session.query(Title)

            if emp_no:
                query = query.filter_by(emp_no=emp_no)
            else:
                if args['emp_no']:
                    query = query.filter_by(emp_no=args['emp_no'])
            
            if args['title']:
                query = query.filter_by(title=args['title'])
            if args['from_date']:
                query = query.filter_by(from_date=args['from_date'])

            titles, pagination_details = paginate_query(query, args['page'], args['per_page'])
            
            return {
                "data": [{'emp_no': t.emp_no, 'title': t.title, 'from_date': str(t.from_date), 'to_date': str(t.to_date)} for t in titles],
                "pagination": pagination_details
            }
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            session.close()




    def post(self):
        session = Session()
        data = TitleResource.parser.parse_args()
        existing_title = session.query(Title).filter_by(emp_no=data['emp_no'], title=data['title'], from_date=data['from_date']).first()
        if existing_title:
            return {"message": "A title entry with those details already exists."}, 400

        new_title = Title(
            emp_no=data['emp_no'],
            title=data['title'],
            from_date=data['from_date'],
            to_date=data['to_date']
        )
        try:
            session.add(new_title)
            session.commit()
            return {"message": "Title entry created successfully."}, 201
        # except Exception as e:
        #     session.rollback()
        #     return {"error": str(e)}, 500
        except Exception as e:
            session.rollback()
            print(e)  # Log the error to the console
            return {"error": str(e)}, 500

        finally:
            session.close()

    def put(self, emp_no, title, from_date):
        session = Session()
        data = TitleResource.parser.parse_args()
        title_entry = session.query(Title).filter_by(emp_no=emp_no, title=title, from_date=from_date).first()
        if title_entry:
            title_entry.to_date = data['to_date']
            try:
                session.commit()
                return {"message": "Title entry updated successfully."}
            except Exception as e:
                session.rollback()
                return {"error": str(e)}, 500
            finally:
                session.close()
        return {"message": "Title entry not found for the provided details."}, 404

    def delete(self, emp_no, title, from_date):
        session = Session()
        title_entry = session.query(Title).filter_by(emp_no=emp_no, title=title, from_date=from_date).first()
        if title_entry:
            try:
                session.delete(title_entry)
                session.commit()
                return {"message": "Title entry deleted successfully."}
            except Exception as e:
                session.rollback()
                return {"error": str(e)}, 500
            finally:
                session.close()
        return {"message": "Title entry not found for the provided details."}, 404

