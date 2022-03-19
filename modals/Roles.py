import uuid

from pymongo import MongoClient, collection
from os import environ as env

mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_ROLES_COLLECTION']]

class Roles(object):

    role_uuid: uuid
    name: str
        
    def get_all_roles():
        roles = []
        
        rolesMongo = list(collection.find({}))
        for role in rolesMongo:
            rolesObj = Roles()
            rolesObj.role_uuid = role['role_uuid']
            rolesObj.name = role['name']
            roles.append(rolesObj.json())
        return roles

    def addRole(data):
        print(data)
        
        if Roles.find_by_name(data['name']):
            print('already exists')
            return {'status': False, 'message':'Role already exists'}
        else:
            print('inserting')
            role = Roles.convertJSONToRole(data)
            collection.insert(role.toMongoJSON())
            return {'status': True}
        

    def find_by_name(name):
        role = collection.find_one({'name': name})
        print(role)
        if role:
            return Roles.convertMongoJSONToRole(role).json()
        else:
            return None

    def find_by_uuid(uuid):
        role = collection.find_one({'role_uuid': uuid})
        print(role)
        if role:
            return Roles.convertMongoJSONToRole(role).json()
        else:
            return None

    def delete_task_by_role_uuid(role_uuid):
        role = collection.delete_one({'role_uuid': role_uuid})
        # add validation when we have JWT on user_uuid and story_uuid
        return role

    def convertMongoJSONToRole(role):
        rolesObj = Roles()
        rolesObj.role_uuid = role['role_uuid']
        rolesObj.name = role['name']
        return rolesObj

    def convertJSONToRole(role):
        rolesObj = Roles()
        rolesObj.role_uuid = role['roleUUID']
        rolesObj.name = role['name']
        return rolesObj   

    def json(self):
        return {
            'roleUUID': self.role_uuid,
            'name': self.name
        }

    def toMongoJSON(self):
        return {
            'role_uuid': self.role_uuid,
            'name': self.name
        }
