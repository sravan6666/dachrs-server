from modals.TaskBoardStatus import TaskBoardStatus
import uuid
from flask_jwt_extended.utils import get_jwt_identity
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from modals.TaskBoard import TaskBoard
from os import environ as env

defaultTaskBoardColumns = env['DEFAULT_TASKBOARD_COLUMNS']

class TaskBoardResource(Resource):

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
    def get(self, storyUUID):
        identity = get_jwt_identity()
        return TaskBoard.find_by_user_uuid("", storyUUID, identity['companyUUID'], identity['teams']), 200, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def put(self, storyUUID):
        data = TaskBoardResource.parser.parse_args()
        identity = get_jwt_identity()
        data['taskBoardUUID'] = str(uuid.uuid4())
        data['storyUUID'] = storyUUID
        data['companyUUID'] = identity['companyUUID']
        data['teams'] = identity['teams']
        result = TaskBoard.addTask(data)
        if result['status']:
            # create 4 task board status Backlog, To-Do, In Progress, Completed
            for column in defaultTaskBoardColumns.split(","):
                taskBoardStatusUUID = str(uuid.uuid4())
                TaskBoardStatus.addTaskStatus({'title': column, 'taskBoardUUID': result['taskBoardUUID'], 'companyUUID': identity['companyUUID'], 'teams': identity['teams'], 'taskBoardStatusUUID': taskBoardStatusUUID})
            return ('', 201)
        else:
            return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}

