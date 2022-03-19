from modals.Team import Team
import uuid
from flask_jwt_extended.utils import get_jwt_identity
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from modals.TaskBoardStatus import TaskBoardStatus

class TeamListResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('members',
                        type=list,
                        required=True,
                        help="This field cannot be left blank!"
                        )
                        
                        
    @jwt_required(fresh=True)
    def get(self):
        identity = get_jwt_identity()
        return Team.find_by_user_uuid("", identity['companyUUID']), 200, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def put(self):
        data = TeamListResource.parser.parse_args()
        identity = get_jwt_identity()
        data['teamUUID'] = str(uuid.uuid4())
        data['companyUUID'] = identity['companyUUID']
        result = Team.addTeam(data)
        if result['status']:
            return (result['teamUUID'], 201)
        else:
            return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}

