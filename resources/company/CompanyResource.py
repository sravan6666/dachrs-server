from flask_restful import Resource, request
from modals.Company import Company
from flask_jwt_extended import jwt_required

class CompanyResource(Resource):

    def delete(self, companyUUID):
        user = Company.find_by_uuid(companyUUID)
        if user:
            Company.delete_by_company_uuid(companyUUID)
            return {'message': companyUUID+' deleted'} , 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return {'errorMessage': companyUUID+' not found'}, 404, {'Content-Type': 'application/json; charset=utf-8'}
