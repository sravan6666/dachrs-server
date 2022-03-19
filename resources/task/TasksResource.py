import uuid
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, request

from modals.Tasks import Tasks

class TasksResource(Resource):

    @jwt_required(fresh=True)
    def get(self, taskBoardStatusUUID, taskUUID):
        identity = get_jwt_identity()
        task = Tasks.find_by_user_uuid_and_task_uuid("", taskBoardStatusUUID, taskUUID, identity['companyUUID'], identity['teams'])
        if task:
            return task.json() , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': taskUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def delete(self, taskBoardStatusUUID, taskUUID):
        identity = get_jwt_identity()
        task = Tasks.find_by_user_uuid_and_task_uuid("", taskBoardStatusUUID, taskUUID, identity['companyUUID'], identity['teams'])
        if task:
            Tasks.delete_task_by_task_uuid(taskUUID)
            return {'message': taskUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': taskUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def patch(self, taskBoardStatusUUID, taskUUID):
        print(request.get_json())
        data = request.get_json()
        identity = get_jwt_identity()
        task = Tasks.find_by_user_uuid_and_task_uuid("", taskBoardStatusUUID, taskUUID, identity['companyUUID'], identity['teams'])
        if task:
            Tasks.update_task_by_task_uuid(task, data)
            return  {'message': taskUUID+' updated successfully'}, 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': taskUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}
