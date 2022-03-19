import uuid

from pymongo import MongoClient, collection
from os import environ as env

mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_TASKBOARD_COLLECTION']]

class TaskBoard(object):

    task_board_uuid: uuid
    title: str
    story_uuid: uuid
    archived: bool = False
    company_uuid: uuid
    teams: list
        
    def find_by_user_uuid(userUUID, storyUUID, companyUUID, teams):
        taskBoards = []
        
        taskBoardMongo = list(collection.find({'story_uuid': storyUUID, 'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for taskBoard in taskBoardMongo:
            taskBoardObj = TaskBoard()
            taskBoardObj.task_board_uuid = taskBoard['task_board_uuid']
            taskBoardObj.title = taskBoard['title']
            taskBoardObj.story_uuid = taskBoard['story_uuid']
            taskBoardObj.archived = taskBoard['archived']
            taskBoardObj.company_uuid = taskBoard['company_uuid']
            taskBoardObj.teams = taskBoard['teams']
            taskBoards.append(taskBoardObj.json())
        return taskBoards


    def findAll_by_user_uuid(userUUID, companyUUID, teams):
        taskBoards = []
        
        taskBoardMongo = list(collection.find({'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for taskBoard in taskBoardMongo:
            taskBoardObj = TaskBoard()
            taskBoardObj.task_board_uuid = taskBoard['task_board_uuid']
            taskBoardObj.title = taskBoard['title']
            taskBoardObj.story_uuid = taskBoard['story_uuid']
            taskBoardObj.archived = taskBoard['archived']
            taskBoardObj.company_uuid = taskBoard['company_uuid']
            taskBoardObj.teams = taskBoard['teams']
            taskBoards.append(taskBoardObj.json())
        return taskBoards

    def addTask(data):
        print(data)
        if TaskBoard.find_by_title_and_story_uuid(data['title'], data['storyUUID'], data['companyUUID'], data['teams']):
            print('already exists')
            return {'status': False, 'message':'Title already exists'}
        else:
            print('inserting')
            taskBoard = TaskBoard.convertJSONToTask(data)
            collection.insert(taskBoard.toMongoJSON())
            return {'status': True, 'taskBoardUUID': taskBoard.task_board_uuid}
        

    def find_by_title_and_story_uuid(title, story_uuid, companyUUID, teams):
        taskBoard = collection.find_one({'title': title, 'story_uuid': story_uuid, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        print(taskBoard)
        if taskBoard:
            return TaskBoard.convertMongoJSONToTask(taskBoard).json()
        else:
            return None

    def find_by_user_uuid_and_task_uuid(user_uuid, storyUUID, task_board_uuid, companyUUID, teams):
        taskBoard = collection.find_one({'story_uuid': storyUUID, 'task_board_uuid': task_board_uuid, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        # add validation when we have JWT on user_uuid and story_uuid
        if taskBoard:
            return TaskBoard.convertMongoJSONToTask(taskBoard)
        return None

    def delete_task_by_task_uuid(task_board_uuid):
        taskBoard = collection.delete_one({'task_board_uuid': task_board_uuid})
        # add validation when we have JWT on user_uuid and story_uuid
        return taskBoard

    def update_task_by_task_uuid(taskBoard, inputRequest):
        print('before -')
        print(taskBoard)
        if inputRequest.get('title'):
            taskBoard.title = inputRequest.get('title')
        if inputRequest.get('storyUUID'):
            taskBoard.story_uuid = inputRequest.get('storyUUID')
        if inputRequest.get('archived') is not taskBoard.archived:
            taskBoard.archived = inputRequest.get('archived')
        if inputRequest.get('teams'):
            taskBoard.teams = inputRequest.get('teams')
        
        print('afetr -')
        print(taskBoard.toMongoJSON())
        result = collection.update_one({'task_board_uuid': taskBoard.task_board_uuid}, {'$set': taskBoard.toMongoJSON()})
        return result.modified_count

    def convertMongoJSONToTask(taskBoard):
        taskBoardObj = TaskBoard()
        taskBoardObj.task_board_uuid = taskBoard['task_board_uuid']
        taskBoardObj.title = taskBoard['title']
        taskBoardObj.story_uuid = taskBoard['story_uuid']
        taskBoardObj.archived = taskBoard['archived']
        taskBoardObj.company_uuid = taskBoard['company_uuid']
        taskBoardObj.teams = taskBoard['teams']
        return taskBoardObj

    def convertJSONToTask(taskBoard):
        taskBoardObj = TaskBoard()
        taskBoardObj.task_board_uuid = taskBoard['taskBoardUUID']
        taskBoardObj.title = taskBoard['title']
        taskBoardObj.story_uuid = taskBoard['storyUUID']
        taskBoardObj.archived = taskBoard['archived']
        taskBoardObj.company_uuid = taskBoard['companyUUID']
        taskBoardObj.teams = taskBoard['teams']
        return taskBoardObj   

    def json(self):
        return {
            'taskBoardUUID': self.task_board_uuid,
            'title': self.title,
            'storyUUID': self.story_uuid,
            'archived' : self.archived,
            'companyUUID': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }

    def toMongoJSON(self):
        return {
            'task_board_uuid': self.task_board_uuid,
            'title': self.title,
            'story_uuid': self.story_uuid,
            'archived' : self.archived,
            'company_uuid': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }
