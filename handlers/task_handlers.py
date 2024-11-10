from aiogram import Router
from models import Messages
from states.states import UserState
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from services import user_service, task_service
from utils import add_daily_task, return_to_main_page as main_page, get_username_from_message
from utils import get_custom_task_duration, get_template_task_duration, get_deadline, get_selected_day
from services import KeyboardService
from aiogram.types import (
  InlineKeyboardMarkup,
  InlineKeyboardButton,
)
import datetime

router = Router()
PAGE_SIZE = 9

@router.message(lambda message: message.text == "🔙 Главное меню")
async def return_to_main_page(message, state: FSMContext):
  """
  Функция, которая возвращает на главную страницу
  """
  await main_page(message, state)

@router.message(UserState.waiting_for_task_name)
async def process_task_name(message, state: FSMContext):
  """
  Функция, которая обрабатывает название задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  try:
    task_name = message.text.strip()
  except ValueError:
    keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Error.something_went_wrong,
      reply_markup=keyboard
    )
    return

  await state.set_state(UserState.process_task_duration)
  await state.update_data({"title": task_name})

  keyboard = KeyboardService.get_task_duration_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.task_duration_question,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Ввести свое время", UserState.process_task_duration)
async def process_task_duration(message, state: FSMContext):
  """
  Функция, которая обрабатывает длительность задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.set_state(UserState.waiting_for_task_custom_duration)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.custom_task_duration,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "🔙 Изменить название задачи", UserState.process_task_duration)
async def change_task_name(message, state: FSMContext):
  """
  Возвращает на страницу изменения названия задачи
  """
  await add_daily_task(message, state)

@router.message(UserState.process_task_duration)
async def process_template_task_duration(message, state: FSMContext):
  """
  Функция, которая обрабатывает длительность задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  hours, minutes, error = get_template_task_duration(message.text)
  if hours is None:
    keyboard = KeyboardService.get_task_duration_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return
  
  await state.update_data({"duration": [hours, minutes]})
  await state.set_state(UserState.process_deadline)

  keyboard = KeyboardService.get_deadline_exists_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.deadline_exists_question,
    reply_markup=keyboard
  )

@router.message(UserState.waiting_for_task_custom_duration)
async def process_custom_task_duration(message, state: FSMContext):
  """
  Функция, которая обрабатывает длительность задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  
  hours, minutes, error = get_custom_task_duration(message.text)
  if hours is None:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return
  
  await state.update_data({"duration": [hours, minutes]})
  await state.set_state(UserState.process_deadline)

  keyboard = KeyboardService.get_deadline_exists_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.deadline_exists_question,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Да, дедлайн будет", UserState.process_deadline)
async def process_deadline(message, state: FSMContext):
  """
  Функция, которая обрабатывает дедлайн задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.waiting_for_task_deadline)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.get_deadline,
    reply_markup=keyboard
  )

async def final_stage_add_task(message, state: FSMContext):
  """
  Функция, которая обрабатывает дедлайн задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Задача добавлена!",
    reply_markup=keyboard
  )

@router.message(UserState.waiting_for_task_deadline)
async def process_deadline(message, state: FSMContext):
  """
  Функция, которая обрабатывает дедлайн задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  
  data = await state.get_data()
  current_date = data.get("day_date")

  deadline_time, error = get_deadline(message.text, current_date)
  if deadline_time is None:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return

  await state.update_data({"deadline": deadline_time})
  telegram_id = message.from_user.id
  data = await state.get_data()
  task_service.create_task(telegram_id, data)

  await final_stage_add_task(message, state)

@router.message(lambda message: message.text == "Нет, дедлайна не будет", UserState.process_deadline)
async def process_deadline(message, state: FSMContext):
  """
  Функция, которая обрабатывает дедлайн задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.update_data({"deadline": None})

  telegram_id = message.from_user.id
  data = await state.get_data()
  task_service.create_task(telegram_id, data)

  await final_stage_add_task(message, state)

