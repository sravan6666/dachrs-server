from modals.Company import Company
from util.SendEmail import SendEmail
import uuid
from flask_restful import Resource, reqparse

from modals.Users import Users

class CompanyListResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    
    def put(self):
        data = CompanyListResource.parser.parse_args()
        data['companyUUID'] = str(uuid.uuid4())
        result = Company.addCompany(data)
        if result['status']:
            return ('', 201)
        else:
            return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}

    def get(self):
        return Company.find_all_company(""), 200, {'Content-Type': 'application/json; charset=utf-8'}

