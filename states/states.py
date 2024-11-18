from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
  on_start_page = State()
  on_day_page = State()
  on_week_page = State()
  on_project_page = State()

  waiting_for_task_name = State()
  waiting_for_task_start_date = State()
  waiting_for_task_start_time = State()

  process_task_start_time = State()
  waiting_for_task_custom_duration = State()

  process_task_duration = State()
  waiting_for_task_deadline = State()
  process_deadline = State()
  
  print_edit_tasks_page = State()

  edit_task = State()
  edit_task_title_process = State()
  waiting_for_transfer_time = State()
  waiting_for_transfer_date = State()
  
  edit_task_duration_process = State()
  edit_task_custom_duration= State()
  edit_task_deadline_process = State()

  edit_weekly_task = State()
  edit_task_date_process = State()
  add_task_date = State()
  add_task_date_process = State()

  waiting_day_date = State()
  waiting_project_name = State()
  on_current_project_page = State()
  waiting_project_member_name = State()
  waiting_member_name_for_delete = State()
  on_project_tasks_page = State()
  process_responsible_person = State()
  waiting_for_responsible_person = State()
  process_person_name = State()
  waiting_edit_responsible_person = State()

  editing_project_task = State()
  mark_as_done_project_task = State()
  waiting_for_project_task_name = State()