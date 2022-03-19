import uuid

from pymongo import MongoClient, collection
from os import environ as env

mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_TEAM_COLLECTION']]

class Team(object):

    team_uuid: uuid
    title: str
    company_uuid: uuid
    members: list
        
    def find_by_user_uuid(userUUID, companyUUID):
        teams = []
        
        teamMongo = list(collection.find({'company_uuid': companyUUID}))
        for team in teamMongo:
            teamObj = Team()
            teamObj.team_uuid = team['team_uuid']
            teamObj.title = team['title']
            teamObj.company_uuid = team['company_uuid']
            teamObj.members = team['members']
            teams.append(teamObj.json())
        return teams

    def addTeam(data):
        print(data)
        if Team.find_by_title_and_status_uuid(data['title'], data['companyUUID']):
            print('already exists')
            return {'status': False, 'message':'Title already exists'}
        else:
            print('inserting')
            team = Team.convertJSONToTeam(data)
            collection.insert(team.toMongoJSON())
            return {'status': True, 'teamUUID': team.team_uuid}
        

    def find_by_title_and_status_uuid(title, companyUUID):
        team = collection.find_one({'title': title, 'company_uuid': companyUUID})
        print(team)
        if team:
            return Team.convertMongoJSONToTeam(team).json()
        else:
            return None

    def find_by_user_uuid_and_task_uuid(user_uuid, team_uuid, companyUUID):
        print(team_uuid)
        print(companyUUID)
        team = collection.find_one({'team_uuid': team_uuid, 'company_uuid': companyUUID})
        # add validation when we have JWT on user_uuid and task_board_uuid
        if team:
            return Team.convertMongoJSONToTeam(team)
        return None

    def delete_task_by_task_uuid(team_uuid):
        team = collection.delete_one({'team_uuid': team_uuid})
        # add validation when we have JWT on user_uuid and task_board_uuid
        return team

    def update_task_by_task_uuid(team, inputRequest):
        print('before -')
        print(team)
        if inputRequest.get('title'):
            team.title = inputRequest.get('title')
        if inputRequest.get('members'):
            team.members = inputRequest.get('members')
        
        print('afetr -')
        print(team.toMongoJSON())
        result = collection.update_one({'team_uuid': team.team_uuid}, {'$set': team.toMongoJSON()})
        return result.modified_count

    def convertMongoJSONToTeam(team):
        teamObj = Team()
        teamObj.team_uuid = team['team_uuid']
        teamObj.title = team['title']
        teamObj.company_uuid = team['company_uuid']
        teamObj.members = team['members']
        return teamObj

    def convertJSONToTeam(team):
        teamObj = Team()
        teamObj.team_uuid = team['teamUUID']
        teamObj.title = team['title']
        teamObj.company_uuid = team['companyUUID']
        teamObj.members = team['members']
        return teamObj   

    def json(self):
        return {
            'title': self.title,
            'teamUUID': self.team_uuid,
            'companyUUID': self.company_uuid,
            'members': self.members
        }

    def toMongoJSON(self):
        return {
            'team_uuid': self.team_uuid,
            'title': self.title,
            'company_uuid': self.company_uuid,
            'members': self.members
        }
