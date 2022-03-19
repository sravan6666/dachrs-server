from pymongo.message import _EMPTY
from modals.Users import Users
from flask_restful import Resource, reqparse, request

class ConfirmAccountResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('token',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = ConfirmAccountResource.parser.parse_args()
        print(data)
        user = Users.find_by_user_uuid_and_token(data["email"], data["token"])
        print(user)
        if user:
            Users.update_user(user, {'isActive': True})
            return {'message':'User activated'}, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': 'Bad credentials'}, 400, {'Content-Type': 'application/json; charset=utf-8'}


    def patch(self):
        inputBody = request.get_json()
        print(inputBody)
        print(inputBody['email'])
        if inputBody['email']:
            response = Users.resend_verification_token(inputBody['email'])
            if response['errorMessage']:
                return response, 400, {'Content-Type': 'application/json; charset=utf-8'}
            else:
                return response, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': 'invalid request'}, 400, {'Content-Type': 'application/json; charset=utf-8'}
        
