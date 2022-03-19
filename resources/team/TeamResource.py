import uuid
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, request

from modals.Team import Team

class TeamResource(Resource):


    @jwt_required(fresh=True)
    def get(self, teamUUID):
        identity = get_jwt_identity()
        team = Team.find_by_user_uuid_and_task_uuid("", teamUUID, identity['companyUUID'])
        if team:
            return team.json() , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': teamUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def delete(self, teamUUID):
        identity = get_jwt_identity()
        task = Team.find_by_user_uuid_and_task_uuid("", teamUUID, identity['companyUUID'])
        if task:
            Team.delete_task_by_task_uuid(teamUUID)
            return {'message': teamUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': teamUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def patch(self, teamUUID):
        print(request.get_json())
        data = request.get_json()
        identity = get_jwt_identity()
        task = Team.find_by_user_uuid_and_task_uuid("", teamUUID, identity['companyUUID'])
        if task:
            Team.update_task_by_task_uuid(task, data)
            return  Team.find_by_user_uuid_and_task_uuid("", teamUUID, identity['companyUUID']).json(), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': teamUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}
