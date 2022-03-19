import uuid

from pymongo import MongoClient, collection
from os import environ as env

mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_COMPANY_COLLECTION']]

class Company(object):

    company_uuid: uuid
    name: str
    
    def find_all_company(user_uuid):
        companies = []
        
        companiesMongo = list(collection.find({}))
        for user in companiesMongo:
            companiesObj = Company()
            companiesObj.company_uuid = user['company_uuid']
            companiesObj.name = user['company_name']
            companies.append(companiesObj.json())
        return companies

    def addCompany(data):
        print(data)
        if Company.find_by_name(data['name']):
            print('already exists')
            return {'status': False, 'message':'company already exists'}
        else:
            print('inserting')
            collection.insert({'company_uuid': data['companyUUID'], 'name': data['name']})
            return {'status': True}
        

    def find_by_name(name):
        user = collection.find_one({'name': name})
        if user:
            return Company.convertMongoJSONToUser(user).json()
        else:
            return None

    def find_by_uuid(name):
        user = collection.find_one({'company_uuid': name})
        if user:
            return Company.convertMongoJSONToUser(user).json()
        else:
            return None

    def delete_by_company_uuid(company_uuid):
        return collection.delete_one({'company_uuid': company_uuid})

    def convertMongoJSONToUser(user):
        companiesObj = Company()
        companiesObj.company_uuid = user['company_uuid']
        companiesObj.name = user['company_name']
        return companiesObj  

    def json(self):
        return {
            'companyUUID': self.company_uuid,
            'name': self.name
        }

    def toMongoJSON(self):
        return {
            'company_uuid': self.company_uuid,
            'name': self.name
        }
