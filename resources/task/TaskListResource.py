import uuid
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from modals.Tasks import Tasks

class TaskListResource(Resource):

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
    parser.add_argument('userUUID',
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
    parser.add_argument('status',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('file',
                        type=dict,
                        required=False,
                        help="This field cannot be left blank!"
                        )
                        
                        
    @jwt_required(fresh=True)
    def get(self, taskBoardStatusUUID):
        identity = get_jwt_identity()
        return Tasks.find_by_user_uuid("", taskBoardStatusUUID, identity['companyUUID'], identity['teams']), 200, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def put(self, taskBoardStatusUUID):
        data = TaskListResource.parser.parse_args()
        identity = get_jwt_identity()
        data['taskUUID'] = str(uuid.uuid4())
        data['taskBoardStatusUUID'] = taskBoardStatusUUID
        data['companyUUID'] = identity['companyUUID']
        data['teams'] = identity['teams']
        result = Tasks.addTask(data)
        if result['status']:
            return ('', 201)
        else:
            return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}

