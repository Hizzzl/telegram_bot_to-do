# services.py
from repositories import UserRepository, SQLAlchemyRepository, TaskRepository, ProjectRepository
from services.user_service import UserService
from services.task_service import TaskService
from services.project_service import ProjectService
from connections import connection_manager

conn_db = connection_manager.get_db_connection()

sql_alchemy_repository = SQLAlchemyRepository(conn_db, connection_manager.get_engine())

user_repo = UserRepository(sql_alchemy_repository)
user_service = UserService(user_repo)

task_repo = TaskRepository(sql_alchemy_repository)
task_service = TaskService(task_repo)

project_repo = ProjectRepository(sql_alchemy_repository)
project_service = ProjectService(project_repo)