async def print_tasks_page(message, state: FSMContext):
  """
  Функция, которая печатает страницу задач
  """
  data = await state.get_data()

  page_index = data.get("page", 1)
  tasks = data.get("tasks", [])
  message_text = "Ваши задачи, страница " + str(page_index) + ":\n\n"
  buttons = []

  if len(tasks) == 0:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Error.no_tasks,
      reply_markup=keyboard
    )
    return
  
  if len(tasks) < page_index * PAGE_SIZE:
    for i in range(len(tasks) - (PAGE_SIZE * (page_index - 1))):
      button = InlineKeyboardButton(
        text=tasks[PAGE_SIZE * (page_index - 1) + i].title,
        callback_data="edit_task_" + str(tasks[PAGE_SIZE * (page_index - 1) + i].task_id)
      )
      buttons.append([button])
  else:
    current_page_tasks = tasks[(page_index - 1) * PAGE_SIZE: (page_index) * PAGE_SIZE]
    for i in range(PAGE_SIZE):
      button = InlineKeyboardButton(
        text=current_page_tasks[i].title,
        callback_data="edit_task_" + str(current_page_tasks[i].task_id)
      )
      buttons.append([button])
  
  if page_index > 1:
    button = InlineKeyboardButton(
      text="⬅️",
      callback_data="prev_tasks_page_" + str(page_index)
    )
    buttons.append([button])

  if len(tasks) > (page_index) * PAGE_SIZE:
    button = InlineKeyboardButton(
      text="➡️",
      callback_data="next_tasks_page_" + str(page_index)
    )
    buttons.append([button])
  page_keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

  await state.update_data({"tasks": tasks, "page": page_index})
  await state.set_state(UserState.print_edit_tasks_page)
  await message.answer(
    text=message_text,
    reply_markup=page_keyboard
  )

@router.callback_query(lambda call: call.data.startswith("prev_tasks_page_"))
async def prev_tasks_page(call, state: FSMContext):
  """
  Функция, которая обрабатывает предыдущую страницу задач
  """
  user_service.update_user_exists(call.from_user.id, get_username_from_message(call))

  data = await state.get_data()
  page_index = data["page"] - 1
  await state.update_data({"page": page_index})
  await print_tasks_page(call.message, state)

@router.callback_query(lambda call: call.data.startswith("next_tasks_page_"))
async def next_tasks_page(call, state: FSMContext):
  """
  Функция, которая обрабатывает следующую страницу задач
  """
  user_service.update_user_exists(call.from_user.id, get_username_from_message(call))

  data = await state.get_data()
  page_index = data["page"] + 1
  await state.update_data({"page": page_index})
  await print_tasks_page(call.message, state)

