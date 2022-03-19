import uuid
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from modals.Project import Project

class ProjectListResource(Resource):

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
    def get(self, boardUUID):
        identity = get_jwt_identity()
        return Project.find_by_user_uuid("", boardUUID, identity['companyUUID'], identity['teams']), 200, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def put(self, boardUUID):
        data = ProjectListResource.parser.parse_args()
        identity = get_jwt_identity()
        data['projectUUID'] = str(uuid.uuid4())
        data['boardUUID'] = boardUUID
        data['companyUUID'] = identity['companyUUID']
        data['teams'] = identity['teams']
        result = Project.addEpic(data)
        if result['status']:
            return ('', 201)
        else:
            return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}

