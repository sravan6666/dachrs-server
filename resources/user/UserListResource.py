from modals.Company import Company
from util.SendEmail import SendEmail
import uuid
from flask_restful import Resource, reqparse, request

from modals.Users import Users

class UserListResource(Resource):

    parser = reqparse.RequestParser()
    # parser.add_argument('name',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be left blank!"
    #                     )
    # parser.add_argument('username',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be left blank!"
    #                     )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('roleUUID',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    # parser.add_argument('company',
    #                     type=str,
    #                     required=False,
    #                     help="This field cannot be left blank!"
    #                     )
    # parser.add_argument('companyUUID',
    #                     type=str,
    #                     required=False,
    #                     help="This field cannot be left blank!"
    #                     )
    parser.add_argument('phone',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('website',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('teams',
                        type=list,
                        required=True,
                        help="This field cannot be left blank!"
                        )
                        

    def put(self):
        data = UserListResource.parser.parse_args()
        data['userUUID'] = str(uuid.uuid4())
        if data:
            result = Users.addUser(data)
            print('result......', result)
            if result['status']:
                accountConfirmationMessage = str(result['otp']) + ' is the account verification code'
                SendEmail.sendEmail(data['email'], "Registration Confirmation", accountConfirmationMessage)
                return (result, 200)
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
