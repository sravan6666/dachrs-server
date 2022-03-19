from modals.Company import Company
from util.SendEmail import SendEmail
import uuid
from flask_restful import Resource, reqparse, request

from modals.Users import Users

class ValidateLoginResource(Resource):

    parser = reqparse.RequestParser()
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
    

    def post(self):
        #work pending
        data = ValidateLoginResource.parser.parse_args()
        if Company.find_by_uuid(data['companyUUID']):
            result = Users.addUser(data)
            if result['status']:
                accountConfirmationMessage = str(result['otp']) + ' is the account verification code'
                SendEmail.sendEmail(data['email'], "Registration Confirmation", accountConfirmationMessage)
                return ('', 201)
            else:
                return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': 'Invalid request'}, 400, {'Content-Type': 'application/json; charset=utf-8'}

    def get(self):
        companyUUID = request.args.get('companyUUID')
        if companyUUID:
            return Users.find_by_all_user_for_company(companyUUID), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': 'Invalid request'}, 400, {'Content-Type': 'application/json; charset=utf-8'}
