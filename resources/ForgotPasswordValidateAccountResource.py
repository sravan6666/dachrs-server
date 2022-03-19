from modals.Users import Users
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import jsonify

from security.security import authenticate

class ForgotPasswordValidateAccountResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = ForgotPasswordValidateAccountResource.parser.parse_args()
        user = Users.find_by_email(data["email"])
        print(user)
        if user:
            response = Users.forgot_password_validate_account(Users.convertJSONToUser(user, False))
            return response, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': 'Bad credentials'}, 400, {'Content-Type': 'application/json; charset=utf-8'}
