from repositories import TaskRepository
from models import Task
import datetime
from typing import List
import math

class TaskService:
  def __init__(self, task_repository: TaskRepository):
    self.task_repository = task_repository
  
  def create_task(self, user_id, data: dict) -> None:
    """
    Создает задачу в базе данных
    """
    telegram_id = user_id
    title = data.get("title", None)
    project_id = data.get("project_id", None)
    responsible_id = data.get("responsible_id", None)
    completed = False
    deadline = data.get("deadline", None)
    week_first_day_date = data.get("week_first_day_date", None)
    day_date = data.get("day_date", None)
    hours, minutes = data.get("duration", 0)
    duration = hours * 60 + minutes

    task = Task(
      task_id=0,
      telegram_id=telegram_id,
      project_id=project_id,
      responsible_id=responsible_id,
      title=title,
      completed=completed,
      deadline=deadline,
      week_first_day_date=week_first_day_date,
      day_date=day_date,
      duration=duration
    )
    self.task_repository.create_task(task)

  def get_task_by_id(self, task_id: int) -> Task:
    """
    Возвращает задачу по ее id
    """
    return self.task_repository.get_task_by_id(task_id)

  def get_tasks_by_date(self, user_id: int, day_date: datetime) -> List[Task]:
    """
    Возвращает список задач пользователя по дате
    """
    return self.task_repository.get_tasks_by_date(user_id, day_date)
  
  def edit_task_title(self, task_id: int, new_title: str) -> None:
    """
    Изменяет название задачи
    """
    task = self.task_repository.get_task_by_id(task_id)
    task.title = new_title
    self.task_repository.update_task(task_id, task)

  def update_task(self, task_id: int, task: Task) -> None:
    """
    Обновляет задачу в базе данных
    """
    self.task_repository.update_task(task_id, task)

  def edit_task_duration(self, task_id: int, new_duration: int) -> None:
    """
    Изменяет длительность задачи
    """
    task = self.task_repository.get_task_by_id(task_id)
    task.duration = new_duration
    self.task_repository.update_task(task_id, task)

  def invert_task_status(self, task_id: int) -> None:
    """
    Инвертирует статус задачи
    """
    task = self.task_repository.get_task_by_id(task_id)
    if not task:
      return
    task.completed = not task.completed
    self.task_repository.update_task(task_id, task)

  def edit_task_deadline(self, task_id: int, new_deadline: datetime) -> None:
    """
    Изменяет дедлайн задачи
    """
    task = self.task_repository.get_task_by_id(task_id)
    task.deadline = new_deadline
    self.task_repository.update_task(task_id, task)

  def move_tasks_by_date(self, user_id: int, old_date: datetime, new_date: datetime) -> None:
    """
    Переносит задачи с одной даты на другую
    """
    tasks = self.task_repository.get_tasks_by_date(user_id, old_date)
    for task in tasks:
      task.day_date = new_date
      self.task_repository.update_task(task.task_id, task)

  def get_tasks_by_week_date(self, user_id: int, week_first_day_date: datetime) -> List[Task]:
    """
    Возвращает список задач пользователя по дате первого дня недели
    """
    return self.task_repository.get_tasks_by_week_date(user_id, week_first_day_date)
  
  def edit_task_date(self, task_id: int, new_date: datetime) -> None:
    """
    Изменяет дату задачи
    """
    task = self.task_repository.get_task_by_id(task_id)
    task.day_date = new_date
    self.task_repository.update_task(task_id, task)

  def move_to_next_week(self, user_id: int, week_date: datetime) -> None:
    """
    Переносит задачи на следующую неделю
    """
    tasks = self.task_repository.get_tasks_by_week_date(user_id, week_date)
    for task in tasks:
      task.week_first_day_date = task.week_first_day_date + datetime.timedelta(days=7)
      self.task_repository.update_task(task.task_id, task)

  def distribute_tasks(self, user_id: int, week_date: datetime) -> None:
    """
    Равномерно распределяет задачи на неделю
    """
    my_tasks = self.task_repository.get_tasks_by_week_date(user_id, week_date)
    
    tasks = []
    for task in my_tasks:
      if task.deadline is not None:
        if task.deadline > task.week_first_day_date + datetime.timedelta(days=6):
          task.deadline = None
        else:
          task.deadline = task.deadline.weekday()
      tasks.append(task)

    # Инициализация расписания: ключ - день недели, значение - список задач
    schedule = {day: [] for day in range(7)}
    # Суммарное время по дням
    duration_per_day = {day: 0.0 for day in range(7)}
    # Количество задач по дням
    tasks_per_day = {day: 0 for day in range(7)}
    
    # Разделение задач на категории
    tasks_with_deadline_duration = []
    tasks_with_deadline = []
    tasks_with_duration = []
    tasks_without = []
    
    for task in tasks:
        if task.deadline is not None and task.duration is not None:
            tasks_with_deadline_duration.append(task)
        elif task.deadline is not None:
            tasks_with_deadline.append(task)
        elif task.duration is not None:
            tasks_with_duration.append(task)
        else:
            tasks_without.append(task)
    
    # Сортировка задач с дедлайном по дедлайну (раньше - раньше)
    tasks_with_deadline_duration.sort(key=lambda x: x.deadline)
    tasks_with_deadline.sort(key=lambda x: x.deadline)
    
    # Функция для поиска дня с минимальной нагрузкой до дедлайна
    def assign_task_with_deadline(task, schedule, duration_per_day, tasks_per_day):
        latest_day = task.deadline
        # Найти день с минимальной суммарной нагрузкой до дедлайна
        min_load = math.inf
        selected_day = None
        for day in range(latest_day + 1):
            if duration_per_day[day] < min_load:
                min_load = duration_per_day[day]
                selected_day = day
        # Назначить задачу на выбранный день
        schedule[selected_day].append(task)
        tasks_per_day[selected_day] += 1
        if task.duration is not None:
            duration_per_day[selected_day] += task.duration
    
    # Назначение задач с дедлайном и временем
    for task in tasks_with_deadline_duration:
        assign_task_with_deadline(task, schedule, duration_per_day, tasks_per_day)
    
    # Назначение задач с дедлайном без времени
    for task in tasks_with_deadline:
        assign_task_with_deadline(task, schedule, duration_per_day, tasks_per_day)
    
    # Функция для назначения задач без дедлайна
    def assign_task_no_deadline(task, schedule, duration_per_day, tasks_per_day):
        # Выбрать день с минимальной суммарной нагрузкой
        # Учитываем время, если есть
        if task.duration is not None:
            selected_day = min(duration_per_day, key=duration_per_day.get)
            schedule[selected_day].append(task)
            duration_per_day[selected_day] += task.duration
            tasks_per_day[selected_day] += 1
        else:
            # Если времени нет, распределяем по количеству задач
            selected_day = min(tasks_per_day, key=tasks_per_day.get)
            schedule[selected_day].append(task)
            tasks_per_day[selected_day] += 1
    
    # Назначение задач без дедлайна, но с временем
    for task in tasks_with_duration:
        assign_task_no_deadline(task, schedule, duration_per_day, tasks_per_day)
    
    # Назначение задач без дедлайна и без времени
    for task in tasks_without:
        assign_task_no_deadline(task, schedule, duration_per_day, tasks_per_day)

    # print(schedule)

    for i in range(7):
      for task in schedule[i]:
        for my_task in my_tasks:
          if task.task_id == my_task.task_id:
            my_task.day_date = my_task.week_first_day_date + datetime.timedelta(days=i)
            updated_task = Task(
              task_id=my_task.task_id,
              telegram_id=my_task.telegram_id,
              project_id=my_task.project_id,
              title=my_task.title,
              completed=my_task.completed,
              deadline=my_task.deadline,
              week_first_day_date=my_task.week_first_day_date,
              day_date=my_task.day_date,
              duration=my_task.duration
            )
            self.task_repository.update_task(my_task.task_id, updated_task)

  def get_tasks_by_project_id(self, project_id: int) -> List[Task]:
    """
    Возвращает список задач по id проекта
    """
    return self.task_repository.get_tasks_by_project_id(project_id)
  
  def edit_task_responsible_person(self, task_id: int, user_id: int) -> None:
    """
    Изменяет ответственного за задачу
    """
    task = self.task_repository.get_task_by_id(task_id)
    task.responsible_id = user_id
    self.task_repository.update_task(task_id, task)
    