from app.services import AuthService, TaskService, UserService
from app.models import Task, User
from app.repositories import TaskRepository, UserRepository


class ServiceOverrides:
    def __init__(self, db_session):
        self.db_session = db_session

    def user_service(self):
        print("\n\n\n OVERRIDE \n\n\n")
        return UserService(UserRepository(model=User, session=self.db_session))

    def task_service(self):
        return TaskService(TaskRepository(model=Task, session=self.db_session))

    def auth_service(self):
        return AuthService(UserRepository(model=User, session=self.db_session))
