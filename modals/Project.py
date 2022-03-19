import uuid
from datetime import datetime

from pymongo import MongoClient, collection
from os import environ as env


mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_PROJECT_COLLECTION']]

class Project(object):

    project_uuid: uuid
    title: str
    description: str
    importance: str
    priority: str
    start_date: datetime
    end_date: datetime
    board_uuid: uuid
    archived: bool = False
    company_uuid: uuid
    teams: list

    def find_by_user_uuid(user_uuid, boardUUID, companyUUID, teams):
        epics = []
        
        projectsMongo = list(collection.find({'board_uuid': boardUUID, 'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for project in projectsMongo:
            projectObj = Project()
            projectObj.project_uuid = project['project_uuid']
            projectObj.title = project['title']
            projectObj.description = project['description']
            projectObj.importance = project['importance']
            projectObj.priority = project['priority']
            projectObj.start_date = project['start_date']
            projectObj.end_date = project['end_date']
            projectObj.board_uuid = project['board_uuid']
            projectObj.archived = project['archived']
            projectObj.company_uuid = project['company_uuid']
            projectObj.teams = project['teams']
            epics.append(projectObj.json())
        return epics

    def findAll_by_user_uuid(user_uuid, companyUUID, teams):
        epics = []
        
        projectsMongo = list(collection.find({'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for project in projectsMongo:
            projectObj = Project()
            projectObj.project_uuid = project['project_uuid']
            projectObj.title = project['title']
            projectObj.description = project['description']
            projectObj.importance = project['importance']
            projectObj.priority = project['priority']
            projectObj.start_date = project['start_date']
            projectObj.end_date = project['end_date']
            projectObj.board_uuid = project['board_uuid']
            projectObj.archived = project['archived']
            projectObj.company_uuid = project['company_uuid']
            projectObj.teams = project['teams']
            epics.append(projectObj.json())
        return epics

    def addEpic(data):
        print(data)
        if data['endDate'] < data['startDate']:
            return {'status': False, 'message':'End date cannot be less than start date'}

        if Project.find_by_title_and_board_uuid(data['title'], data['boardUUID'], data['companyUUID'], data['teams']):
            print('already exists')
            return {'status': False, 'message':'Title already exists'}
        else:
            print('inserting')
            project = Project.convertJSONToEpic(data)
            collection.insert(project.toMongoJSON())
            return {'status': True}

    def find_by_title_and_board_uuid(title, boardUUID, companyUUID, teams):
        # add check on user role
        project = collection.find_one({'title': title, 'board_uuid': boardUUID, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        print(project)
        if project:
            return Project.convertMongoJSONToEpic(project).json()
        else:
            return None

    def find_by_user_uuid_and_project_uuid(user_uuid, boardUUID, project_uuid, companyUUID, teams):
        project = collection.find_one({'board_uuid': boardUUID, 'project_uuid': project_uuid, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        # add validation when we have JWT on user_uuid and board_uuid
        if project:
            return Project.convertMongoJSONToEpic(project)
        return None

    def delete_project_by_board_uuid(project_uuid):
        project = collection.delete_one({'project_uuid': project_uuid})
        # add validation when we have JWT on user_uuid and board_uuid
        return project

    def update_epic_by_project_uuid(project, inputRequest):
        print('before -')
        print(project)
        if inputRequest.get('title'):
            project.title = inputRequest.get('title')
        if inputRequest.get('description'):
            project.description = inputRequest.get('description')
        if inputRequest.get('importance'):
            project.importance = inputRequest.get('importance')
        if inputRequest.get('priority'):
            project.priority = inputRequest.get('priority')
        if inputRequest.get('startDate'):
            project.start_date = inputRequest.get('startDate')
        if inputRequest.get('endDate'):
            project.end_date = inputRequest.get('endDate')
        if inputRequest.get('archived') is not project.archived:
            project.archived = inputRequest.get('archived')
        if inputRequest.get('teams'):
            project.teams = inputRequest.get('teams')
            
        print('afetr -')
        print(project.toMongoJSON())
        result = collection.update_one({'project_uuid': project.project_uuid}, {'$set': project.toMongoJSON()})
        return result.modified_count

    def convertMongoJSONToEpic(project):
        projectObj = Project()
        projectObj.project_uuid = project['project_uuid']
        projectObj.title = project['title']
        projectObj.description = project['description']
        projectObj.importance = project['importance']
        projectObj.priority = project['priority']
        projectObj.start_date = project['start_date']
        projectObj.end_date = project['end_date']
        projectObj.board_uuid = project['board_uuid']
        projectObj.archived = project['archived']
        projectObj.company_uuid = project['company_uuid']
        projectObj.teams = project['teams']
        return projectObj

    def convertJSONToEpic(project):
        projectObj = Project()
        projectObj.project_uuid = project['projectUUID']
        projectObj.title = project['title']
        projectObj.description = project['description']
        projectObj.importance = project['importance']
        projectObj.priority = project['priority']
        projectObj.start_date = project['startDate']
        projectObj.end_date = project['endDate']
        projectObj.board_uuid = project['boardUUID']
        projectObj.archived = project['archived']
        projectObj.company_uuid = project['companyUUID']
        projectObj.teams = project['teams']
        return projectObj   

    def json(self):
        return {
            'projectUUID': self.project_uuid,
            'title': self.title,
            'description': self.description,
            'importance': self.importance,
            'priority': self.priority,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'boardUUID': self.board_uuid,
            'archived': self.archived,
            'companyUUID': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }

    def toMongoJSON(self):
        return {
            'project_uuid': self.project_uuid,
            'title': self.title,
            'description': self.description,
            'importance': self.importance,
            'priority': self.priority,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'board_uuid': self.board_uuid,
            'archived': self.archived,
            'company_uuid': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }