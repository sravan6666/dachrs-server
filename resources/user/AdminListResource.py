from modals.Company import Company
from util.SendEmail import SendEmail
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
import uuid
from flask_restful import Resource, reqparse, request

from modals.Users import Users

class AdminListResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    
    @jwt_required(fresh=True)
    def put(self):
        data = AdminListResource.parser.parse_args()
        identity = get_jwt_identity()
        data['userUUID'] = str(uuid.uuid4())
        data['companyUUID'] = identity['companyUUID']
        data['teams'] = identity['teams']
        if Company.find_by_uuid(data['companyUUID']):
            result = Users.addUserByAdmin(data)
            if result['status']:
                accountConfirmationMessage = result['pwd'] + ' is your temprary account login code. Please reset your account password post login.'
                SendEmail.sendEmail(data['email'], "Account Registration Confirmation", accountConfirmationMessage)
                return ('', 201)
            else:
                return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': 'Invalid request'}, 400, {'Content-Type': 'application/json; charset=utf-8'}
