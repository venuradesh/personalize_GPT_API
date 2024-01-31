from Services.user_service import UserService

class UserControllers:
    def __init__(self, users_db) -> None:
        self.user_service = UserService(users_db)

    def user_create(self, user_data):
        return self.user_service.create_user(user_data)
    
    def login_user(self, email, password):
        return self.user_service.login_user(email, password)
