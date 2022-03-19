import uuid
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from modals.Epic import Epic


class EpicListResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('importance',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('priority',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('startDate',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('endDate',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('archived',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    
    @jwt_required(fresh=True)
    def get(self, projectUUID):
        identity = get_jwt_identity()
        return Epic.find_by_user_uuid("", projectUUID, identity['companyUUID'], identity['teams']), 200, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def put(self, projectUUID):
        data = EpicListResource.parser.parse_args()
        identity = get_jwt_identity()
        data['epicUUID'] = str(uuid.uuid4())
        data['projectUUID'] = projectUUID
        data['companyUUID'] = identity['companyUUID']
        data['teams'] = identity['teams']
        result = Epic.addEpic(data)
        if result['status']:
            return ('', 201)
        else:
            return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}

