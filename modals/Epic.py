import uuid
from datetime import datetime

from pymongo import MongoClient, collection
from os import environ as env


mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_EPIC_COLLECTION']]

class Epic(object):

    epic_uuid: uuid
    title: str
    description: str
    importance: str
    priority: str
    start_date: datetime
    end_date: datetime
    project_uuid: uuid
    archived: bool = False
    company_uuid: uuid
    teams: list
    

    def find_by_user_uuid(user_uuid, projectUUID, companyUUID, teams):
        epics = []
        
        epicsMongo = list(collection.find({'project_uuid': projectUUID, 'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for epic in epicsMongo:
            epicObj = Epic()
            epicObj.epic_uuid = epic['epic_uuid']
            epicObj.title = epic['title']
            epicObj.description = epic['description']
            epicObj.importance = epic['importance']
            epicObj.priority = epic['priority']
            epicObj.start_date = epic['start_date']
            epicObj.end_date = epic['end_date']
            epicObj.project_uuid = epic['project_uuid']
            epicObj.archived = epic['archived']
            epicObj.company_uuid = epic['company_uuid']
            epicObj.teams = epic['teams']
            epics.append(epicObj.json())
        return epics

    def findAll_by_user_uuid(user_uuid, companyUUID, teams):
        epics = []
        
        epicsMongo = list(collection.find({'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for epic in epicsMongo:
            epicObj = Epic()
            epicObj.epic_uuid = epic['epic_uuid']
            epicObj.title = epic['title']
            epicObj.description = epic['description']
            epicObj.importance = epic['importance']
            epicObj.priority = epic['priority']
            epicObj.start_date = epic['start_date']
            epicObj.end_date = epic['end_date']
            epicObj.project_uuid = epic['project_uuid']
            epicObj.archived = epic['archived']
            epicObj.company_uuid = epic['company_uuid']
            epicObj.teams = epic['teams']
            epics.append(epicObj.json())
        return epics


    def addEpic(data):
        print(data)
        if data['endDate'] < data['startDate']:
            return {'status': False, 'message':'End date cannot be less than start date'}

        if Epic.find_by_title_and_project_uuid(data['title'], data['projectUUID'], data['companyUUID'], data['teams']):
            print('already exists')
            return {'status': False, 'message':'Title already exists'}
        else:
            print('inserting')
            epic = Epic.convertJSONToEpic(data)
            collection.insert(epic.toMongoJSON())
            return {'status': True}

    def find_by_title_and_project_uuid(title, projectUUID, companyUUID, teams):
        # add check on user role
        epic = collection.find_one({'title': title, 'project_uuid': projectUUID, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        print(epic)
        if epic:
            return Epic.convertMongoJSONToEpic(epic).json()
        else:
            return None

    def find_by_user_uuid_and_epic_uuid(user_uuid, projectUUID, epic_uuid, companyUUID, teams):
        epic = collection.find_one({'epic_uuid': epic_uuid, 'project_uuid': projectUUID, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        # add validation when we have JWT on user_uuid and board_uuid
        if epic:
            return Epic.convertMongoJSONToEpic(epic)
        return None

    def delete_epic_by_epic_uuid(epic_uuid):
        epic = collection.delete_one({'epic_uuid': epic_uuid})
        # add validation when we have JWT on user_uuid and board_uuid
        return epic

    def update_epic_by_epic_uuid(epic, inputRequest):
        print('before -')
        print(epic)
        if inputRequest.get('title'):
            epic.title = inputRequest.get('title')
        if inputRequest.get('description'):
            epic.description = inputRequest.get('description')
        if inputRequest.get('importance'):
            epic.importance = inputRequest.get('importance')
        if inputRequest.get('priority'):
            epic.priority = inputRequest.get('priority')
        if inputRequest.get('startDate'):
            epic.start_date = inputRequest.get('startDate')
        if inputRequest.get('endDate'):
            epic.end_date = inputRequest.get('endDate')
        if inputRequest.get('archived') is not epic.archived:
            epic.archived = inputRequest.get('archived')
        if inputRequest.get('teams'):
            epic.teams = inputRequest.get('teams')
            
        print('afetr -')
        print(epic.toMongoJSON())
        result = collection.update_one({'epic_uuid': epic.epic_uuid}, {'$set': epic.toMongoJSON()})
        return result.modified_count

    def convertMongoJSONToEpic(epic):
        epicObj = Epic()
        epicObj.epic_uuid = epic['epic_uuid']
        epicObj.title = epic['title']
        epicObj.description = epic['description']
        epicObj.importance = epic['importance']
        epicObj.priority = epic['priority']
        epicObj.start_date = epic['start_date']
        epicObj.end_date = epic['end_date']
        epicObj.project_uuid = epic['project_uuid']
        epicObj.archived = epic['archived']
        epicObj.company_uuid = epic['company_uuid']
        epicObj.teams = epic['teams']
        return epicObj

    def convertJSONToEpic(epic):
        epicObj = Epic()
        epicObj.epic_uuid = epic['epicUUID']
        epicObj.title = epic['title']
        epicObj.description = epic['description']
        epicObj.importance = epic['importance']
        epicObj.priority = epic['priority']
        epicObj.start_date = epic['startDate']
        epicObj.end_date = epic['endDate']
        epicObj.project_uuid = epic['projectUUID']
        epicObj.archived = epic['archived']
        epicObj.company_uuid = epic['companyUUID']
        epicObj.teams = epic['teams']
        return epicObj   

    def json(self):
        return {
            'epicUUID': self.epic_uuid,
            'title': self.title,
            'description': self.description,
            'importance': self.importance,
            'priority': self.priority,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'projectUUID': self.project_uuid,
            'archived': self.archived,
            'companyUUID': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }

    def toMongoJSON(self):
        return {
            'epic_uuid': self.epic_uuid,
            'title': self.title,
            'description': self.description,
            'importance': self.importance,
            'priority': self.priority,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'project_uuid': self.project_uuid,
            'archived': self.archived,
            'company_uuid': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }