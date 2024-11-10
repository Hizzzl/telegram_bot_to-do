from abc import ABC, abstractmethod
from models import User, Task, Project, UserProjects
from database_tables import User_table, Task_table, Project_table, User_projects_table
import datetime
from typing import List

class DatabaseInterface(ABC):
  @abstractmethod
  def get_user_by_id(self, user_id: int) -> User:
    """
    Возвращает пользователя по его id
    """
    pass  

  @abstractmethod
  def get_user_by_username(self, username: str) -> User_table:
    """
    Возвращает пользователя по его username
    """
    pass

  @abstractmethod
  def create_user(self, user: User) -> None:
    """
    Создает пользователя в базе данных
    """
    pass

  @abstractmethod
  def update_user(self, user_id: int, user_data: dict) -> None:
    """
    Обновляет данные пользователя в базе данных
    """
    pass

  @abstractmethod
  def check_user_exists(self, user_id: int) -> bool:
    """
    Проверяет, существует ли пользователь в базе данных
    """
    pass

  @abstractmethod
  def create_task(self, task: Task) -> None:
    """
    Создает задачу в базе данных
    """
    pass

  @abstractmethod
  def get_task_by_id(self, task_id: int) -> Task:
    """
    Возвращает задачу по его id
    """
    pass

  @abstractmethod
  def get_tasks_by_date(self, user_id: int, day_date: datetime) -> List[Task]:
    """
    Возвращает список задач пользователя по дате
    """
    pass

  @abstractmethod
  def update_task(self, task_id: int, task: Task) -> None:
    """
    Обновляет задачу в базе данных
    """
    pass

  @abstractmethod
  def get_tasks_by_week_date(self, user_id: int, week_first_day_date: datetime) -> List[Task]:
    """
    Возвращает список задач пользователя за неделю по дате первого дня недели
    """
    pass

  @abstractmethod
  def create_project(self, project: Project) -> None:
    """
    Создает проект в базе данных
    """
    pass

  @abstractmethod
  def delete_project(self, project_id: int) -> None:
    """
    Удаляет проект из базы данных
    """
    pass

  @abstractmethod
  def get_project_by_id(self, project_id: int) -> Project:
    """
    Возвращает проект по его id
    """
    pass

  @abstractmethod
  def get_projects_by_user_id(self, user_id: int) -> List[Project]:
    """
    Возвращает список проектов пользователя по его telegram_id
    """
    pass

  @abstractmethod
  def add_project_member(self, user_id: int, project_id: int) -> None:
    """
    Добавляет пользователя в проект
    """
    pass

  @abstractmethod
  def get_user_projects_by_id(self, project_id: int) -> List[UserProjects]:
    """
    Возвращает список связей проект-пользователь по project_id
    """
    pass

  @abstractmethod
  def add_project_member(self, project_id: int, user_id: int) -> None:
    """
    Добавляет пользователя в проект
    """
    pass

  @abstractmethod
  def member_exists(self, user_id: int, project_id: int) -> bool:
    """
    Проверяет, является ли пользователь участником проекта
    """
    pass

  @abstractmethod
  def delete_project_member(self, user_id: int, project_id: int) -> None:
    """
    Удаляет пользователя из проекта
    """
    pass

  @abstractmethod
  def get_tasks_by_project_id(self, project_id: int) -> List[Task]:
    """
    Возвращает список задач по project_id
    """
    pass