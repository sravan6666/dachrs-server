from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from modals.Program import Program
import uuid
from flask_restful import Resource, reqparse, request
from modals.Project import Project
from modals.Epic import Epic
from modals.Story import Story
from modals.TaskBoard import TaskBoard

class UserTeamsResource(Resource):

    @jwt_required(fresh=True)
    def get(self):
        identity = get_jwt_identity()
        companyUUID = identity['companyUUID']
        programs=[]
        projects =[]
        epics=[]
        stories=[]
        taskboards = []
        for team in identity['teams']:
            if team:
                programs.append(Program.find_by_user_uuid('', companyUUID, [team]))
                projects.append(Project.findAll_by_user_uuid('', companyUUID, [team]))
                epics.append(Epic.findAll_by_user_uuid('', companyUUID, [team]))
                stories.append(Story.findAll_by_user_uuid('', companyUUID, [team]))
                taskboards.append(TaskBoard.findAll_by_user_uuid('', companyUUID, [team]))
        return {'programs': programs, 'projects': projects, 'epics': epics, 'stories': stories, 'baords': taskboards}, 200, {'Content-Type': 'application/json; charset=utf-8'}
