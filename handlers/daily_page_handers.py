from aiogram import Router
from aiogram.filters import Command
from models import Messages
from states.states import UserState
from aiogram.fsm.context import FSMContext
import datetime
from services import user_service, task_service, KeyboardService
from utils import add_daily_task as process_daily_task, get_first_day_of_week, get_username_from_message
from aiogram.types import (
  InlineKeyboardMarkup,
  InlineKeyboardButton,
)

router = Router()
PAGE_SIZE = 9

@router.message(lambda message: message.text == "Ежедневные задачи 📅", UserState.on_start_page)
async def show_daily_tasks(message, state: FSMContext):
  """
  Показать ежедневные задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  message_text = ""

  data = await state.get_data()
  day_date = data.get("day_date", datetime.date.today())

  tasks = task_service.get_tasks_by_date(message.from_user.id, day_date)
  if len(tasks) == 0:
    message_text = Messages.Errors.no_tasks
  else:
    message_text = "Ваши задачи:\n\n"
    for i, task in enumerate(tasks):
      message_text += f"{i + 1}. {task.title}\n"
      if task.start_time:
        message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
      message_text += f"   ⏱ Длительность: {task.duration} минут\n"
      if task.deadline:
        message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
      message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n\n"

  await state.set_state(UserState.on_day_page)
  await state.update_data({"week_first_day_date": get_first_day_of_week(datetime.date.today())})
  
  day_date = data.get("day_date", datetime.date.today())
  if day_date == datetime.date.today():
    await state.update_data({"day_date": datetime.date.today()})

  keyboard = KeyboardService.get_daily_tasks_keyboard(message.from_user.id)
  await message.answer(
    text=message_text,
    reply_markup=keyboard
  )


@router.message(lambda message: message.text == "➕ Добавить задачу", UserState.on_day_page)
async def add_daily_task(message, state: FSMContext):
  """
  Добавить ежедневную задачу
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await process_daily_task(message, state)

@router.message(lambda message: message.text == "✏️ Редактировать задачу", UserState.on_day_page)
async def edit_daily_task(message, state: FSMContext):
  """
  Отобразить список ежедневных задач для редактирования
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  tasks = task_service.get_tasks_by_date(message.from_user.id, datetime.date.today())

  if len(tasks) == 0:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Errors.no_tasks,
      reply_markup=keyboard
    )
    return

  page_index = 1
  message_text = "Ваши задачи, страница " + str(page_index) + ":\n\n"
  buttons = []

  if len(tasks) < page_index * PAGE_SIZE:
    for i in range(len(tasks)):
      button = InlineKeyboardButton(
        text=tasks[i].title,
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

@router.message(lambda message: message.text == "✅ Отметить выполненной", UserState.on_day_page)
async def mark_daily_task(message, state: FSMContext):
  """
  Отобразить список ежедневных задач для отметки выполненной
  """
  data = await state.get_data()
  day_date = data.get("day_date", datetime.date.today())

  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  tasks = task_service.get_tasks_by_date(message.from_user.id, day_date)

  if len(tasks) == 0:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Errors.no_tasks,
      reply_markup=keyboard
    )
    return

  page_index = 1
  message_text = "Ваши задачи, страница " + str(page_index) + ". Выберите задачу для отметки выполненной:\n\n"
  buttons = []

  if len(tasks) < page_index * PAGE_SIZE:
    for i in range(len(tasks)):
      button = InlineKeyboardButton(
        text=tasks[i].title,
        callback_data="edit_status_" + str(tasks[PAGE_SIZE * (page_index - 1) + i].task_id)
      )
      buttons.append([button])
  else:
    current_page_tasks = tasks[(page_index - 1) * PAGE_SIZE: (page_index) * PAGE_SIZE]
    for i in range(PAGE_SIZE):
      button = InlineKeyboardButton(
        text=current_page_tasks[i].title,
        callback_data="edit_status_" + str(current_page_tasks[i].task_id)
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

@router.message(lambda message: message.text == "➡️ Завтрашние задачи", UserState.on_day_page)
async def show_tomorrow_tasks(message, state: FSMContext):
  """
  Показать завтрашние задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  message_text = ""

  data = await state.get_data()
  curr_date = data.get("day_date", datetime.date.today())
  day_date = curr_date + datetime.timedelta(days=1)

  tasks = task_service.get_tasks_by_date(message.from_user.id, day_date)

  if len(tasks) == 0:
    message_text = Messages.Errors.no_tasks
  else:
    message_text = "Задачи за " + str(day_date) + ":\n\n"
    for i, task in enumerate(tasks):
      message_text += f"{i + 1}. {task.title}\n"
      if task.start_time:
        message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
      message_text += f"   ⏱ Длительность: {task.duration} минут\n"
      if task.deadline:
        message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
      message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n\n"


  await state.set_state(UserState.on_day_page)
  await state.update_data({"week_first_day_date": get_first_day_of_week(day_date)})
  await state.update_data({"day_date": day_date})

  keyboard = KeyboardService.get_daily_tasks_keyboard(message.from_user.id)
  await message.answer(
    text=message_text,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "🔄 Перенести на завтра", UserState.on_day_page)
