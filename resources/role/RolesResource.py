import uuid
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from modals.Roles import Roles

class RolesResource(Resource):

    @jwt_required(fresh=True)
    def get(self, roleUUID):
        task = Roles.find_by_uuid(roleUUID)
        if task:
            return task.json() , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': roleUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def delete(self, roleUUID):
        task = Roles.find_by_uuid(roleUUID)
        if task:
            Roles.delete_task_by_role_uuid(roleUUID)
            return {'message': roleUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': roleUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}
