import uuid

from pymongo import MongoClient, collection
from os import environ as env

mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_TASKBOARDSTATUS_COLLECTION']]

class TaskBoardStatus(object):

    task_board_status_uuid: uuid
    title: str
    task_board_uuid: uuid
    archived: bool = False
    company_uuid: uuid
    teams: list
        
    def find_by_user_uuid(userUUID, taskBoardUUID, companyUUID, teams):
        taskBoards = []
        
        taskBoardMongo = list(collection.find({'task_board_uuid': taskBoardUUID, 'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for taskBoard in taskBoardMongo:
            taskBoardObj = TaskBoardStatus()
            taskBoardObj.task_board_status_uuid = taskBoard['task_board_status_uuid']
            taskBoardObj.title = taskBoard['title']
            taskBoardObj.task_board_uuid = taskBoard['task_board_uuid']
            taskBoardObj.archived = taskBoard['archived']
            taskBoardObj.company_uuid = taskBoard['company_uuid']
            taskBoardObj.teams = taskBoard['teams']
            taskBoards.append(taskBoardObj.json())
        return taskBoards

    def addTaskStatus(data):
        print(data)
        if TaskBoardStatus.find_by_title_and_status_uuid(data['title'], data['taskBoardUUID'], data['companyUUID'], data['teams']):
            print('already exists')
            return {'status': False, 'message':'Title already exists'}
        else:
            print('inserting')
            taskBoard = TaskBoardStatus.convertJSONToTask(data)
            collection.insert(taskBoard.toMongoJSON())
            return {'status': True}
        

    def find_by_title_and_status_uuid(title, task_board_uuid, companyUUID, teams):
        taskBoard = collection.find_one({'title': title, 'task_board_uuid': task_board_uuid, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        print(taskBoard)
        if taskBoard:
            return TaskBoardStatus.convertMongoJSONToTask(taskBoard).json()
        else:
            return None

    def find_by_user_uuid_and_task_uuid(user_uuid, taskBoardStatusUUID, task_board_status_uuid, companyUUID, teams):
        taskBoard = collection.find_one({'task_board_uuid': taskBoardStatusUUID, 'task_board_status_uuid': task_board_status_uuid, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        # add validation when we have JWT on user_uuid and task_board_uuid
        if taskBoard:
            return TaskBoardStatus.convertMongoJSONToTask(taskBoard)
        return None

    def delete_task_by_task_uuid(task_board_status_uuid):
        taskBoard = collection.delete_one({'task_board_status_uuid': task_board_status_uuid})
        # add validation when we have JWT on user_uuid and task_board_uuid
        return taskBoard

    def update_task_by_task_uuid(taskBoard, inputRequest):
        print('before -')
        print(taskBoard)
        if inputRequest.get('title'):
            taskBoard.title = inputRequest.get('title')
        if inputRequest.get('taskBoardStatusUUID'):
            taskBoard.task_board_uuid = inputRequest.get('taskBoardStatusUUID')
        if inputRequest.get('teams'):
            taskBoard.teams = inputRequest.get('teams')
        if inputRequest.get('archived') is not taskBoard.archived:
            taskBoard.archived = inputRequest.get('archived')
        
        print('afetr -')
        print(taskBoard.toMongoJSON())
        result = collection.update_one({'task_board_status_uuid': taskBoard.task_board_status_uuid}, {'$set': taskBoard.toMongoJSON()})
        return result.modified_count

    def convertMongoJSONToTask(taskBoard):
        taskBoardObj = TaskBoardStatus()
        taskBoardObj.task_board_status_uuid = taskBoard['task_board_status_uuid']
        taskBoardObj.title = taskBoard['title']
        taskBoardObj.task_board_uuid = taskBoard['task_board_uuid']
        taskBoardObj.archived = taskBoard['archived']
        taskBoardObj.company_uuid = taskBoard['company_uuid']
        taskBoardObj.teams = taskBoard['teams']
        return taskBoardObj

    def convertJSONToTask(taskBoard):
        taskBoardObj = TaskBoardStatus()
        taskBoardObj.task_board_status_uuid = taskBoard['taskBoardStatusUUID']
        taskBoardObj.title = taskBoard['title']
        taskBoardObj.task_board_uuid = taskBoard['taskBoardUUID']
        taskBoardObj.archived = taskBoard.get('archived', None)
        taskBoardObj.company_uuid = taskBoard['companyUUID']
        taskBoardObj.teams = taskBoard['teams']
        return taskBoardObj   

    def json(self):
        return {
            'taskBoardUUID': self.task_board_uuid,
            'title': self.title,
            'taskBoardStatusUUID': self.task_board_status_uuid,
            'archived' : self.archived,
            'companyUUID': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }

    def toMongoJSON(self):
        return {
            'task_board_status_uuid': self.task_board_status_uuid,
            'title': self.title,
            'task_board_uuid': self.task_board_uuid,
            'archived' : self.archived,
            'company_uuid': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }
