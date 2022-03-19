from modals.Story import Story
import uuid
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

class StoryListResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('userUUID',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('importance',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('priority',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('startDate',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('endDate',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('archived',
                        type=str,
                        required=False,
                        help="This field cannot be left blank!"
                        )
    
    @jwt_required(fresh=True)
    def get(self, epicUUID):
        identity = get_jwt_identity()
        return Story.find_by_user_uuid("", epicUUID, identity['companyUUID'], identity['teams']), 200, {'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*'}

    @jwt_required(fresh=True)
    def put(self, epicUUID):
        data = StoryListResource.parser.parse_args()
        identity = get_jwt_identity()
        data['storyUUID'] = str(uuid.uuid4())
        data['epicUUID'] = epicUUID
        data['companyUUID'] = identity['companyUUID']
        data['teams'] = identity['teams']
        result = Story.addStory(data)
        if result['status']:
            return ('', 201)
        else:
            return {'errorMessage': result['message']}, 400, {'Content-Type': 'application/json; charset=utf-8'}

