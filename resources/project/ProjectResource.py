from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from modals.Project import Project

class ProjectResource(Resource):

    @jwt_required(fresh=True)
    def get(self, boardUUID, projectUUID):
        identity = get_jwt_identity()
        project = Project.find_by_user_uuid_and_project_uuid("", boardUUID, projectUUID, identity['companyUUID'], identity['teams'])
        if project:
            return project.json() , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': projectUUID+' not found for board - '+boardUUID}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def delete(self, boardUUID, projectUUID):
        identity = get_jwt_identity()
        project = Project.find_by_user_uuid_and_project_uuid("", boardUUID, projectUUID, identity['companyUUID'], identity['teams'])
        if project:
            Project.delete_project_by_board_uuid(projectUUID)
            return {'message': projectUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': projectUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def patch(self, boardUUID, projectUUID):
        print(request.get_json())
        data = request.get_json()
        identity = get_jwt_identity()
        project = Project.find_by_user_uuid_and_project_uuid("", boardUUID, projectUUID, identity['companyUUID'], identity['teams'])
        if project:
            Project.update_epic_by_project_uuid(project, data)
            return  Project.find_by_user_uuid_and_project_uuid("", boardUUID, projectUUID, identity['companyUUID'], identity['teams']).json(), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': projectUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}
