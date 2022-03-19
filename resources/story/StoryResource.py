from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from modals.Story import Story

class StoryResource(Resource):

    @jwt_required(fresh=True)
    def get(self, epicUUID, storyUUID):
        identity = get_jwt_identity()
        task = Story.find_by_user_uuid_and_story_uuid_and_epic_uuid("", storyUUID, epicUUID, identity['companyUUID'], identity['teams'])
        if task:
            return task.json() , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': storyUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def delete(self, epicUUID, storyUUID):
        identity = get_jwt_identity()
        task = Story.find_by_user_uuid_and_story_uuid_and_epic_uuid("", storyUUID, epicUUID, identity['companyUUID'], identity['teams'])
        if task:
            Story.delete_story_by_story_uuid(storyUUID)
            return {'message': storyUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': storyUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def patch(self, epicUUID, storyUUID):
        print(request.get_json())
        data = request.get_json()
        identity = get_jwt_identity()
        task = Story.find_by_user_uuid_and_story_uuid_and_epic_uuid("", storyUUID, epicUUID, identity['companyUUID'], identity['teams'])
        if task:
            Story.update_story_by_story_uuid(task, data)
            return  Story.find_by_user_uuid_and_story_uuid_and_epic_uuid("", storyUUID, epicUUID, identity['companyUUID'], identity['teams']).json(), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': storyUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}
