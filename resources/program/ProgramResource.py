from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity

from modals.Program import Program

class ProgramResource(Resource):

    @jwt_required(fresh=True)
    def get(self, programUUID):
        identity = get_jwt_identity()
        program = Program.find_by_user_uuid_and_program_uuid("", programUUID, identity['companyUUID'], identity['teams'])
        if program:
            return program.json() , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': programUUID+' not found for board - '+programUUID}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def delete(self, programUUID):
        identity = get_jwt_identity()
        program = Program.find_by_user_uuid_and_program_uuid("", programUUID, identity['companyUUID'], identity['teams'])
        if program:
            Program.delete_program_by_program_uuid(programUUID)
            return {'message': programUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': programUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}

    @jwt_required(fresh=True)
    def patch(self, programUUID):
        print(request.get_json())
        data = request.get_json()
        identity = get_jwt_identity()
        program = Program.find_by_user_uuid_and_program_uuid("", programUUID, identity['companyUUID'], identity['teams'])
        if program:
            Program.update_epic_by_program_uuid(program, data)
            return  Program.find_by_user_uuid_and_program_uuid("", programUUID, identity['companyUUID'], identity['teams']).json(), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': programUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}
