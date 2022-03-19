from flask_restful import Resource, request
from modals.Users import Users
from flask_jwt_extended import jwt_required

class UserResource(Resource):

    @jwt_required(fresh=True)
    def get(self, userUUID):
        user = Users.find_by_user_uuid(userUUID)
        if user:
            return user.json() , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': userUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def delete(self, userUUID):
        user = Users.find_by_user_uuid(userUUID)
        if user:
            Users.delete_by_user_uuid(userUUID)
            return {'message': userUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': userUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def patch(self, userUUID):
            print(request.get_json())
            data = request.get_json()

            task = Users.find_by_user_uuid(userUUID)
            if task:
                Users.update_user(task, data)
                return  Users.find_by_user_uuid(userUUID).json(), 200, {'Content-Type': 'application/json; charset=utf-8'}
            else:
                return {'errorMessage': userUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}