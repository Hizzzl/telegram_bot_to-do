from repositories.database_interface import DatabaseInterface
from models import User, Task, Project, UserProjects
from database_tables import User_table, Base, Task_table, Project_table
from database_tables import User_projects_table
from sqlalchemy import select, update, delete
import datetime
from typing import List

class SQLAlchemyRepository(DatabaseInterface):
  def __init__(self, session, engine):
      self.session = session
      self.engine = engine
      self.Base = Base
      Base.metadata.create_all(bind=engine)

  def get_user_by_id(self, user_id: int) -> User:
    """
    Возвращает пользователя по его id
    """
    stmt = select(User_table).where(User_table.telegram_id == user_id)
    result = self.session.scalars(stmt)
    for user in result:
      return user
    return None

  def get_user_by_username(self, username: str) -> User_table:
    """
    Возвращает пользователя по его username
    """
    stmt = select(User_table).where(User_table.username == username)
    result = self.session.scalars(stmt)
    for user in result:
      return user
    return None

  def create_user(self, user_data: User) -> None:
    """
    Создает пользователя в базе данных
    """
    new_user = User_table(
      telegram_id=user_data.telegram_id,
      username=user_data.username,
      current_streak=user_data.current_streak,
      max_streak=user_data.max_streak,
      settings={
        "keyboard_type": user_data.settings.keyboard_type
      }
    )
    
    self.session.add(new_user)
    self.session.commit()

  def update_user(self, user_id: int, user_data: User) -> None:
    """
    Обновляет данные пользователя в базе данных
    """
    user = self.get_user_by_id(user_id)
    if user:
      user.username = user_data.username
      user.current_streak = user_data.current_streak
      user.max_streak = user_data.max_streak
      user.settings["keyboard_type"] = user_data.settings.keyboard_type
      
      print(user.telegram_id, user.username, user.current_streak, user.max_streak, user.settings["keyboard_type"])

      self.session.commit()

  def delete_user(self, user_id: int) -> None:
    """
    Удаляет пользователя из базы данных
    """
    user = self.get_user_by_id(user_id)
    if user:
      self.session.delete(user)
      self.session.commit()

  def check_user_exists(self, user_id: int) -> bool:
    """
    Проверяет наличие пользователя в базе данных
    """
    user = self.get_user_by_id(user_id)
    return user is not None
  
  def create_task(self, task: Task) -> None:
    """
    Создает задачу в базе данных
    """
    new_task = Task_table(
      telegram_id=task.telegram_id,
      project_id=task.project_id,
      responsible_id=task.responsible_id,
      title=task.title,
      completed=task.completed,
      deadline=task.deadline,
      week_first_day_date=task.week_first_day_date,
      day_date=task.day_date,
      duration=task.duration
    )
    self.session.add(new_task)
    self.session.commit()

  def get_task_by_id(self, task_id: int) -> Task:
    """
    Возвращает задачу по ее id
    """
    stmt = select(Task_table).where(Task_table.task_id == task_id)
    result = self.session.scalars(stmt)
    for task in result:
      my_task = Task(
        task_id=task.task_id,
        telegram_id=task.telegram_id,
        project_id=task.project_id,
        responsible_id=task.responsible_id,
        title=task.title,
        completed=task.completed,
        deadline=task.deadline,
        week_first_day_date=task.week_first_day_date,
        day_date=task.day_date,
        duration=task.duration
      )
      return my_task
    return None

  def get_tasks_by_date(self, user_id: int, day_date: datetime) -> List[Task]:
    """
    Возвращает список задач пользователя по дате
    """
    stmt = (
      select(Task_table)
      .where(Task_table.telegram_id == user_id, Task_table.day_date == day_date)
    )
    tasks = []
    result = self.session.scalars(stmt)

    for task in result:
      converted_task = Task(
        task_id=task.task_id,
        telegram_id=task.telegram_id,
        project_id=task.project_id,
        responsible_id=task.responsible_id,
        title=task.title,
        completed=task.completed,
        deadline=task.deadline,
        week_first_day_date=task.week_first_day_date,
        day_date=task.day_date,
        duration=task.duration
      )
      tasks.append(converted_task)
    return tasks
  
  def update_task(self, task_id: int, task: Task) -> None:
    """
    Обновляет задачу в базе данных
    """   
    stmt = update(Task_table).where(Task_table.task_id == task_id).values(
      telegram_id=task.telegram_id,
      project_id=task.project_id,
      responsible_id=task.responsible_id,
      title=task.title,
      completed=task.completed,
      deadline=task.deadline,
      week_first_day_date=task.week_first_day_date,
      day_date=task.day_date,
      duration=task.duration
    )
    self.session.execute(stmt)
    self.session.commit()

  def get_tasks_by_week_date(self, user_id: int, week_first_day_date: datetime) -> List[Task]:
    """
    Возвращает список задач пользователя по дате
    """
    stmt = (
      select(Task_table)
      .where(Task_table.telegram_id == user_id, Task_table.week_first_day_date == week_first_day_date)
    )
    tasks = []
    result = self.session.scalars(stmt)

    for task in result:
      converted_task = Task(
        task_id=task.task_id,
        telegram_id=task.telegram_id,
        project_id=task.project_id,
        responsible_id=task.responsible_id,
        title=task.title,
        completed=task.completed,
        deadline=task.deadline,
        week_first_day_date=task.week_first_day_date,
        day_date=task.day_date,
        duration=task.duration
      )
      tasks.append(converted_task)
    return tasks
  
  def create_project(self, project: Project) -> Project:
    """
    Создает проект в базе данных
    """
    new_project = Project_table(
      name=project.name
    )
    self.session.add(new_project)
    self.session.commit()
    
    return new_project

  def delete_project(self, project_id: int) -> None:
    """
    Удаляет проект из базы данных
    """
    stmt = delete(Project_table).where(Project_table.project_id == project_id)
    self.session.execute(stmt)
    self.session.commit()

  def get_project_by_id(self, project_id: int) -> Project:
    """
    Возвращает проект по его id
    """
    stmt = select(Project_table).where(Project_table.project_id == project_id)
    result = self.session.scalars(stmt)
    for project in result:
      my_project = Project(
        project_id=project.project_id,
        name=project.name
      )
      return my_project
    return None
  
  def get_projects_by_user_id(self, user_id: int) -> List[Project]:
    """
    Возвращает список проектов пользователя
    """
    stmt = (
        select(Project_table)
        .join(User_projects_table, User_projects_table.project_id == Project_table.project_id)
        .where(User_projects_table.user_id == user_id)
    )
    result = self.session.scalars(stmt).all()  # .all() для получения всех значений сразу
    return result
  
  def add_project_member(self, user_id: int, project_id: int) -> None:
    """
    Добавляет пользователя в проект
    """
    new_user_project = User_projects_table(
      user_id=user_id,
      project_id=project_id
    )
    self.session.add(new_user_project)
    self.session.commit()

  def get_user_projects_by_id(self, project_id: int) -> List[User_projects_table]:
    """
    Возвращает список проектов пользователя
    """
    stmt = (
      select(User_projects_table)
      .where(User_projects_table.project_id == project_id)
    )
    result = self.session.scalars(stmt)
    return result
  
  def add_project_member(self, user_id: int, project_id: int) -> None:
    """
    Добавляет пользователя в проект
    """
    new_user_project = User_projects_table(
      user_id=user_id,
      project_id=project_id
    )
    self.session.add(new_user_project)
    self.session.commit()

  def member_exists(self, user_id: int, project_id: int) -> bool:
    """
    Проверяет наличие пользователя в проекте
    """
    stmt = (
      select(User_projects_table)
      .where(User_projects_table.user_id == user_id, User_projects_table.project_id == project_id)
    )
    result = self.session.scalars(stmt)
    if result:
      return True
    else:
      return False
    
  def delete_project_member(self, user_id, project_id) -> None:
    """
    Удаляет пользователя из проекта
    """
    stmt = (
      delete(User_projects_table)
      .where(User_projects_table.user_id == user_id, User_projects_table.project_id == project_id)
    )
    self.session.execute(stmt)
    self.session.commit()

  def get_tasks_by_project_id(self, project_id) -> List[Task_table]:
    """
    Возвращает список задач по project_id
    """
    stmt = (
      select(Task_table)
      .where(Task_table.project_id == project_id)
    )
    result = self.session.scalars(stmt)
    return result