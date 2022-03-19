from modals.Company import Company
import uuid
from datetime import datetime

from pymongo import MongoClient, collection
from os import environ as env


mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_PROGRAM_COLLECTION']]

class Program(object):

    program_uuid: uuid
    title: str
    description: str
    importance: str
    priority: str
    start_date: datetime
    end_date: datetime
    archived: bool = False
    company_uuid: uuid
    teams: list

    def find_by_user_uuid(user_uuid, companyUUID, teams):
        epics = []
        
        programMongo = list(collection.find({'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for program in programMongo:
            programObj = Program()
            programObj.program_uuid = program['program_uuid']
            programObj.title = program['title']
            programObj.description = program['description']
            programObj.importance = program['importance']
            programObj.priority = program['priority']
            programObj.start_date = program['start_date']
            programObj.end_date = program['end_date']
            programObj.archived = program['archived']
            programObj.company_uuid = program['company_uuid']
            programObj.teams = program['teams']
            epics.append(programObj.json())
        return epics

    def addProgram(data):
        print(data)
        if data['endDate'] < data['startDate']:
            return {'status': False, 'message':'End date cannot be less than start date'}

        if Program.find_by_title(data['title'], data['companyUUID'], data['teams']):
            print('already exists')
            return {'status': False, 'message':'Title already exists'}
        else:
            print('inserting')
            program = Program.convertJSONToEpic(data)
            collection.insert(program.toMongoJSON())
            return {'status': True}

    def find_by_title(title, companyUUID, teams):
        # add check on user role
        program = collection.find_one({'title': title, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        print(program)
        if program:
            return Program.convertMongoJSONToEpic(program).json()
        else:
            return None

    def find_by_user_uuid_and_program_uuid(user_uuid, program_uuid, companyUUID, teams):
        program = collection.find_one({'program_uuid': program_uuid, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        # add validation when we have JWT on user_uuid and board_uuid
        if program:
            return Program.convertMongoJSONToEpic(program)
        return None

    def delete_program_by_program_uuid(program_uuid):
        program = collection.delete_one({'program_uuid': program_uuid})
        # add validation when we have JWT on user_uuid and board_uuid
        return program

    def update_epic_by_program_uuid(program, inputRequest):
        print('before -')
        print(program)
        if inputRequest.get('title'):
            program.title = inputRequest.get('title')
        if inputRequest.get('description'):
            program.description = inputRequest.get('description')
        if inputRequest.get('importance'):
            program.importance = inputRequest.get('importance')
        if inputRequest.get('priority'):
            program.priority = inputRequest.get('priority')
        if inputRequest.get('startDate'):
            program.start_date = inputRequest.get('startDate')
        if inputRequest.get('endDate'):
            program.end_date = inputRequest.get('endDate')
        if inputRequest.get('teams'):
            program.teams = inputRequest.get('teams', [])
        if inputRequest.get('archived') is not program.archived:
            program.archived = inputRequest.get('archived')

        print('afetr -')
        print(program.toMongoJSON())
        result = collection.update_one({'program_uuid': program.program_uuid}, {'$set': program.toMongoJSON()})
        return result.modified_count

    def convertMongoJSONToEpic(program):
        programObj = Program()
        programObj.program_uuid = program['program_uuid']
        programObj.title = program['title']
        programObj.description = program['description']
        programObj.importance = program['importance']
        programObj.priority = program['priority']
        programObj.start_date = program['start_date']
        programObj.end_date = program['end_date']
        programObj.archived = program['archived']
        programObj.company_uuid = program['company_uuid']
        programObj.teams = program['teams']
        return programObj

    def convertJSONToEpic(program):
        programObj = Program()
        programObj.program_uuid = program['programUUID']
        programObj.title = program['title']
        programObj.description = program['description']
        programObj.importance = program['importance']
        programObj.priority = program['priority']
        programObj.start_date = program['startDate']
        programObj.end_date = program['endDate']
        programObj.archived = program['archived']
        programObj.company_uuid = program['companyUUID']
        programObj.teams = program['teams']
        return programObj   

    def json(self):
        return {
            'programUUID': self.program_uuid,
            'title': self.title,
            'description': self.description,
            'importance': self.importance,
            'priority': self.priority,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'archived': self.archived,
            'companyUUID': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None

        }

    def toMongoJSON(self):
        return {
            'program_uuid': self.program_uuid,
            'title': self.title,
            'description': self.description,
            'importance': self.importance,
            'priority': self.priority,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'archived': self.archived,
            'company_uuid': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }