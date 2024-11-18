from models import Project
from repositories import ProjectRepository
from typing import List

class ProjectService:
  def __init__(self, project_repo: ProjectRepository):
    self.project_repo = project_repo

  def get_projects_by_user_id(self, user_id: int) -> List[Project]:
    """
    Возвращает список проектов пользователя
    """
    return self.project_repo.get_projects_by_user_id(user_id)
  
  def get_project_by_id(self, project_id: int) -> Project:
    """
    Возвращает проект по его id
    """
    return self.project_repo.get_project_by_id(project_id)
  
  def create_project(self, user_id: int, project_name: str) -> Project:
    """
    Создает проект в базе данных
    """
    project = Project(name=project_name)
    project = self.project_repo.create_project(project)
    self.project_repo.add_project_member(user_id, project.project_id)

  def get_members_ids_by_project_id(self, project_id: int) -> List[int]:
    """
    Возвращает список user_id участников проекта
    """
    user_projects = self.project_repo.get_user_projects_by_id(project_id)

    user_ids = []
    for user_project in user_projects:
      user_ids.append(user_project.user_id)

    return user_ids
  
  def add_project_member(self, user_id: int, project_id: int):
    """
    Добавляет пользователя в проект
    """
    self.project_repo.add_project_member(user_id=user_id, project_id=project_id)

  def member_exists(self, user_id: int, project_id: int) -> bool:
    """
    Проверяет, является ли пользователь участником проекта
    """
    return self.project_repo.member_exists(user_id=user_id, project_id=project_id)
  
  def delete_project_member(self, user_id: int, project_id: int):
    """
    Удаляет пользователя из проекта. Если проект не имеет участников, удаляет проект
    """
    self.project_repo.delete_project_member(user_id=user_id, project_id=project_id)
    members = self.get_members_ids_by_project_id(project_id)
    if len(members) == 0:
      self.project_repo.delete_project(project_id)