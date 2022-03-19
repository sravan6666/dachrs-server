from util.BlobStorage import BlobStorage
import uuid
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, request
from flask import json, jsonify

from modals.Tasks import Tasks

class TasksAttachmentResource(Resource):

    @jwt_required(fresh=True)
    def get(self, taskBoardStatusUUID, taskUUID):
        identity = get_jwt_identity()
        fileName = request.args.get('fileName')
        task = Tasks.find_by_user_uuid_and_task_uuid("", taskBoardStatusUUID, taskUUID, identity['companyUUID'], identity['teams'])
        if task:
            response = BlobStorage.downloadFile(taskUUID,fileName)
            if response['status']:
                return response, 200, {'Content-Type': 'application/json; charset=utf-8'}
            else: 
                return response, 400, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': taskUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}