from werkzeug.security import check_password_hash
from modals.Users import Users


def authenticate(username, password):
    user = Users.find_by_username(username, True)
    if user and check_password_hash(user.get('password'), password):
        return Users.convertJSONToUser(user, False)

def identity(payload):
    print(payload)
    user_id = payload['identity']
    return Users.find_by_user_uuid(user_id)