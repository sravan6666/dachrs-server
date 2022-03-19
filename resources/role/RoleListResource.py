import uuid
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from modals.Roles import Roles

class RoleListResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self):
        return Roles.get_all_roles(), 200, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def put(self):
        data = RoleListResource.parser.parse_args()
        data['roleUUID'] = str(uuid.uuid4())
        result = Roles.addRole(data)
        if result['status']:
            return ('', 201)
        else:
            return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}

