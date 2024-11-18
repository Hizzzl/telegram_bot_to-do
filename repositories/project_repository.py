from repositories.database_interface import DatabaseInterface
from models import Project, UserProjects
from typing import List

class ProjectRepository:
  def __init__(self, db: DatabaseInterface):  # Внедряем зависимость от интерфейса базы данных
    self.db = db

  def create_project(self, project: Project) -> Project:
    """
    Создает проект в базе данных
    """
    project = self.db.create_project(project)
    my_project = Project(
      project_id=project.project_id,
      name=project.name
    )
    return my_project

  def delete_project(self, project_id: int) -> None:
    """
    Удаляет проект из базы данных
    """
    self.db.delete_project(project_id)

  def get_project_by_id(self, project_id: int) -> Project:
    """
    Возвращает проект по его id
    """
    return self.db.get_project_by_id(project_id)
  
  def get_projects_by_user_id(self, user_id: int) -> List[Project]:
    """
    Возвращает список проектов пользователя по его telegram_id
    """
    return self.db.get_projects_by_user_id(user_id)
  
  def add_project_member(self, user_id: int, project_id: int) -> None:
    """
    Добавляет пользователя в проект
    """
    self.db.add_project_member(user_id, project_id)

  def get_user_projects_by_id(self, project_id: int) -> List[UserProjects]:
    """
    Возвращает список связей проект-пользователь по project_id
    """
    projects_table = self.db.get_user_projects_by_id(project_id)

    user_projects = []
    for project in projects_table:
      my_project = UserProjects(
        user_id=project.user_id,
        project_id=project.project_id
      )
      user_projects.append(my_project)

    return user_projects

  def add_project_member(self, user_id: int, project_id: int) -> None:
    """
    Добавляет пользователя в проект
    """
    self.db.add_project_member(user_id, project_id)

  def member_exists(self, user_id: int, project_id: int) -> bool:
    """
    Проверяет, является ли пользователь участником проекта
    """
    return self.db.member_exists(user_id, project_id)
  
  def delete_project_member(self, user_id: int, project_id: int) -> None:
    """
    Удаляет пользователя из проекта
    """
    self.db.delete_project_member(user_id, project_id)