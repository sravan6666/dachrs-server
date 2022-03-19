import uuid
from flask_jwt_extended.utils import get_jwt_identity
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from modals.TaskBoardStatus import TaskBoardStatus

class TaskBoardStatusResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title',
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
    def get(self, taskBoardUUID):
        identity = get_jwt_identity()
        return TaskBoardStatus.find_by_user_uuid("", taskBoardUUID, identity['companyUUID'], identity['teams']), 200, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def put(self, taskBoardUUID):
        data = TaskBoardStatusResource.parser.parse_args()
        identity = get_jwt_identity()
        data['taskBoardStatusUUID'] = str(uuid.uuid4())
        data['taskBoardUUID'] = taskBoardUUID
        data['companyUUID'] = identity['companyUUID']
        data['teams'] = identity['teams']
        result = TaskBoardStatus.addTaskStatus(data)
        if result['status']:
            return ('', 201)
        else:
            return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}

