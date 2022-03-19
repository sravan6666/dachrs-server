from modals.Users import Users
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask import jsonify

from security.security import authenticate

class LoginResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    
    def post(self):
        data = LoginResource.parser.parse_args()
        user = authenticate(data["email"], data["password"])
        print('user.........',user)
        if user:
            access_token = create_access_token(user.json(), fresh=True)
            print('access_token.........',access_token)
            refresh_token = create_refresh_token(user.json())
            return {'accessToken':access_token, 'refreshToken': refresh_token}, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': 'Bad credentials'}, 400, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(refresh=True)
    def patch(self):
        print('refresh token')
        identity = get_jwt_identity()
        print(identity)
        user = Users.find_by_user_uuid(identity['id'])
        if user:
            access_token = create_access_token(identity=user.json(), fresh=True)
            return {'accessToken':access_token}, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else: 
            return {'errorMessage':'Bad Request'}, 400, {'Content-Type': 'application/json; charset=utf-8'}