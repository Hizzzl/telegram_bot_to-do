from aiogram import Router
from models import Messages
from states.states import UserState
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from services import user_service, task_service
from utils import add_daily_task, return_to_main_page as main_page, get_username_from_message
from utils import get_custom_task_duration, get_template_task_duration, get_deadline, get_selected_day
from utils import get_task_start_time
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

  await state.update_data({"title": task_name})


  data = await state.get_data()
  day_date = data.get("day_date", None)
  if day_date is not None:
    await state.set_state(UserState.process_task_start_time)
    keyboard = KeyboardService.get_task_start_time_exists_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.AddTask.task_start_time_exists_question,
      reply_markup=keyboard
    )
  else:
    await state.set_state(UserState.process_task_duration)
    keyboard = KeyboardService.get_task_duration_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.AddTask.task_duration_question,
      reply_markup=keyboard
    )

@router.message(lambda message: message.text == "Да, будет время начала", UserState.process_task_start_time)
async def process_task_start_time_yes(message, state: FSMContext):
  """
  Функция, которая обрабатывает наличие времени начала задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.set_state(UserState.waiting_for_task_start_time)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.task_start_time_question,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Нет, не будет времени начала", UserState.process_task_start_time)
async def process_task_start_time_no(message, state: FSMContext):
  """
  Функция, которая обрабатывает отсутствие времени начала задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.update_data({"start_time": None})
  await state.set_state(UserState.process_task_duration)

  keyboard = KeyboardService.get_task_duration_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.task_duration_question,
    reply_markup=keyboard
  )

@router.message(UserState.waiting_for_task_start_time)
async def process_task_start_time_input(message, state: FSMContext):
  """
  Функция, которая обрабатывает ввод времени начала задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  start_time, error = get_task_start_time(message.text)
  print(start_time, error)
  if error:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return

  await state.update_data({"start_time": start_time})
  await state.set_state(UserState.process_task_duration)

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
    tasks_on_page = tasks[len(tasks) - (PAGE_SIZE * (page_index - 1)):]
  else:
    tasks_on_page = tasks[(page_index - 1) * PAGE_SIZE: (page_index) * PAGE_SIZE]
  
  for i in range(len(tasks_on_page)):
    task = tasks_on_page[i]
    task_text = f"{i + 1}. {task.title}\n"
    
    if task.start_time:
      task_text += f"   🕒 Начало: {task.start_time.strftime('%d.%m.%Y %H:%M')}\n"
    
    task_text += f"   ⏱ Длительность: {task.duration} минут\n"
    
    if task.deadline:
      task_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
    
    if task.responsible_id:
      responsible = user_service.get_user_by_id(task.responsible_id)
      if responsible:
        task_text += f"   👤 Ответственный: {responsible.username}\n"
    
    task_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n\n"
    
    message_text += task_text
  
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
  task_id = int(call.data.split("_")[2], 0)
  
  task = task_service.get_task_by_id(task_id)
  if task is None:
    keyboard = KeyboardService.get_return_main_page_keyboard(call.from_user.id)
    await call.message.answer(
      text=Messages.Error.task_not_found,
      reply_markup=keyboard
    )
    return

  await state.update_data({"task_id": task_id})
  await state.set_state(UserState.edit_task)

  task_info = f"Редактирование задачи:\n\n"
  task_info += f"📝 Название: {task.title}\n"
  if task.start_time:
    task_info += f"🕒 Начало: {task.start_time.strftime('%d.%m.%Y %H:%M')}\n"
  task_info += f"⏱ Длительность: {task.duration} минут\n"
  if task.deadline:
    task_info += f"📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
  task_info += f"✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n"

  keyboard = KeyboardService.get_edit_task_keyboard(call.from_user.id)
  await call.message.answer(
    text=task_info,
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

@router.message(lambda message: message.text == "Время начала задачи", StateFilter(UserState.edit_task, UserState.edit_weekly_task))
async def transfer_task(message, state: FSMContext):
  """
  Функция, которая обрабатывает перенос задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  data = await state.get_data()
  task_id = data["task_id"]
  
  task = task_service.get_task_by_id(task_id)
  if not task.start_time and not task.day_date:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text="Задача не привязана к дате!",
      reply_markup=keyboard
    )
    return

  await state.set_state(UserState.waiting_for_transfer_time)

  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Введите новое время начала в формате ЧЧ:ММ:",
    reply_markup=keyboard
  )