@router.callback_query(lambda call: call.data.startswith("edit_task_"))
async def edit_task(call, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование задачи
  """
  user_service.update_user_exists(call.from_user.id, get_username_from_message(call))

  task_id = int(call.data.split("_")[2])

  await state.update_data({"task_id": task_id})
  await state.set_state(UserState.edit_task)
  keyboard = KeyboardService.get_edit_task_keyboard(call.from_user.id)
  await call.message.answer(
    text=Messages.AddTask.edit_task_question,
    reply_markup=keyboard
  )


@router.message(lambda message: message.text == "Название задачи", StateFilter(UserState.edit_task, UserState.edit_weekly_task))
async def edit_task_title_process(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование названия задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.set_state(UserState.edit_task_title_process)

  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.edit_task_title,
    reply_markup=keyboard
  )

@router.message(UserState.edit_task_title_process)
async def edit_task_title(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование названия задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  try:
    task_title = message.text.strip()
  except ValueError:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Error.something_went_wrong,
      reply_markup=keyboard
    )
    return
  
  data = await state.get_data()
  task_id = data["task_id"]
  task_service.edit_task_title(task_id, task_title)

  await state.set_state(UserState.on_start_page)
  await message.answer(
    text="Задача изменена!",
    reply_markup=KeyboardService.get_main_page_keyboard(message.from_user.id)
  )

@router.message(lambda message: message.text == "Длительность задачи", StateFilter(UserState.edit_task, UserState.edit_weekly_task))
async def edit_task_duration(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование длительности задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  
  await state.set_state(UserState.edit_task_duration_process)
  keyboard = KeyboardService.get_task_duration_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.edit_task_duration,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Ввести свое время", UserState.edit_task_duration_process)
async def edit_task_custom_duration(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование длительности задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.set_state(UserState.edit_task_custom_duration)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.custom_task_duration,
    reply_markup=keyboard
  )

@router.message(UserState.edit_task_custom_duration)
async def edit_task_duration_process(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование длительности задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  hours, minutes, error = get_custom_task_duration(message.text)
  if hours is None:
    keyboard = KeyboardService.get_task_duration_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return
  
  data = await state.get_data()
  task_id = data["task_id"]
  task_service.edit_task_duration(task_id, hours * 60 + minutes)

  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Задача изменена!",
    reply_markup=keyboard
  )

@router.message(UserState.edit_task_duration_process)
async def edit_task_duration(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование длительности задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  
  hours, minutes, error = get_template_task_duration(message.text)
  if hours is None:
    keyboard = KeyboardService.get_task_duration_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return
  
  data = await state.get_data()
  task_id = data["task_id"]
  task_service.edit_task_duration(task_id, hours * 60 + minutes)

  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Задача изменена!",
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Дедлайн задачи", StateFilter(UserState.edit_task, UserState.edit_weekly_task))
async def edit_task_deadline(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование дедлайна задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  
  await state.set_state(UserState.edit_task_deadline_process)

  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.get_deadline,
    reply_markup=keyboard
  )

@router.message(UserState.edit_task_deadline_process)
async def edit_task_deadline_process(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование дедлайна задачи  
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  data = await state.get_data()
  current_date = data.get("day_date")

  deadline_time, error = get_deadline(message.text, current_date)
  if deadline_time is None:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return

  data = await state.get_data()
  task_id = data["task_id"]
  task_service.edit_task_deadline(task_id, deadline_time)

  await state.clear()
  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Задача изменена!",
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Изменить статус задачи", StateFilter(UserState.edit_task, UserState.edit_weekly_task))
async def edit_task_status(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование статуса задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  
  data = await state.get_data()
  task_id = data["task_id"]
  task_service.invert_task_status(task_id)

  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Статус задачи изменен!",
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Ответственный за задачу", UserState.edit_task)
async def edit_task_responsible_person(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование ответственного за задачу
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.waiting_edit_responsible_person)

  keyboard = KeyboardService.get_return_main_page_or_back_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.Project.add_project_member,
    reply_markup=keyboard
  )

@router.message(UserState.edit_task)
async def unknown_message_edit_task(message, state: FSMContext):
  """
  Функция, которая обрабатывает неизвестные сообщения при редактировании задачи 
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await state.set_state(UserState.on_start_page)
  await message.answer(
    text=Messages.Errors.choose_duration_from_keyboard_error,
    reply_markup=keyboard
  )

@router.callback_query(lambda call: call.data.startswith("edit_status_"))
async def edit_status(call, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование статуса задачи
  """
  user_service.update_user_exists(call.from_user.id, get_username_from_message(call))

  task_id = int(call.data.split("_")[2])
  task = task_service.get_task_by_id(task_id)

  if task is None:
    keyboard = KeyboardService.get_return_main_page_keyboard(call.from_user.id)
    await call.message.answer(
      text=Messages.Errors.task_not_found,
      reply_markup=keyboard
    )

  if task.completed:
    keyboard = KeyboardService.get_return_main_page_keyboard(call.from_user.id)
    await call.message.answer(
      text="Задача уже выполнена!",
      reply_markup=keyboard
    )
    return
  
  task_service.invert_task_status(task_id)

  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(call.from_user.id)
  await call.message.answer(
    text="Статус задачи изменен!",
    reply_markup=keyboard
  )

@router.callback_query(lambda call: call.data.startswith("edit_weekly_task_"), UserState.on_week_page)
async def edit_weekly_task(call, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование задачи
  """
  user_service.update_user_exists(call.from_user.id, get_username_from_message(call))

  task_id = int(call.data.split("_")[3])

  await state.update_data({"task_id": task_id})
  await state.set_state(UserState.edit_weekly_task)
  keyboard = KeyboardService.get_edit_weekly_task_keyboard(call.from_user.id)
  await call.message.answer(
    text=Messages.AddTask.edit_task_question,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Изменить назначенный день задачи", UserState.edit_weekly_task)
async def edit_weekly_task_date(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование даты задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  
  await state.set_state(UserState.edit_task_date_process)
  keyboard = KeyboardService.get_edit_task_date_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.edit_task_date,
    reply_markup=keyboard
  )

@router.message(UserState.edit_task_date_process)
async def edit_weekly_task_monday(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование даты задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  message_text = message.text
  add_day, err = get_selected_day(message_text)

  if err:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=err,
      reply_markup=keyboard
    )
    return
  
  data =  await state.get_data()
  week_first_day = data.get("week_first_day_date")
  task_id = data.get("task_id")
  date = week_first_day + datetime.timedelta(days=add_day)

  task_service.edit_task_date(task_id, date)

  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Задача изменена!",
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Да", UserState.add_task_date)
async def add_task_date_yes(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование даты задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  
  await state.set_state(UserState.add_task_date_process)
  keyboard = KeyboardService.get_edit_task_date_keyboard(message.from_user.id)

  await message.answer(
    text=Messages.AddTask.edit_task_date,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Нет", UserState.add_task_date)
async def add_task_date_no(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование даты задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  
  await add_daily_task(message, state)

@router.message(UserState.add_task_date)
async def add_task_date(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование даты задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  
  keyboard = KeyboardService.get_yes_or_no_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.Errors.choose_from_keyboard,
    reply_markup=keyboard
  )

@router.message(UserState.add_task_date_process)
async def add_task_date_process(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование даты задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  message_text = message.text
  add_day, err = get_selected_day(message_text)

  if err:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=err,
      reply_markup=keyboard
    )
    return
  
  data =  await state.get_data()
  week_first_day = data.get("week_first_day_date")
  date = week_first_day + datetime.timedelta(days=add_day)

  await state.update_data({"day_date": date})
  await add_daily_task(message, state)