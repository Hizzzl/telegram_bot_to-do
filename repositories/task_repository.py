from repositories.database_interface import DatabaseInterface
from models import Task
import datetime
from typing import List

class TaskRepository:
  def __init__(self, db: DatabaseInterface):  # Внедряем зависимость от интерфейса базы данных
    self.db = db

  def get_task_by_id(self, task_id: int) -> Task:
    """
    Возвращает задачу по ее id
    """
    return self.db.get_task_by_id(task_id)
  
  def create_task(self, task: Task) -> None:
    """
    Создает задачу в базе данных
    """
    self.db.create_task(task)
  
  def get_tasks_by_date(self, user_id: int, day_date: datetime) -> List[Task]:
    """
    Возвращает список задач пользователя по дате
    """
    return self.db.get_tasks_by_date(user_id, day_date)
  
  def update_task(self, task_id: int, task: Task) -> None:
    """
    Обновляет задачу в базе данных
    """
    self.db.update_task(task_id, task)

  def get_tasks_by_week_date(self, user_id: int, week_first_day_date: datetime) -> List[Task]:
    """
    Возвращает список задач пользователя по дате первого дня недели
    """
    return self.db.get_tasks_by_week_date(user_id, week_first_day_date)
  
  def get_tasks_by_project_id(self, project_id: int) -> List[Task]:
    """
    Возвращает список задач по id проекта
    """
    db_tasks = self.db.get_tasks_by_project_id(project_id)
    tasks = []
    for task in db_tasks:
      tasks.append(Task(
        task_id=task.task_id,
        telegram_id=task.telegram_id,
        project_id=task.project_id,
        responsible_id=task.responsible_id,
        title=task.title,
        completed=task.completed,
        deadline=task.deadline,
        week_first_day_date=task.week_first_day_date,
        day_date=task.day_date,
        start_time=task.start_time,
        duration=task.duration
      ))
    return tasks