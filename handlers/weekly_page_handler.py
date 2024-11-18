from aiogram import Router
from aiogram.filters import Command
from models import Messages
from states.states import UserState
from aiogram.fsm.context import FSMContext
import datetime
from services import user_service, task_service, KeyboardService
from utils import add_daily_task, get_first_day_of_week, get_selected_day, get_username_from_message
from aiogram.types import (
  InlineKeyboardMarkup,
  InlineKeyboardButton,
)
from .daily_page_handers import show_daily_tasks

router = Router()
PAGE_SIZE = 9

@router.message(lambda message: message.text == "Недельные задачи 📅", UserState.on_start_page)
async def show_weekly_tasks(message, state: FSMContext):
  """
  Отображение страницы недельных задач
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
        message_text += f"{i}. {task.title}\n"
        if task.start_time:
          message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
        message_text += f"   ⏱ Длительность: {task.duration} минут\n"
        if task.deadline:
          message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
        message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n"
    message_text += "\n"

    i = 0

    message_text += "Вторник:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 1:
        i += 1
        message_text += f"{i}. {task.title}\n"
        if task.start_time:
          message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
        message_text += f"   ⏱ Длительность: {task.duration} минут\n"
        if task.deadline:
          message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
        message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n"
    message_text += "\n"

    i = 0

    message_text += "Среда:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 2:
        i += 1
        message_text += f"{i}. {task.title}\n"
        if task.start_time:
          message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
        message_text += f"   ⏱ Длительность: {task.duration} минут\n"
        if task.deadline:
          message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
        message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n"
    message_text += "\n"

    i = 0
    message_text += "Четверг:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 3:
        i += 1
        message_text += f"{i}. {task.title}\n"
        if task.start_time:
          message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
        message_text += f"   ⏱ Длительность: {task.duration} минут\n"
        if task.deadline:
          message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
        message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n"
    message_text += "\n"

    i = 0
    message_text += "Пятница:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 4:
        i += 1
        message_text += f"{i}. {task.title}\n"
        if task.start_time:
          message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
        message_text += f"   ⏱ Длительность: {task.duration} минут\n"
        if task.deadline:
          message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
        message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n"
    message_text += "\n"

    i = 0

    message_text += "Суббота:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 5:
        i += 1
        message_text += f"{i}. {task.title}\n"
        if task.start_time:
          message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
        message_text += f"   ⏱ Длительность: {task.duration} минут\n"
        if task.deadline:
          message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
        message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n"
    message_text += "\n"

    i = 0

    message_text += "Воскресенье:\n"
    for task in tasks:
      if task.day_date and task.day_date.weekday() == 6:
        i += 1
        message_text += f"{i}. {task.title}\n"
        if task.start_time:
          message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
        message_text += f"   ⏱ Длительность: {task.duration} минут\n"
        if task.deadline:
          message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
        message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n"
    message_text += "\n"

    i = 0
    message_text += "Не назначенные задачи:\n"
    for task in tasks:
      if not task.day_date:
        i += 1
        message_text += f"{i + 1}. {task.title}\n"
        if task.start_time:
          message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
        message_text += f"   ⏱ Длительность: {task.duration} минут\n"
        if task.deadline:
          message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
        message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n"
    message_text += "\n"

  await state.set_state(UserState.on_week_page)
  await state.update_data({"week_first_day_date": get_first_day_of_week(datetime.date.today())})
  await state.update_data({"day_date": datetime.date.today()})

  keyboard = KeyboardService.get_weekly_tasks_keyboard(message.from_user.id)
  await message.answer(
    text=message_text,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "✏️ Редактировать задачу", UserState.on_week_page)
async def edit_weekly_task(message, state: FSMContext):
  """
  Отображение страницы редактирования недельной задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  data = await state.get_data()
  user_id = data.get("user_id", 0)
  if user_id == 0:
    user_id = message.from_user.id
    await state.update_data({"user_id": user_id})
  tasks = task_service.get_tasks_by_week_date(user_id, get_first_day_of_week(datetime.date.today()))
  if len(tasks) == 0:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Errors.no_tasks,
      reply_markup=keyboard
    )
    return

  data = await state.get_data()
  page_index = data.get("page", 1)
  message_text = "Ваши задачи, страница " + str(page_index) + ":\n\n"
  buttons = []

  if len(tasks) < page_index * PAGE_SIZE:
    for i in range(len(tasks) - (PAGE_SIZE * (page_index - 1))):
      button = InlineKeyboardButton(
        text=tasks[i + PAGE_SIZE * (page_index - 1)].title,
        callback_data="edit_weekly_task_" + str(tasks[PAGE_SIZE * (page_index - 1) + i].task_id)
      )
      buttons.append([button])
  else:
    current_page_tasks = tasks[(page_index - 1) * PAGE_SIZE: (page_index) * PAGE_SIZE]
    for i in range(PAGE_SIZE):
      button = InlineKeyboardButton(
        text=current_page_tasks[i].title,
        callback_data="edit_weekly_task_" + str(current_page_tasks[i].task_id)
      )
      buttons.append([button])

  if page_index > 1:
    button = InlineKeyboardButton(
      text="⬅️",
      callback_data="edit_weekly_page_" + str(page_index - 1)
    )
    buttons.append([button])

  if len(tasks) > page_index * PAGE_SIZE:
    button = InlineKeyboardButton(
      text="➡️",
      callback_data="edit_weekly_page_" + str(page_index + 1)
    )
    buttons.append([button])

  keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
  await state.set_state(UserState.edit_weekly_task)
  await message.answer(
    text=message_text,
    reply_markup=keyboard
  )

