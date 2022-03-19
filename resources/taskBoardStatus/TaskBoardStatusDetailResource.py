import uuid
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, request

from modals.TaskBoardStatus import TaskBoardStatus

class TaskBoardStatusDetailResource(Resource):

    @jwt_required(fresh=True)
    def delete(self, taskBoardUUID, taskBoardStatusUUID):
        identity = get_jwt_identity()
        task = TaskBoardStatus.find_by_user_uuid_and_task_uuid("", taskBoardUUID, taskBoardStatusUUID, identity['companyUUID'], identity['teams'])
        if task:
            TaskBoardStatus.delete_task_by_task_uuid(taskBoardStatusUUID)
            return {'message': taskBoardStatusUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': taskBoardStatusUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def patch(self, taskBoardUUID, taskBoardStatusUUID):
        print(request.get_json())
        data = request.get_json()
        identity = get_jwt_identity()
        task = TaskBoardStatus.find_by_user_uuid_and_task_uuid("", taskBoardUUID, taskBoardStatusUUID, identity['companyUUID'], identity['teams'])
        if task:
            TaskBoardStatus.update_task_by_task_uuid(task, data)
            return  TaskBoardStatus.find_by_user_uuid_and_task_uuid("", taskBoardUUID, taskBoardStatusUUID, identity['companyUUID'], identity['teams']).json(), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': taskBoardStatusUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}