async def move_tomorrow_tasks(message, state: FSMContext):
  """
  Перенести задачи на завтра
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  data = await state.get_data()
  curr_date = data.get("day_date", datetime.date.today())
  day_date = curr_date + datetime.timedelta(days=1)

  task_service.move_tasks_by_date(message.from_user.id, curr_date, day_date)

  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Задачи перенесены на " + str(day_date) + ".",
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "📅 Недельные задачи", UserState.on_day_page)
async def show_weekly_tasks(message, state: FSMContext):
  """
  Показать недельные задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  message_text = ""
  tasks = task_service.get_tasks_by_week_date(message.from_user.id, get_first_day_of_week(datetime.date.today()))

  if len(tasks) == 0:
    message_text = Messages.Errors.no_tasks
  else:
    message_text = "Ваши задачи:\n\n"
    message_text += "Понедельник:\n"
    i = 0
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 0:
        i += 1
        if task.completed:
          check = "✅"
        else:
          check = "❌"
        message_text += str(i) + ".\n" + "Название: " + str(task.title) + "\n" + "Выполнено: " + check + "\n" + "Дедлайн: " + str(task.deadline) + "\n" + "Длительность: " + str(task.duration) + " минут\n"
    message_text += "\n"

    i = 0

    message_text += "Вторник:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 1:
        i += 1
        if task.completed:
          check = "✅"
        else:
          check = "❌"
        message_text += str(i) + ".\n" + "Название: " + str(task.title) + "\n" + "Выполнено: " + check + "\n" + "Дедлайн: " + str(task.deadline) + "\n" + "Длительность: " + str(task.duration) + " минут\n"
    message_text += "\n"

    i = 0

    message_text += "Среда:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 2:
        i += 1
        if task.completed:
          check = "✅"
        else:
          check = "❌"
        message_text += str(i) + ".\n" + "Название: " + str(task.title) + "\n" + "Выполнено: " + check + "\n" + "Дедлайн: " + str(task.deadline) + "\n" + "Длительность: " + str(task.duration) + " минут\n"
    message_text += "\n"

    i = 0
    message_text += "Четверг:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 3:
        i += 1
        if task.completed:
          check = "✅"
        else:
          check = "❌"
        message_text += str(i) + ".\n" + "Название: " + str(task.title) + "\n" + "Выполнено: " + check + "\n" + "Дедлайн: " + str(task.deadline) + "\n" + "Длительность: " + str(task.duration) + " минут\n"
    message_text += "\n"

    i = 0
    message_text += "Пятница:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 4:
        i += 1
        if task.completed:
          check = "✅"
        else:
          check = "❌"
        message_text += str(i) + ".\n" + "Название: " + str(task.title) + "\n" + "Выполнено: " + check + "\n" + "Дедлайн: " + str(task.deadline) + "\n" + "Длительность: " + str(task.duration) + " минут\n"
    message_text += "\n"

    i = 0

    message_text += "Суббота:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 5:
        i += 1
        if task.completed:
          check = "✅"
        else:
          check = "❌"
        message_text += str(i) + ".\n" + "Название: " + str(task.title) + "\n" + "Выполнено: " + check + "\n" + "Дедлайн: " + str(task.deadline) + "\n" + "Длительность: " + str(task.duration) + " минут\n"
    message_text += "\n"

    i = 0

    message_text += "Воскресенье:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 6:
        i += 1
        if task.completed:
          check = "✅"
        else:
          check = "❌"
        message_text += str(i) + ".\n" + "Название: " + str(task.title) + "\n" + "Выполнено: " + check + "\n" + "Дедлайн: " + str(task.deadline) + "\n" + "Длительность: " + str(task.duration) + " минут\n"

    i = 0
    message_text += "Не назначенные задачи:\n"
    for task in tasks:
      if not task.day_date:
        i += 1
        if task.completed:
          check = "✅"
        else:
          check = "❌"
        message_text += str(i) + ".\n" + "Название: " + str(task.title) + "\n" + "Выполнено: " + check + "\n" + "Дедлайн: " + str(task.deadline) + "\n" + "Длительность: " + str(task.duration) + " минут\n"
  await state.set_state(UserState.on_week_page)
  await state.update_data({"week_first_day_date": get_first_day_of_week(datetime.date.today())})
  await state.update_data({"day_date": datetime.date.today()})

  keyboard = KeyboardService.get_weekly_tasks_keyboard(message.from_user.id)
  await message.answer(
    text=message_text,
    reply_markup=keyboard
  )