@router.message(UserState.waiting_for_transfer_time)
async def transfer_task(message, state: FSMContext):
  """
  Функция, которая обрабатывает перенос задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  transfer_time, error = get_task_start_time(message.text)
  if error:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return

  data = await state.get_data()
  task_id = data["task_id"]
  task_service.edit_task_start_time(task_id, transfer_time)

  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Задача изменена!",
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Прикрепленный день", UserState.edit_task)
async def edit_project_task_date(message, state: FSMContext):
  """
  Функция, которая обрабатывает редактирование даты задачи проекта
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.set_state(UserState.waiting_for_task_start_date)

  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Введите дату начала задачи в формате ДД.ММ.ГГГГ:",
    reply_markup=keyboard
  )

@router.message(UserState.waiting_for_task_start_date)
async def process_project_task_date(message, state: FSMContext):
  """
  Функция, которая обрабатывает ввод даты задачи проекта
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  try:
    day_date = datetime.datetime.strptime(message.text.strip(), "%d.%m.%Y").date()
    if day_date < datetime.date.today():
      keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
      await message.answer(
        text="Дата не может быть в прошлом!",
        reply_markup=keyboard
      )
      return
  except ValueError:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text="Неверный формат даты!",
      reply_markup=keyboard
    )
    return

  data = await state.get_data()
  task_id = data["task_id"]
  
  task_service.edit_task_date(task_id, day_date)

  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Дата задачи изменена!",
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

@router.callback_query(lambda call: call.data.startswith("edit_weekly_task_"), UserState.edit_weekly_task)
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

@router.message(lambda message: message.text == "🔄 Перенести задачу", UserState.edit_task)
async def transfer_task(message, state: FSMContext):
  """
  Функция, которая обрабатывает перенос задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.set_state(UserState.waiting_for_transfer_date)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Введите новую дату начала задачи в формате ДД.ММ.ГГГГ:",
    reply_markup=keyboard
  )

@router.callback_query(lambda c: c.data == "transfer_task", UserState.edit_task)
async def transfer_task_inline(call, state: FSMContext):
  """
  Функция, которая обрабатывает перенос задачи (inline версия)
  """
  await state.set_state(UserState.waiting_for_transfer_date)
  keyboard = KeyboardService.get_return_main_page_keyboard(call.from_user.id)
  await call.message.answer(
    text="Введите новую дату начала задачи в формате ДД.ММ.ГГГГ:",
    reply_markup=keyboard
  )
  await call.answer()

@router.message(UserState.waiting_for_transfer_date)
async def process_transfer_date(message, state: FSMContext):
  """
  Функция, которая обрабатывает ввод новой даты начала задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  try:
    transfer_date = datetime.datetime.strptime(message.text.strip(), "%d.%m.%Y")
    data = await state.get_data()
    task_id = data.get("task_id")
    task = task_service.get_task_by_id(task_id)
    
    if task.start_time:
      # Если у задачи было время начала, спросим новое время
      await state.update_data({"transfer_date": transfer_date})
      await state.set_state(UserState.waiting_for_transfer_time)
      keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
      await message.answer(
        text="Введите новое время начала в формате ЧЧ:ММ:",
        reply_markup=keyboard
      )
    else:
      # Если времени начала не было, просто обновляем дату
      task_service.update_task(task_id, {"start_time": transfer_date})
      await state.set_state(UserState.edit_task)
      keyboard = KeyboardService.get_edit_task_keyboard(message.from_user.id)
      await message.answer(
        text=f"Задача перенесена на {transfer_date.strftime('%d.%m.%Y')}",
        reply_markup=keyboard
      )
      
  except ValueError:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text="Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ",
      reply_markup=keyboard
    )

@router.message(UserState.waiting_for_transfer_time)
async def process_transfer_time(message, state: FSMContext):
  """
  Функция, которая обрабатывает ввод нового времени начала задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  try:
    time_parts = message.text.strip().split(":")
    if len(time_parts) != 2:
      raise ValueError()
    
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    
    if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
      raise ValueError()
      
    data = await state.get_data()
    transfer_date = data.get("transfer_date")
    task_id = data.get("task_id")
    
    new_datetime = transfer_date.replace(hour=hours, minute=minutes)
    task_service.update_task(task_id, {"start_time": new_datetime})
    
    await state.set_state(UserState.edit_task)
    keyboard = KeyboardService.get_edit_task_keyboard(message.from_user.id)
    await message.answer(
      text=f"Задача перенесена на {new_datetime.strftime('%d.%m.%Y %H:%M')}",
      reply_markup=keyboard
    )
    
  except ValueError:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text="Неверный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ",
      reply_markup=keyboard
    )