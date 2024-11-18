import datetime
from models import Messages
from typing import List, Optional, Dict
import math
from models import Task

def get_first_day_of_week(date: datetime.date) -> datetime.date:
    """
    Возвращает первый день недели
    """
    first_day = date - datetime.timedelta(days=date.weekday())
    return first_day

def get_template_task_duration(message: str) -> tuple[int, int, str]:
  """
  Сравнивает сообщения с возможными вариантами и возвращает часы и минуты
  """
  possible_durations = ["30 минут", "1 час", "2 часа", "4 часа"]
  converted_duration = [[0, 30], [1, 0], [2, 0], [4, 0]]
  try:
    hours, minutes = dict(zip(possible_durations, converted_duration))[message]
  except:
    return None, None, Messages.Errors.choose_duration_from_keyboard_error
  
  return hours, minutes, None
  
def get_custom_task_duration(message: str) -> tuple[int, int, str]:
  """
  Из сообщения получает часы и минуты и возвращает их
  Если функция завершена без ошибок, то возвращается None в переменной ошибки
  """
  try:
    hours, minutes = message.split(":")
    hours = int(hours)
    minutes = int(minutes)
  except ValueError:
    return None, None, Messages.Errors.task_duration_format_error
  
  if hours < 0 or minutes < 0:
    return None, None, Messages.Errors.task_duration_negative
  
  if minutes > 59:
    hours += minutes // 60
    minutes = minutes % 60

  if hours > 23:
    return None, None, Messages.Errors.task_duration_too_long
  
  if hours == 0 and minutes == 0:
    return None, None, Messages.Errors.task_duration_is_zero
  
  return hours, minutes, None

def get_deadline(message: str, current_date: datetime.date) -> tuple[datetime.date, str]:
  """
  Возвращает дату и переменную с текстом ошибки
  Если функция завершена без ошибок, то возвращается None в переменной ошибки
  """
  try:
    message = message.strip()
    date = datetime.datetime.strptime(message, "%d.%m.%Y").date()
  except ValueError:
    return None, Messages.Errors.deadline_format_error
  
  if not current_date:
    current_date = datetime.date.today()
  
  if date < current_date:
    return None, Messages.Errors.deadline_passed
  
  return date, None

def get_selected_day(message: str) -> tuple[int, str]:
  """
  Возвращает номер дня недели и переменную с текстом ошибки
  Если функция завершена без ошибок, то возвращается None в переменной ошибки
  """
  add_days = {"Понедельник": 0, "Вторник": 1, "Среда": 2, "Четверг": 3, "Пятница": 4, "Суббота": 5, "Воскресенье": 6}

  try:
    day = add_days[message]
  except KeyError:
    return None, Messages.Errors.choose_duration_from_keyboard_error

  return day, None

def get_username(message: str) -> tuple[str, str]:
  """
  Возвращает username и переменную с текстом ошибки
  Если функция завершена без ошибок, то возвращается None в переменной ошибки
  """

  try:
    username = message.split("@")[1]
  except IndexError:
    return None, Messages.Errors.username_format_error

  return username, None

def get_username_from_message(message):
  """
  По пользователю получим строку, которая будет использоваться в качестве username в боте
  """
  if (message.from_user.username):
    return message.from_user.username
  else:
    if (message.from_user.first_name and message.from_user.last_name):
      return message.from_user.first_name + " " + message.from_user.last_name
    else:
      if (message.from_user.first_name):
        return message.from_user.first_name
      else:
        if (message.from_user.last_name):
          return message.from_user.last_name

def get_task_start_time(message: str) -> tuple[datetime.time, str]:
  """
  Из сообщения получает время начала задачи и возвращает его
  Если функция завершена без ошибок, то возвращается None в переменной ошибки
  """
  try:
    hours, minutes = map(int, message.strip().split(':'))
    if hours < 0 or minutes < 0:
      return None, Messages.Errors.task_start_time_format_error
    if hours >= 24 or minutes >= 60:
      return None, Messages.Errors.task_start_time_format_error
    return datetime.time(hours, minutes), None
  except ValueError:
    return None, Messages.Errors.task_start_time_format_error