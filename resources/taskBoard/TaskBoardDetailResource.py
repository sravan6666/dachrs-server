import uuid
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, request

from modals.TaskBoard import TaskBoard

class TaskBoardDetailResource(Resource):

    @jwt_required(fresh=True)
    def delete(self, storyUUID, taskBoardUUID):
        identity = get_jwt_identity()
        task = TaskBoard.find_by_user_uuid_and_task_uuid("", storyUUID, taskBoardUUID, identity['companyUUID'], identity['teams'])
        if task:
            TaskBoard.delete_task_by_task_uuid(taskBoardUUID)
            return {'message': taskBoardUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': taskBoardUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def patch(self, storyUUID, taskBoardUUID):
        print(request.get_json())
        data = request.get_json()
        identity = get_jwt_identity()
        task = TaskBoard.find_by_user_uuid_and_task_uuid("", storyUUID, taskBoardUUID, identity['companyUUID'], identity['teams'])
        if task:
            TaskBoard.update_task_by_task_uuid(task, data)
            return  TaskBoard.find_by_user_uuid_and_task_uuid("", storyUUID, taskBoardUUID, identity['companyUUID'], identity['teams']).json(), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': taskBoardUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}
