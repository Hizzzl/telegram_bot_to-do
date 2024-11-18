from models import ReplyKeyboard, InlineKeyboard
from services.services_init import user_service

class KeyboardService:
  def get_main_page_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для основного меню
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.main_page_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.main_page_keyboard

  def get_daily_tasks_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для страницы с ежедневными задачами
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.daily_tasks_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.daily_tasks_keyboard
    
  def get_return_main_page_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для возврата в основное меню
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.return_main_page_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.return_main_page_keyboard
    
  def get_task_duration_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для выбора длительности задачи
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.task_duration_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.task_duration_keyboard
    
  def get_deadline_exists_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для выбора наличия дедлайна
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.task_deadline_exists_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.task_deadline_exists_keyboard

  def get_task_start_time_exists_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для выбора наличия времени начала задачи
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.task_start_time_exists_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.task_start_time_exists_keyboard
  
  def get_edit_task_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для редактирования задачи
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.edit_task_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.edit_task_keyboard
    
  def get_weekly_tasks_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для страницы с недельными задачами
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.weekly_tasks_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.weekly_tasks_keyboard
    
  def get_edit_weekly_task_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для редактирования недельной задачи
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.edit_weekly_task_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.edit_weekly_task_keyboard    
    
  def get_edit_task_date_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для редактирования даты задачи
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.edit_task_date_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.edit_task_date_keyboard
    
  def get_yes_or_no_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для ответа "да" или "нет"
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.yes_or_no_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.yes_or_no_keyboard
    
  def get_project_page_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для страницы проектов
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.project_page_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.project_page_keyboard
    
  def get_current_project_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для страницы выбранного проекта
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.current_project_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.current_project_keyboard
    
  def get_project_tasks_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для страницы задач выбранного проекта
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.project_tasks_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.project_tasks_keyboard
    
  def get_return_main_page_or_back_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для возврата в основное меню или возврата на предыдущее меню
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.return_main_page_or_back_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.return_main_page_or_back_keyboard
    
  def get_edit_project_task_keyboard(user_id: int) -> ReplyKeyboard:
    """
    Возвращает клавиатуру для редактирования задачи в проекте
    """
    keyboard_type = user_service.get_user_settings(user_id).keyboard_type

    if keyboard_type == "reply":
      return ReplyKeyboard.edit_project_task_keyboard
    if keyboard_type == "inline":
      return InlineKeyboard.edit_project_task_keyboard