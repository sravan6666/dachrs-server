import uuid
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from modals.Epic import Epic

class EpicResource(Resource):

    @jwt_required(fresh=True)
    def get(self, projectUUID, epicUUID):
        identity = get_jwt_identity()
        epic = Epic.find_by_user_uuid_and_epic_uuid("", projectUUID, epicUUID, identity['companyUUID'], identity['teams'])
        if epic:
            return epic.json() , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': epicUUID+' not found for project - '+projectUUID}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def delete(self, projectUUID, epicUUID):
        identity = get_jwt_identity()
        epic = Epic.find_by_user_uuid_and_epic_uuid("", projectUUID, epicUUID, identity['companyUUID'], identity['teams'])
        if epic:
            Epic.delete_epic_by_epic_uuid(epicUUID)
            return {'message': epicUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': epicUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def patch(self, projectUUID, epicUUID):
        print(request.get_json())
        data = request.get_json()
        identity = get_jwt_identity()
        epic = Epic.find_by_user_uuid_and_epic_uuid("", projectUUID, epicUUID, identity['companyUUID'], identity['teams'])
        if epic:
            Epic.update_epic_by_epic_uuid(epic, data)
            return  Epic.find_by_user_uuid_and_epic_uuid("", projectUUID, epicUUID, identity['companyUUID'], identity['teams']).json(), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': epicUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}
