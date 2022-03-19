#from security.SecretManager import SecretManager
from util.BlobStorage import BlobStorage
from modals.Team import Team
from util.SendEmail import SendEmail
from util.Utility import Utility
import uuid
from werkzeug.security import generate_password_hash

from pymongo import MongoClient, collection
from os import environ as env

#mongo_url = SecretManager.get_secret_value(env['MONGO_CONNECTION_STR'])
#print(mongo_url)
mongoClient = MongoClient(env['MONGO_CONNECTION_STR'])
db=mongoClient[env['MONGO_DB']]
collection =db[env['MONGO_USERS_COLLECTION']]

class Users(object):

    id: uuid
    user_uuid: uuid
    name: str
    username: str
    password: str
    role_uuid: uuid
    company_uuid: uuid
    company: str
    phone: str
    website: str
    email: str
    verification_code: int
    is_active: bool
    teams: list
    
    def find_by_all_user(user_uuid):
        users = []
        
        userMongo = list(collection.find({'is_active': True}))
        for user in userMongo:
            userObj = Users()
            userObj.user_uuid = user['user_uuid']
            userObj.username = user['username']
            userObj.name = user['name']
            userObj.role_uuid = user['role_uuid']
            userObj.company_uuid = user['company_uuid']
            userObj.company = user['company']
            userObj.phone = user['phone']
            userObj.website = user['website']
            userObj.email = user['email']
            userObj.teams = user['teams']
            users.append(userObj.json())
        return users

    def find_by_all_user_for_company(companyUUID):
        users = []
        #fileBlob = "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AAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAABBL8AAAAEEjwAwAAQCDBDwAAAIEEPwAAAAQS/AAAABBI8AMAAEAgwQ8AAACBBD8AAAAEEvwAAAAQSPADAABAIMEPAAAAgQQ/AAAAxPnrr/8DGWEU3VLNhEIAAAAASUVORK5CYII="
        #name = str(uuid.uuid4())
        #print('up')
        #print(BlobStorage.uploadFile(name,'image.png',fileBlob))
        #print('down')
        #print(BlobStorage.downloadFile(name,'image.png'))
        
        userMongo = list(collection.find({'company_uuid': companyUUID}))
        for user in userMongo:
            userObj = Users()
            userObj.user_uuid = user['user_uuid']
            userObj.username = user['username']
            userObj.name = user['name']
            userObj.role_uuid = user['role_uuid']
            userObj.company_uuid = user['company_uuid']
            userObj.company = user['company']
            userObj.phone = user['phone']
            userObj.website = user['website']
            userObj.email = user['email']
            users.append(userObj.json())
        return users

    def addUser(data):
        print(data)
        # if Users.find_by_username(data['username'], True):
        #     print('already exists')
        #     return {'status': False, 'message':'user already exists'}
        if Users.find_by_email(data['email']):
            print('already exists')
            return {'status': False, 'message':'user already exists'}
        else:
            # check for valid team id
            #if Team.find_by_user_uuid_and_task_uuid("", data['teamUUID'], data['companyUUID']):
            print('inserting')
            user = Users.convertJSONToUser(data, True)
            user.is_active = False
            user.verification_code = Utility.random_with_N_digits(6)
            print(user.teams)
            collection.insert(user.toMongoJSON())
            return {'status': True, 'otp': user.verification_code}
            #else:
            #    return {'status': False, 'errorMessage': 'Invalid team'}
        
    def addUserByAdmin(data):
        print(data)
        if Users.find_by_username(data['username'], True):
            print('already exists')
            return {'status': False, 'message':'user already exists'}
        elif Users.find_by_email(data['email']):
            print('already exists')
            return {'status': False, 'message':'user already exists'}
        else:
            # check for valid team id
            #if Team.find_by_user_uuid_and_task_uuid("", data['teamUUID'], data['companyUUID']):
            print('inserting')
            data['password'] = 'Password@123'
            user = Users.convertJSONToUser(data, True)
            user.is_active = True
            user.verification_code = 0
            print(user.teams)
            collection.insert(user.toMongoJSON())
            return {'status': True, 'pwd': data['password']}

    def find_by_username(username, is_active):
        user = collection.find_one({'username': username, 'is_active': is_active})
        print(user)
        if user:
            return Users.convertMongoJSONToUser(user).json()
        else:
            return None

    def find_by_email(email):
        user = collection.find_one({'email': email})
        print(user)

        if user and user.get('is_active'):
            return Users.convertMongoJSONToUser(user).json()
        else:
            return None

    def find_by_user_uuid(user_uuid):
        user = collection.find_one({'user_uuid': user_uuid, 'is_active': True})
        # add validation when we have JWT on user_uuid and story_uuid
        if user:
            return Users.convertMongoJSONToUser(user)
        return None

    def find_by_user_uuid_and_token(email, token):
        user = collection.find_one({'email': email, 'is_active': False})
        # add validation when we have JWT on user_uuid and story_uuid
        print(user)
        
        if user and (int(token) == user.get('verification_code', 0)):
            return Users.convertMongoJSONToUser(user)
        # return None

    def delete_by_user_uuid(user_uuid):
        user = collection.delete_one({'user_uuid': user_uuid})
        # add validation when we have JWT on user_uuid and story_uuid
        return user

    def update_user(user, inputRequest):
        print('before -')
        print(user)
        if inputRequest.get('company'):
            user.company = inputRequest.get('company')
        if inputRequest.get('roleUUID'):
            user.role_uuid = inputRequest.get('roleUUID')
        if inputRequest.get('company_uuid'):
            user.company_uuid = inputRequest.get('company_uuid')
        if inputRequest.get('phone'):
            user.phone = inputRequest.get('phone')
        if inputRequest.get('website'):
            user.website = inputRequest.get('website')
        if inputRequest.get('email'):
            user.email = inputRequest.get('email')
        if inputRequest.get('teams'):
            user.teams = inputRequest.get('teams')
        if isinstance(inputRequest.get('isActive'), bool): 
            user.is_active = inputRequest.get('isActive')
            user.verification_code = 0

        print('afetr -')
        print(user.toMongoJSON())
        result = collection.update_one({'user_uuid': user.user_uuid}, {'$set': user.toMongoJSON()})
        return result.modified_count

    def forgot_password_validate_account(user):
        user.verification_code = Utility.random_with_N_digits(6)
        collection.update_one({'user_uuid': user.user_uuid}, {'$set': {'verification_code': user.verification_code}})
        accountConfirmationMessage = str(user.verification_code) + ' is the password reset verification code'
        SendEmail.sendEmail(user.email, "Password Reset", accountConfirmationMessage)
        
        return {'message': 'Password reset code sent to the registered email address'}

    def forgot_password(user, input):
        print(user.json())

        if (int(input['token']) == user.verification_code):
            collection.update_one({'user_uuid': user.user_uuid}, {'$set': {'password': generate_password_hash(input.get('password')), 'verification_code': 0}})
            accountConfirmationMessage = 'Password reset is successfully completed for your account.'
            SendEmail.sendEmail(user.email, "Password Reset", accountConfirmationMessage)
            return {'message': 'Password reset successful', 'errorMessage': None}
        else:
            return {'errorMessage': 'Invalid request'}

    def resend_verification_token(username):
        user = Users.find_by_username(username, False)
        if user:
            user = Users.convertJSONToUser(user, False)
            verification_code = Utility.random_with_N_digits(6)
            print(user.user_uuid)
            collection.update_one({'user_uuid': user.user_uuid}, {'$set': {'verification_code': verification_code}})
            accountConfirmationMessage = str(verification_code) + ' is the account verification code'
            SendEmail.sendEmail(user.email, "Registration Confirmation", accountConfirmationMessage)
            return {'message': 'Token sent on the registered email', 'errorMessage': None}
        else:
            return {'errorMessage': 'Invalid credentials provided'}

    def convertMongoJSONToUser(user):
        userObj = Users()
        userObj.id = user['user_uuid']
        userObj.user_uuid = user['user_uuid']
        # userObj.username = user['username']
        userObj.role_uuid = user['role_uuid']
        userObj.password = user['password']
        # userObj.name = user['name']
        userObj.company = user.get('company')
        userObj.company_uuid = user.get('company_uuid')
        userObj.phone = user.get('phone')
        userObj.website = user.get('website')
        userObj.email = user.get('email')
        userObj.is_active = user.get('is_active')
        userObj.verification_code = user.get('verification_code', 0)
        userObj.teams = user.get('teams', [])

        return userObj

    def convertJSONToUser(user, is_password_required):
        userObj = Users()
        userObj.id = user['userUUID']
        userObj.user_uuid = user['userUUID']
        # userObj.name = user['name']
        userObj.role_uuid = user.get('roleUUID', None)
        # userObj.username = user['username']
        userObj.company = user.get('company', None)
        userObj.company_uuid = user.get('companyUUID', None)
        userObj.phone = user.get('phone', None)
        userObj.website = user.get('website', None)
        userObj.password = generate_password_hash(user.get('password')) if is_password_required else ''
        userObj.email = user.get('email', None)
        userObj.verification_code = user.get('verification_code', 0)
        userObj.teams = user.get('teams', [])
        return userObj   

    def json(self):
        return {
            'id': self.id if hasattr(self, 'id') else None,
            'userUUID': self.user_uuid,
            # 'name': self.name,
            'roleUUID': self.role_uuid,
            # 'username': self.username,
            'password': self.password if hasattr(self, 'password') else None,
            'companyUUID': self.company_uuid,
            'company': self.company,
            'phone': self.phone,
            'website': self.website,
            'email': self.email,
            'verification_code': self.verification_code if hasattr(self, 'verification_code') else None,
            'teams': self.teams if hasattr(self, 'teams') else None
        }

    def toMongoJSON(self):
        return {
            'user_uuid': self.user_uuid,
            # 'name': self.name,
            'role_uuid': self.role_uuid,
            # 'username': self.username,
            'password': self.password,
            'company_uuid': self.company_uuid,
            'company': self.company,
            'phone': self.phone,
            'website': self.website,
            'email': self.email,
            'is_active': self.is_active,
            'verification_code': self.verification_code,
            'teams': self.teams if hasattr(self, 'teams') else None
        }