@router.callback_query(lambda query: query.data.startswith("edit_weekly_page_"))
async def edit_weekly_page(callback_query, state: FSMContext):
  """
  Переход на другую страницу редактирования недельной задачи
  """
  user_service.update_user_exists(callback_query.from_user.id, get_username_from_message(callback_query))

  page_index = int(callback_query.data.split("_")[3])
  await state.update_data({"page": page_index})
  await state.update_data({"user_id": callback_query.from_user.id})
  await edit_weekly_task(callback_query.message, state)

@router.message(lambda message: message.text == "✅ Отметить выполненной", UserState.on_week_page)
async def mark_as_done(message, state: FSMContext):
  """
  Отметка задачи как выполненной
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  data = await state.get_data()
  user_id = data.get("user_id", 0)
  if user_id == 0:
    user_id = message.from_user.id
    await state.update_data({"user_id": user_id})
  tasks = task_service.get_tasks_by_week_date(user_id, get_first_day_of_week(datetime.date.today()))
  if len(tasks) == 0:
    print("test")
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Errors.no_tasks,
      reply_markup=keyboard
    )
    return

  data = await state.get_data()
  page_index = data.get("page", 1)
  message_text = "Ваши задачи, страница " + str(page_index) + ":\n\n"
  buttons = []

  if len(tasks) < page_index * PAGE_SIZE:
    for i in range(len(tasks) - (PAGE_SIZE * (page_index - 1))):
      button = InlineKeyboardButton(
        text=tasks[i + PAGE_SIZE * (page_index - 1)].title,
        callback_data="edit_weekly_task_status_" + str(tasks[PAGE_SIZE * (page_index - 1) + i].task_id)
      )
      buttons.append([button])
  else:
    current_page_tasks = tasks[(page_index - 1) * PAGE_SIZE: (page_index) * PAGE_SIZE]
    for i in range(PAGE_SIZE):
      button = InlineKeyboardButton(
        text=current_page_tasks[i].title,
        callback_data="edit_weekly_task_status_" + str(current_page_tasks[i].task_id)
      )
      buttons.append([button])

  if page_index > 1:
    button = InlineKeyboardButton(
      text="⬅️",
      callback_data="edit_weekly_page_" + str(page_index - 1)
    )
    buttons.append([button])

  if len(tasks) > page_index * PAGE_SIZE:
    button = InlineKeyboardButton(
      text="➡️",
      callback_data="edit_weekly_page_" + str(page_index + 1)
    )
    buttons.append([button])

  keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
  await state.set_state(UserState.edit_weekly_task)
  await message.answer(
    text=message_text,
    reply_markup=keyboard
  )

@router.callback_query(lambda query: query.data.startswith("edit_weekly_task_status_"))
async def edit_weekly_task_status(callback_query, state: FSMContext):
  """
  Изменение статуса задачи
  """
  user_service.update_user_exists(callback_query.from_user.id, get_username_from_message(callback_query))

  task_id = int(callback_query.data.split("_")[4])
  task = task_service.get_task_by_id(task_id)

  if task is None:
    keyboard = KeyboardService.get_return_main_page_keyboard(callback_query.from_user.id)
    await callback_query.message.answer(
      text=Messages.Errors.task_not_found,
      reply_markup=keyboard
    )

  if task.completed:
    keyboard = KeyboardService.get_return_main_page_keyboard(callback_query.from_user.id)
    await callback_query.message.answer(
      text="Задача уже выполнена!",
      reply_markup=keyboard
    )
    return
  
  task_service.invert_task_status(task_id)

  await state.set_state(UserState.on_week_page)
  keyboard = KeyboardService.get_main_page_keyboard(callback_query.from_user.id)
  await callback_query.message.answer(
    text="Статус задачи изменен!",
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "📝 Добавить задачу", UserState.on_week_page)
async def add_weekly_task(message, state: FSMContext):
  """
  Добавление новой недельной задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_data({
    "user_id": message.from_user.id,
    "week_first_day_date": get_first_day_of_week(datetime.date.today()),
    "day_date": None
  })

  await state.set_state(UserState.add_task_date)
  keyboard = KeyboardService.get_yes_or_no_keyboard(message.from_user.id)
  await message.answer(
    text="Прикреплена ли задача к конкретной дате?",
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "🔄 Перенести на следующую неделю", UserState.on_week_page)
async def move_to_next_week(message, state: FSMContext):
  """
  Перенос задач на следующую неделю
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  data = await state.get_data()
  week_date = data.get("week_first_day_date")
  task_service.move_to_next_week(message.from_user.id, week_date)

  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Задачи перенесены на следующую неделю",
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "⬅️ Ежедневные задачи", UserState.on_week_page)
async def show_daily_tasks_from_week(message, state: FSMContext):
  """
  Показать ежедневные задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.waiting_day_date)
  keyboard = KeyboardService.get_edit_task_date_keyboard(message.from_user.id)

  await message.answer(
    text=Messages.AddTask.edit_task_date,
    reply_markup=keyboard
  )

@router.message(UserState.waiting_day_date)
async def process_day_date(message, state: FSMContext):
  """
  Показать ежедневные задачи
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  day_date, error = get_selected_day(message.text)
  if error:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return

  data = await state.get_data()
  week_first_day = data.get("week_first_day_date")
  date = week_first_day + datetime.timedelta(days=day_date)

  await state.update_data({"day_date": date})
  await show_daily_tasks(message, state)

@router.message(lambda message: message.text == "⏩ Автораспределение", UserState.on_week_page)
async def distribute_weekly_tasks(message, state: FSMContext):
  """
  Распределение задач равномерно на неделю
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  data = await state.get_data()
  week_first_day = data.get("week_first_day_date")

  task_service.distribute_tasks(message.from_user.id, week_first_day)

  await state.set_state(UserState.on_start_page)
  keyboard = KeyboardService.get_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Задачи распределены",
    reply_markup=keyboard
  )