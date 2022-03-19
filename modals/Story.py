import uuid
from datetime import datetime

from pymongo import MongoClient, collection
from os import environ as env

mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_STORY_COLLECTION']]

class Story(object):

    story_uuid: uuid
    title: str
    description: str
    user_uuid: uuid
    importance: str
    priority: str
    start_date: datetime
    end_date: datetime
    epic_uuid: uuid
    archived: bool = False
    company_uuid: uuid
    teams: list
        
    def find_by_user_uuid(user_uuid, epicUUID, companyUUID, teams):
        stories = []
        
        storiesMongo = list(collection.find({'epic_uuid': epicUUID, 'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for story in storiesMongo:
            storyObj = Story()
            storyObj.story_uuid = story['story_uuid']
            storyObj.title = story['title']
            storyObj.description = story['description']
            storyObj.user_uuid = story['user_uuid']
            storyObj.importance = story['importance']
            storyObj.priority = story['priority']
            storyObj.start_date = story['start_date']
            storyObj.end_date = story['end_date']
            storyObj.epic_uuid = story['epic_uuid']
            storyObj.archived = story['archived']
            storyObj.company_uuid = story['company_uuid']
            storyObj.teams = story['teams']
            stories.append(storyObj.json())
        return stories

    def findAll_by_user_uuid(user_uuid, companyUUID, teams):
        stories = []
        
        storiesMongo = list(collection.find({'company_uuid': companyUUID, 'teams': { '$all': teams }}))
        for story in storiesMongo:
            storyObj = Story()
            storyObj.story_uuid = story['story_uuid']
            storyObj.title = story['title']
            storyObj.description = story['description']
            storyObj.user_uuid = story['user_uuid']
            storyObj.importance = story['importance']
            storyObj.priority = story['priority']
            storyObj.start_date = story['start_date']
            storyObj.end_date = story['end_date']
            storyObj.epic_uuid = story['epic_uuid']
            storyObj.archived = story['archived']
            storyObj.company_uuid = story['company_uuid']
            storyObj.teams = story['teams']
            stories.append(storyObj.json())
        return stories

    def addStory(data):
        print(data)
        if data['endDate'] < data['startDate']:
            return {'status': False, 'message':'End date cannot be less than start date'}

        if Story.find_by_title_and_epic_uuid(data['title'], data['epicUUID'], data['companyUUID'], data['teams']):
            print('already exists')
            return {'status': False, 'message':'Title already exists'}
        else:
            print('inserting')
            story = Story.convertJSONToStory(data)
            collection.insert(story.toMongoJSON())
            return {'status': True}
        

    def find_by_title_and_epic_uuid(title, epic_uuid, companyUUID, teams):
        story = collection.find_one({'title': title, 'epic_uuid': epic_uuid, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        print(story)
        if story:
            return Story.convertMongoJSONToStory(story).json()
        else:
            return None

    def find_by_user_uuid_and_story_uuid_and_epic_uuid(user_uuid, story_uuid,epic_uuid, companyUUID, teams):
        story = collection.find_one({'epic_uuid': epic_uuid, 'story_uuid': story_uuid, 'company_uuid': companyUUID, 'teams': { '$all': teams }})
        # add validation when we have JWT on user_uuid and epic_uuid
        if story:
            return Story.convertMongoJSONToStory(story)
        return None

    def delete_story_by_story_uuid(story_uuid):
        story = collection.delete_one({'story_uuid': story_uuid})
        # add validation when we have JWT on user_uuid and story_uuid
        return story

    def update_story_by_story_uuid(story, inputRequest):
        print('before -')
        print(story)
        if inputRequest.get('title'):
            story.title = inputRequest.get('title')
        if inputRequest.get('description'):
            story.description = inputRequest.get('description')
        if inputRequest.get('userUUID'):
            story.user_uuid = inputRequest.get('userUUID')
        if inputRequest.get('importance'):
            story.importance = inputRequest.get('importance')
        if inputRequest.get('priority'):
            story.priority = inputRequest.get('priority')
        if inputRequest.get('startDate'):
            story.start_date = inputRequest.get('startDate')
        if inputRequest.get('endDate'):
            story.end_date = inputRequest.get('endDate')
        if inputRequest.get('epicUUID'):
            story.epic_uuid = inputRequest.get('epicUUID')
        if inputRequest.get('archived') is not story.archived:
            story.archived = inputRequest.get('archived')
        if inputRequest.get('teams'):
            story.teams = inputRequest.get('teams')

        print('afetr -')
        print(story.toMongoJSON())
        result = collection.update_one({'story_uuid': story.story_uuid}, {'$set': story.toMongoJSON()})
        return result.modified_count

    def convertMongoJSONToStory(story):
        storyObj = Story()
        storyObj.story_uuid = story['story_uuid']
        storyObj.title = story['title']
        storyObj.description = story['description']
        storyObj.user_uuid = story['user_uuid']
        storyObj.importance = story['importance']
        storyObj.priority = story['priority']
        storyObj.start_date = story['start_date']
        storyObj.end_date = story['end_date']
        storyObj.epic_uuid = story['epic_uuid']
        storyObj.archived = story['archived']
        storyObj.company_uuid = story['company_uuid']
        storyObj.teams = story['teams']
        return storyObj

    def convertJSONToStory(story):
        storyObj = Story()
        storyObj.story_uuid = story['storyUUID']
        storyObj.title = story['title']
        storyObj.description = story['description']
        storyObj.user_uuid = story['userUUID']
        storyObj.importance = story['importance']
        storyObj.priority = story['priority']
        storyObj.start_date = story['startDate']
        storyObj.end_date = story['endDate']
        storyObj.epic_uuid = story['epicUUID']
        storyObj.archived = story['archived']
        storyObj.company_uuid = story['companyUUID']
        storyObj.teams = story['teams']
        return storyObj   

    def json(self):
        return {
            'storyUUID': self.story_uuid,
            'title': self.title,
            'description': self.description,
            'userUUID': self.user_uuid,
            'importance': self.importance,
            'priority': self.priority,
            'startDate': self.start_date,
            'endDate': self.end_date,
            'epicUUID': self.epic_uuid,
            'archived': self.archived,
            'companyUUID': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }

    def toMongoJSON(self):
        return {
            'story_uuid': self.story_uuid,
            'title': self.title,
            'description': self.description,
            'user_uuid': self.user_uuid,
            'importance': self.importance,
            'priority': self.priority,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'epic_uuid': self.epic_uuid,
            'archived': self.archived,
            'company_uuid': self.company_uuid,
            'teams': self.teams if hasattr(self, 'teams') else None
        }
