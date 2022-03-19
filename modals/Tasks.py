from util.BlobStorage import BlobStorage
import uuid
from datetime import datetime

from pymongo import MongoClient, collection
from os import environ as env

mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_TASKS_COLLECTION']]

class Tasks(object):

    task_uuid: uuid
    title: str
    description: str
    user_uuid: uuid
    importance: str
    priority: str
    start_date: datetime
    end_date: datetime
    task_board_status_uuid: uuid
    archived: bool = False
    status: str
    company_uuid: uuid
    teams: list
    attachments: list
        
    def find_by_user_uuid(userUUID, taskBoardStatusUUID, companyUUID, teams):
        tasks = []
        
        tasksMongo = list(collection.find({'task_board_status_uuid': taskBoardStatusUUID, 'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for task in tasksMongo:
            taskObj = Tasks()
            taskObj.task_uuid = task['task_uuid']
            taskObj.title = task['title']
            taskObj.description = task['description']
            taskObj.user_uuid = task['user_uuid']
            taskObj.importance = task['importance']
            taskObj.priority = task['priority']
            taskObj.start_date = task['start_date']
            taskObj.end_date = task['end_date']
            taskObj.task_board_status_uuid = task['task_board_status_uuid']
            taskObj.archived = task['archived']
            taskObj.company_uuid = task['company_uuid']
            taskObj.teams = task['teams']
            taskObj.attachments = task.get('attachments', [])
            tasks.append(taskObj.json())
        return tasks

    def addTask(data):
        print(data)
        if data['endDate'] < data['startDate']:
            return {'status': False, 'message':'End date cannot be less than start date'}

        if Tasks.find_by_title_and_task_board_uuid(data['title'], data['taskBoardStatusUUID'], data['companyUUID'], data['teams']):
            print('already exists')
            return {'status': False, 'message':'Title already exists'}
        else:
            print('inserting')
            BlobStorage.uploadFile(data['taskUUID'],data['file']['name'],data['file']['blob'])
            task = Tasks.convertJSONToTask(data)
            task.attachments.append(data['file']['name'])
            collection.insert(task.toMongoJSON())
            return {'status': True}
        

    def find_by_title_and_task_board_uuid(title, task_board_status_uuid, companyUUID, teams):
        task = collection.find_one({'title': title, 'task_board_status_uuid': task_board_status_uuid, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        print(task)
        if task:
            return Tasks.convertMongoJSONToTask(task).json()
        else:
            return None

    def find_by_user_uuid_and_task_uuid(user_uuid, taskBoardStatusUUID, task_uuid, companyUUID, teams):
        task = collection.find_one({'task_board_status_uuid': taskBoardStatusUUID, 'task_uuid': task_uuid, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        # add validation when we have JWT on user_uuid and task_board_status_uuid
        if task:
            return Tasks.convertMongoJSONToTask(task)
        return None

    def delete_task_by_task_uuid(task_uuid):
        task = collection.delete_one({'task_uuid': task_uuid})
        # add validation when we have JWT on user_uuid and task_board_status_uuid
        return task

    def update_task_by_task_uuid(task, inputRequest):
        print('before -')
        print(task)
        if inputRequest.get('title'):
            task.title = inputRequest.get('title')
        if inputRequest.get('description'):
            task.description = inputRequest.get('description')
        if inputRequest.get('userUUID'):
            task.user_uuid = inputRequest.get('userUUID')
        if inputRequest.get('importance'):
            task.importance = inputRequest.get('importance')
        if inputRequest.get('priority'):
            task.priority = inputRequest.get('priority')
        if inputRequest.get('startDate'):
            task.start_date = inputRequest.get('startDate')
        if inputRequest.get('endDate'):
            task.end_date = inputRequest.get('endDate')
        if inputRequest.get('taskBoardStatusUUID'):
            task.task_board_status_uuid = inputRequest.get('taskBoardStatusUUID')
        if inputRequest.get('teams'):
            task.teams = inputRequest.get('teams')
        if inputRequest.get('archived') is not task.archived:
            task.archived = inputRequest.get('archived')
        
        print('afetr -')
        print(task.toMongoJSON())
        result = collection.update_one({'task_uuid': task.task_uuid}, {'$set': task.toMongoJSON()})
        return result.modified_count

    def convertMongoJSONToTask(task):
        taskObj = Tasks()
        taskObj.task_uuid = task['task_uuid']
        taskObj.title = task['title']
        taskObj.description = task['description']
        taskObj.user_uuid = task['user_uuid']
        taskObj.importance = task['importance']
        taskObj.priority = task['priority']
        taskObj.start_date = task['start_date']
        taskObj.end_date = task['end_date']
        taskObj.task_board_status_uuid = task['task_board_status_uuid']
        taskObj.archived = task['archived']
        taskObj.company_uuid = task['company_uuid']
        taskObj.teams = task['teams']
        taskObj.attachments = task.get('attachments', [])
        return taskObj

    def convertJSONToTask(task):
        taskObj = Tasks()
        taskObj.task_uuid = task['taskUUID']
        taskObj.title = task['title']
        taskObj.description = task['description']
        taskObj.user_uuid = task['userUUID']
        taskObj.importance = task['importance']
        taskObj.priority = task['priority']
        taskObj.start_date = task['startDate']
        taskObj.end_date = task['endDate']
        taskObj.task_board_status_uuid = task['taskBoardStatusUUID']
        taskObj.archived = task['archived']
        taskObj.company_uuid = task['companyUUID']
        taskObj.teams = task['teams']
        taskObj.attachments = task.get('attachments', [])
        return taskObj   

    def json(self):
        return {
            'taskUUID': self.task_uuid,
            'title': self.title,
            'description': self.description,
            'userUUID': self.user_uuid,
            'importance': self.importance,
            'priority': self.priority,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'taskBoardStatusUUID': self.task_board_status_uuid,
            'archived' : self.archived,
            'companyUUID': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None,
            'attachments': self.attachments if hasattr(self, 'attachments') else []
        }

    def toMongoJSON(self):
        return {
            'task_uuid': self.task_uuid,
            'title': self.title,
            'description': self.description,
            'user_uuid': self.user_uuid,
            'importance': self.importance,
            'priority': self.priority,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'task_board_status_uuid': self.task_board_status_uuid,
            'archived' : self.archived,
            'company_uuid': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None,
            'attachments': self.attachments if hasattr(self, 'attachments') else []
        }
