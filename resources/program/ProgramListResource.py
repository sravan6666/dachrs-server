import uuid
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from modals.Program import Program


class ProgramListResource(Resource):

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
    
    # @jwt_required(fresh=True)
    def get(self):
        identity = get_jwt_identity()
        return Program.find_by_user_uuid("", identity['companyUUID'], identity['teams']), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
    @jwt_required(fresh=True)
    def put(self):
        data = ProgramListResource.parser.parse_args()
        identity = get_jwt_identity()
        data['programUUID'] = str(uuid.uuid4())
        data['companyUUID'] = identity['companyUUID']
        data['teams'] = identity['teams']
        result = Program.addProgram(data)
        if result['status']:
            return ('', 201)
        else:
            return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}

