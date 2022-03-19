from resources.task.TaskAttachmentResource import TasksAttachmentResource
from resources.team.TeamResource import TeamResource
from resources.team.TeamListResource import TeamListResource
from resources.ForgotPasswordResource import ForgotPasswordResource
from resources.ForgotPasswordValidateAccountResource import ForgotPasswordValidateAccountResource
from resources.company.CompanyResource import CompanyResource
from resources.ConfirmAccountResource import ConfirmAccountResource
from resources.taskBoardStatus.TaskBoardStatusDetailResource import TaskBoardStatusDetailResource
from resources.taskBoardStatus.TaskBoardStatusResource import TaskBoardStatusResource
from resources.user.AdminListResource import AdminListResource
from resources.user.UserResource import UserResource
from resources.LoginResource import LoginResource
from flask import Flask
from flask_restful import Api
from os import environ as env
from flask_jwt_extended import JWTManager
from datetime import timedelta

from resources.user.UserListResource import UserListResource
from resources.role.RolesResource import RolesResource
from resources.role.RoleListResource import RoleListResource
from resources.program.ProgramResource import ProgramResource
from resources.program.ProgramListResource import ProgramListResource
from resources.project.ProjectResource import ProjectResource
from resources.project.ProjectListResource import ProjectListResource
from resources.company.CompanyListResource import CompanyListResource
from resources.story.StoryResource import StoryResource
from resources.epic.EpicListResource import EpicListResource
from resources.epic.EpicResource import EpicResource
from resources.story.StoryListResource import StoryListResource
from resources.task.TaskListResource import TaskListResource
from resources.task.TasksResource import TasksResource
from resources.taskBoard.TaskBoardResource import TaskBoardResource
from resources.taskBoard.TaskBoardDetailResource import TaskBoardDetailResource
from flask_cors import CORS

from resources.user.UserTeamsResource import UserTeamsResource

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
api = Api(app)
CORS(app)
app.config["JWT_SECRET_KEY"] = "super-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

jwt = JWTManager(app)

api.add_resource(ProgramListResource, '/program/')
api.add_resource(ProjectListResource, '/program/<string:boardUUID>/projects/')
api.add_resource(EpicListResource, '/projects/<string:projectUUID>/epic/')
api.add_resource(StoryListResource, '/epic/<string:epicUUID>/stories/')
api.add_resource(TaskBoardResource, '/stories/<string:storyUUID>/taskBoard/')
api.add_resource(TaskBoardStatusResource, '/taskBoards/<string:taskBoardUUID>/taskBoardStatus/')
api.add_resource(TaskListResource, '/taskBoardStatus/<string:taskBoardStatusUUID>/tasks/')
api.add_resource(RoleListResource, '/roles/')
api.add_resource(UserListResource, '/users/')
api.add_resource(LoginResource, '/login')
api.add_resource(CompanyListResource, '/company')
api.add_resource(ForgotPasswordValidateAccountResource, '/forgot-account/validate')
api.add_resource(ForgotPasswordResource, '/forgot-account/update-password')
api.add_resource(TeamListResource, '/team')
api.add_resource(UserTeamsResource, '/users/team')

api.add_resource(ProgramResource, '/program/<string:programUUID>')
api.add_resource(ProjectResource, '/program/<string:boardUUID>/projects/<string:projectUUID>')
api.add_resource(EpicResource, '/projects/<string:projectUUID>/epic/<string:epicUUID>')
api.add_resource(StoryResource, '/epic/<string:epicUUID>/stories/<string:storyUUID>')
api.add_resource(TaskBoardDetailResource, '/stories/<string:storyUUID>/taskBoards/<string:taskBoardUUID>')
api.add_resource(TaskBoardStatusDetailResource, '/taskBoards/<string:taskBoardUUID>/taskBoardStatus/<string:taskBoardStatusUUID>')
api.add_resource(TasksResource, '/taskBoardStatus/<string:taskBoardStatusUUID>/tasks/<string:taskUUID>')
api.add_resource(RolesResource, '/roles/<string:roleUUID>')
api.add_resource(UserResource, '/users/<string:userUUID>')
api.add_resource(ConfirmAccountResource, '/users/confirm-account')
api.add_resource(CompanyResource, '/company/<string:companyUUID>')
api.add_resource(TeamResource, '/team/<string:teamUUID>')
api.add_resource(TasksAttachmentResource, '/taskBoardStatus/<string:taskBoardStatusUUID>/tasks/<string:taskUUID>/file')
api.add_resource(AdminListResource, '/admin/users/')

def getJWT():
    return jwt

if __name__ == '__main__':
    app.run(debug=env['APP_DEBUG_MODE'])

def create_app():
   return app