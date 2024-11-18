from aiogram import Router
from states.states import UserState
from aiogram.fsm.context import FSMContext
from services import user_service, task_service, KeyboardService
from services.services_init import project_service
from utils import return_to_main_page, get_username, get_username_from_message
from models.messages import Messages
from aiogram.types import ReplyKeyboardRemove
from utils.navigation import add_daily_task as process_add_task
from utils import get_first_day_of_week
import datetime

from aiogram.types import (
  InlineKeyboardMarkup,
  ReplyKeyboardMarkup,
  InlineKeyboardButton,
)

router = Router()
PAGE_SIZE = 7
TASKS_PAGE_SIZE = 9

@router.message(lambda message: message.text == "Проекты 📝", UserState.on_start_page)
async def show_projects(message, state: FSMContext):
  """
  Выводит список проектов
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  data = await state.get_data()
  page = data.get("page", 1)
  user_id = data.get("user_id", message.from_user.id)

  print(user_id)
  projects = project_service.get_projects_by_user_id(user_id=user_id)

  await state.set_state(UserState.on_project_page)

  

  if len(projects) == 0:
    message_text = "У вас нет проектов"
  else:
    message_text = "Ваши проекты, страница " + str(page) + ":\n\n"

  
  buttons = []

  if len(projects) < page * PAGE_SIZE:
    for i in range(len(projects) - (PAGE_SIZE * (page - 1))):
      button = InlineKeyboardButton(
        text=projects[i + PAGE_SIZE * (page - 1)].name,
        callback_data="project_" + str(projects[PAGE_SIZE * (page - 1) + i].project_id)
      )
      buttons.append([button])
  else:
    for i in range(PAGE_SIZE):
      button = InlineKeyboardButton(
        text=projects[i + PAGE_SIZE * (page - 1)].name,
        callback_data="project_" + str(projects[PAGE_SIZE * (page - 1) + i].project_id)
      )
      buttons.append([button])

  if page > 1 and len(projects) > page * PAGE_SIZE:
    button1 = InlineKeyboardButton(
      text="⬅️",
      callback_data="projects_page_" + str(page - 1)
    )
    button2 = InlineKeyboardButton(
      text="➡️",
      callback_data="projects_page_" + str(page + 1)
    )
    buttons.append([button1, button2])
  else:

    if page > 1:
      button = InlineKeyboardButton(
        text="⬅️ Предыдущая страница",
        callback_data="projects_page_" + str(page - 1)
      )
      buttons.append([button])

    if len(projects) > page * PAGE_SIZE:
      button = InlineKeyboardButton(
        text="➡️ Следующая страница",
        callback_data="projects_page_" + str(page + 1)
      )
      buttons.append([button])

  button = InlineKeyboardButton(
    text = "➕ Добавить проект",
    callback_data="add_project"
  )

  buttons.append([button])
  button = InlineKeyboardButton(
    text = "🔙 Главное меню",
    callback_data="main_menu"
  )

  buttons.append([button])
  keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
  await message.answer(
    text="Переход на страницу проектов",
    reply_markup=ReplyKeyboardRemove(),
  )
  await message.answer(
    text=message_text,
    reply_markup=keyboard
  )
  
@router.callback_query(lambda call: call.data.startswith("projects_page_"), UserState.on_project_page)
async def project_page(call, state: FSMContext):
  """
  Функция, которая обрабатывает переход на другую страницу
  """
  user_service.update_user_exists(call.from_user.id, get_username_from_message(call))

  page = int(call.data.split("_")[2])
  await state.update_data({"page": page})
  await state.update_data({"user_id": call.from_user.id})
  await show_projects(call.message, state)

@router.callback_query(lambda call: call.data == "main_menu")
async def main_menu(call, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Главное меню"
  """
  user_service.update_user_exists(call.from_user.id, get_username_from_message(call))

  await state.set_state(UserState.on_start_page)
  await return_to_main_page(call.message, state)

@router.callback_query(lambda call: call.data == "add_project")
async def add_project(call, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Добавить проект"
  """
  user_service.update_user_exists(call.from_user.id, get_username_from_message(call))

  await state.set_state(UserState.waiting_project_name)
  keyboard = KeyboardService.get_return_main_page_keyboard(call.from_user.id)
  await call.message.answer(
    text=Messages.Project.get_project_name,
    reply_markup=keyboard
  )

@router.message(UserState.waiting_project_name)
async def process_project_name(message, state: FSMContext):
  """
  Функция, которая обрабатывает ввод названия проекта
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  project_name = message.text.strip()
  await state.update_data({"title": project_name})
  project_service.create_project(message.from_user.id, project_name)

  await show_projects(message, state)

async def show_current_project_page(message, state: FSMContext):
  """
  Функция, которая обрабатывает переход на страницу проекта
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  data = await state.get_data()
  project_id = data.get("project_id", None)
  if not project_id:
    await show_projects(message, state)
    return

  project = project_service.get_project_by_id(project_id)
  message_text = f"Название проекта: {project.name}\n\n";

  user_id = data.get("user_id", None)
  keyboard = KeyboardService.get_current_project_keyboard(user_id)
  await state.set_state(UserState.on_current_project_page)
  await message.answer(
    text=message_text,
    reply_markup=keyboard
  )

@router.callback_query(lambda call: call.data.startswith("project_"))
async def project(call, state: FSMContext):
  """
  Функция, которая обрабатывает переход на страницу проекта
  """
  user_service.update_user_exists(call.from_user.id, get_username_from_message(call))

  project_id = int(call.data.split("_")[1])

  await state.update_data({"project_id": project_id})
  await state.update_data({"user_id": call.from_user.id})
  await state.update_data({"page": 1})
  await state.set_state(UserState.on_current_project_page)

  project = project_service.get_project_by_id(project_id)
  message = f"Название проекта: {project.name}\n\n";

  user_id = call.from_user.id

  keyboard = KeyboardService.get_current_project_keyboard(user_id)
  
  await call.message.answer(
    text=message,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "👥 Участники проекта", UserState.on_current_project_page)
async def project_members(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Участники проекта"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  data = await state.get_data()
  project_id = data.get("project_id", None)
  if project_id is None:
    await state.set_state(UserState.on_start_page)
    await return_to_main_page(message, state)
    return
  
  members_ids = project_service.get_members_ids_by_project_id(project_id)
  members_usernames = user_service.get_usernames_by_ids(members_ids)

  if len(members_usernames) == 0:
    await message.answer(
      text="Участников нет"
    )
  else:
    message_text = "Участники проекта:\n\n"
    for i, username in enumerate(members_usernames):
      message_text += str(i + 1) + ") @" + str(username) + "\n"
  
  keyboard = KeyboardService.get_current_project_keyboard(message.from_user.id)
  await message.answer(
    text=message_text,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "➕ Добавить участника", UserState.on_current_project_page)
async def add_project_member(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Добавить участника"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.waiting_project_member_name)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.Project.add_project_member,
    reply_markup=keyboard
  )

@router.message(UserState.waiting_project_member_name)
async def process_project_member_name(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Добавить участника"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  project_member_name = message.text.strip()
  username, error = get_username(project_member_name)

  if error:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return

  data = await state.get_data()
  project_id = data.get("project_id", None)
  user_id = user_service.get_user_id_by_username(username)
  
  if not user_id:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Error.user_not_found,
      reply_markup=keyboard
    )
    return
  
  project_service.add_project_member(user_id, project_id)

  await state.set_state(UserState.on_current_project_page)
  await show_projects(message, state)

@router.message(lambda message: message.text == "📝 Задачи проекта", UserState.on_current_project_page)
async def project_tasks(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Задачи проекта"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.on_project_tasks_page)
  
  data = await state.get_data()
  project_id = data.get("project_id", None)
  if project_id is None:
    await state.set_state(UserState.on_start_page)
    await return_to_main_page(message, state)
    return

  tasks = task_service.get_tasks_by_project_id(project_id)
  
  if len(tasks) == 0:
    keyboard = KeyboardService.get_project_tasks_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Errors.no_tasks,
      reply_markup=keyboard
    )
    return
  
  message_text = "Ваши задачи:\n\n"

  for i, task in enumerate(tasks):
    if task.responsible_id != 0 and task.responsible_id is not None:
      username = user_service.get_user(task.responsible_id).username
      username = "@" + username
    else:
      username = "нет ответственного"

    message_text += f"{i + 1}. {task.title}\n"
    if task.start_time:
      message_text += f"   🕒 Начало: {task.start_time.strftime('%H:%M')}\n"
    if task.day_date:
      message_text += f"   📅 Дата: {task.day_date.strftime('%d.%m.%Y')}\n"
    message_text += f"   ⏱ Длительность: {task.duration} минут\n"
    if task.deadline:
      message_text += f"   📅 Дедлайн: {task.deadline.strftime('%d.%m.%Y')}\n"
    message_text += f"   👤 Ответственный: {username}\n"
    message_text += f"   ✅ Статус: {'Выполнено' if task.completed else 'Не выполнено'}\n\n"

  keyboard = KeyboardService.get_project_tasks_keyboard(message.from_user.id)
  message = await message.answer(
    text=message_text,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "➖ Удалить участника", UserState.on_current_project_page)
async def delete_project_member(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Удалить участника"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.waiting_member_name_for_delete)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.Project.add_project_member,
    reply_markup=keyboard
  )

@router.message(UserState.waiting_member_name_for_delete)
async def process_member_name_for_delete(message, state: FSMContext):
  """
  Функция, которая обрабатывает ввод имени участника для удаления
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  project_member_name = message.text.strip()
  username, error = get_username(project_member_name)

  if error:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return
  
  data = await state.get_data()
  project_id = data.get("project_id", None)
  user_id = user_service.get_user_id_by_username(username)

  if project_service.member_exists(user_id, project_id):
    project_service.delete_project_member(user_id, project_id)
  else:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Error.user_not_in_project,
      reply_markup=keyboard
    )
    return
  await state.set_state(UserState.on_current_project_page)
  await show_projects(message, state)

@router.message(lambda message: message.text == "⬅️ Вернуться назад", UserState.on_current_project_page)
async def return_to_project_page(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Вернуться назад"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await show_projects(message, state)

@router.message(lambda message: message.text == "🏠 На главную страницу", UserState.on_current_project_page)
async def return_to_project_page(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Вернуться назад"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.on_start_page)
  await return_to_main_page(message, state)

async def show_project_tasks(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Показать задачи"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  data = await state.get_data()
  project_id = data.get("project_id", None)
  if project_id is None:
    await state.set_state(UserState.on_start_page)
    await return_to_main_page(message, state)
    return

  tasks = task_service.get_tasks_by_project_id(project_id)
  
  if len(tasks) == 0:
    keyboard = KeyboardService.get_project_tasks_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Errors.no_tasks,
      reply_markup=keyboard
    )

  page_index = data.get("page", 1)
  message_text = "Ваши задачи, страница " + str(page_index) + ":\n\n"

  buttons = []

  if len(tasks) < page_index * TASKS_PAGE_SIZE:
    for i in range(len(tasks) - (TASKS_PAGE_SIZE * (page_index - 1))):
      button = InlineKeyboardButton(
        text=tasks[i + TASKS_PAGE_SIZE * (page_index - 1)].title,
        callback_data="edit_current_project_task_" + str(tasks[TASKS_PAGE_SIZE * (page_index - 1) + i].task_id)
      )
      buttons.append([button])
  else:
    current_page_tasks = tasks[(page_index - 1) * TASKS_PAGE_SIZE: (page_index) * TASKS_PAGE_SIZE]
    for i in range(TASKS_PAGE_SIZE):
      button = InlineKeyboardButton(
        text=current_page_tasks[i].title,
        callback_data="edit_current_project_task_" + str(current_page_tasks[i].task_id)
      )
      buttons.append([button])

  if page_index > 1 and len(tasks) > TASKS_PAGE_SIZE * page_index:
    button = InlineKeyboardButton(
      text="⬅️",
      callback_data="edit_project_tasks_page_" + str(page_index - 1)
    )
    buttons.append([button])

    button = InlineKeyboardButton(
      text="➡️",
      callback_data="edit_project_tasks_page_" + str(page_index + 1)
    )
    buttons.append([button])
  else:
    if page_index > 1:
      button = InlineKeyboardButton(
        text="⬅️",
        callback_data="edit_project_tasks_page_" + str(page_index - 1)
      )
      buttons.append([button])

    if page_index < len(tasks) // TASKS_PAGE_SIZE:
      button = InlineKeyboardButton(
        text="➡️",
        callback_data="edit_project_tasks_page_" + str(page_index + 1)
      )
      buttons.append([button])

  keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
  await message.answer(
    text=message_text,
    reply_markup=keyboard
  )

@router.callback_query(lambda query: query.data.startswith("edit_current_project_task_"), UserState.editing_project_task)
async def edit_current_project_task(query, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Редактировать задачу"
  """
  user_service.update_user_exists(query.from_user.id, get_username_from_message(query))

  task_id = int(query.data.split("_")[4])

  await state.update_data({"task_id": task_id})
  await state.set_state(UserState.edit_task)
  keyboard = KeyboardService.get_edit_project_task_keyboard(query.from_user.id)

  await query.message.answer(
    text=Messages.AddTask.edit_task_question,
    reply_markup=keyboard
  )

@router.callback_query(lambda query: query.data.startswith("edit_current_project_task_"), UserState.mark_as_done_project_task)
async def mark_as_done_current_project_task(query, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Выполнить задачу"
  """
  user_service.update_user_exists(query.from_user.id, get_username_from_message(query))

  task_id = int(query.data.split("_")[4])

  task = task_service.get_task_by_id(task_id)

  if not task:
    keyboard = KeyboardService.get_return_main_page_or_back_keyboard(query.from_user.id)
    await query.message.answer(
      text=Messages.Error.task_not_found,
      reply_markup=keyboard
    )
    return
  
  if task.completed:
    keyboard = KeyboardService.get_return_main_page_or_back_keyboard(query.from_user.id)
    await query.message.answer(
      text="Задача уже выполнена!",
      reply_markup=keyboard
    )
    return

  task.completed = True
  task_service.update_task(task_id, task)

  await state.set_state(UserState.on_project_tasks_page)
  await project_tasks(query.message, state)

@router.message(UserState.waiting_edit_responsible_person)
async def edit_task_responsible_person_process(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "Редактировать ответственного"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  username, error = get_username(message.text.strip())

  if error:
    keyboard = KeyboardService.get_return_main_page_or_back_keyboard(message.from_user.id)
    await message.answer(
      text=error,
      reply_markup=keyboard
    )
    return
  
  user_id = user_service.get_user_id_by_username(username)

  if not user_id:
    keyboard = KeyboardService.get_return_main_page_or_back_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Error.user_not_found,
      reply_markup=keyboard
    )
    return

  data = await state.get_data()
  project_id = data.get("project_id", None)

  if not project_service.member_exists(user_id, project_id):
    keyboard = KeyboardService.get_return_main_page_or_back_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Error.user_not_in_project,
      reply_markup=keyboard
    )
    return
  
  task_id = data.get("task_id", None)
  task_service.edit_task_responsible_person(task_id, user_id)

  keyboard = KeyboardService.get_project_tasks_keyboard(message.from_user.id)

  await project_tasks(message, state)

@router.message(lambda message: message.text == "✅ Отметить выполненной", UserState.on_project_tasks_page)
async def mark_as_done_task_project(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "✅ Отметить выполненной"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.mark_as_done_project_task)
  
  await show_project_tasks(message, state)
  
@router.message(lambda message: message.text == "✏️ Редактировать задачу", UserState.on_project_tasks_page)
async def edit_project_task(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "✏️ Редактировать задачу"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.editing_project_task)
  
  await show_project_tasks(message, state)

@router.message(lambda message: message.text == "➕ Добавить задачу", UserState.on_project_tasks_page)
async def add_task(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "➕ Добавить задачу"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.process_responsible_person)
  keyboard = KeyboardService.get_yes_or_no_keyboard(message.from_user.id)
  
  await message.answer(
    text=Messages.Project.question_has_responsible_person,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Да", UserState.process_responsible_person)
async def wait_for_responsible_person(message, state: FSMContext):
  """
  Функция, которая обрабатывает ожидания имени ответственного
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.waiting_for_responsible_person)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.Project.add_project_member,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "🔙 Вернуться назад", UserState.waiting_for_responsible_person)
async def return_to_project_page(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "🔙 Вернуться назад"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.on_project_tasks_page)
  await state.update_data("page", 1)
  await show_project_tasks(message, state)

@router.message(lambda message: message.text == "🏠 На главную страницу", UserState.waiting_for_responsible_person)
async def return_to_main_page_project(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "🏠 На главную страницу"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.on_start_page)
  await return_to_main_page(message, state)

@router.message(UserState.waiting_for_responsible_person)
async def process_responsible_person(message, state: FSMContext):
  """
  Функция, которая обрабатывает ввод имени ответственного
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.process_person_name)
  
  username, error = get_username(message.text)
  if error:
    await message.answer(
      text=error
    )
    return

  user_id = user_service.get_user_id_by_username(username)
  if not user_id:
    keyboard = KeyboardService.get_return_main_page_or_back_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Error.user_not_found,
      reply_markup=keyboard
    )
    return

  data = await state.get_data()
  project_id = data.get("project_id", None)

  if not project_id:
    keyboard = KeyboardService.get_return_main_page_or_back_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Error.project_not_found,
      reply_markup=keyboard
    )
    return
  
  if not project_service.member_exists(user_id, project_id):
    keyboard = KeyboardService.get_return_main_page_or_back_keyboard(message.from_user.id)
    await message.answer(
      text=Messages.Error.user_not_in_project,
      reply_markup=keyboard
    )
    return
  
  await state.update_data({"responsible_id": user_id})
  await state.update_data({"week_first_day_date": get_first_day_of_week(datetime.date.today())})
  
  await state.set_state(UserState.waiting_for_project_task_name)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Введите название задачи:",
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Нет", UserState.process_responsible_person)
async def process_add_task_project(message, state: FSMContext):
  """
  Функция, которая обрабатывает действия, если нет ответственного
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.update_data({"week_first_day_date": get_first_day_of_week(datetime.date.today())})

  await state.set_state(UserState.waiting_for_project_task_name)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Введите название задачи:",
    reply_markup=keyboard
  )
  
@router.message(lambda message: message.text == "🔙 Вернуться назад", UserState.on_project_tasks_page)
async def return_to_project_page(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "🔙 Вернуться назад"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.update_data({"page": 1})
  await state.update_data({"user_id": message.from_user.id})
  await state.set_state(UserState.on_current_project_page)
  await show_current_project_page(message, state)

@router.message(lambda message: message.text == "🏠 На главную страницу", UserState.on_project_tasks_page)
async def return_to_main_page_project(message, state: FSMContext):
  """
  Функция, которая обрабатывает нажатие на кнопку "🏠 На главную страницу"
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))

  await state.set_state(UserState.on_start_page)
  await return_to_main_page(message, state)

@router.message(UserState.waiting_for_project_task_name)
async def process_task_name_project(message, state: FSMContext):
  """
  Функция, которая обрабатывает название задачи проекта
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
  await state.set_state(UserState.waiting_for_task_start_date)

  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Введите дату начала задачи в формате ДД.ММ.ГГГГ:",
    reply_markup=keyboard
  )

@router.message(UserState.waiting_for_task_start_date)
async def process_task_start_date(message, state: FSMContext):
  """
  Функция, которая обрабатывает дату начала задачи проекта
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  try:
    start_date = datetime.datetime.strptime(message.text.strip(), "%d.%m.%Y")
  except ValueError:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text="Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ",
      reply_markup=keyboard
    )
    return

  await state.update_data({"day_date": start_date})
  await state.set_state(UserState.process_task_start_time)

  keyboard = KeyboardService.get_task_start_time_exists_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.task_start_time_exists_question,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Да, будет время начала", UserState.process_task_start_time)
async def process_task_start_time_yes_project(message, state: FSMContext):
  """
  Функция, которая обрабатывает наличие времени начала задачи проекта
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.set_state(UserState.waiting_for_task_start_time)
  keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
  await message.answer(
    text="Введите время начала в формате ЧЧ:ММ",
    reply_markup=keyboard
  )

@router.message(UserState.waiting_for_task_start_time)
async def process_task_start_time_project(message, state: FSMContext):
  """
  Функция, которая обрабатывает время начала задачи проекта
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
    start_date = data.get("start_date")
    start_datetime = start_date.replace(hour=hours, minute=minutes)
    
    await state.update_data({"start_time": start_datetime})
    
  except ValueError:
    keyboard = KeyboardService.get_return_main_page_keyboard(message.from_user.id)
    await message.answer(
      text="Неверный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ",
      reply_markup=keyboard
    )
    return

  await state.set_state(UserState.process_task_duration)
  keyboard = KeyboardService.get_task_duration_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.task_duration_question,
    reply_markup=keyboard
  )

@router.message(lambda message: message.text == "Нет, не будет времени начала", UserState.process_task_start_time)
async def process_task_start_time_no_project(message, state: FSMContext):
  """
  Функция, которая обрабатывает отсутствие времени начала задачи проекта
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  data = await state.get_data()
  start_date = data.get("start_date")
  await state.update_data({"start_time": start_date})
  
  await state.set_state(UserState.process_task_duration)
  keyboard = KeyboardService.get_task_duration_keyboard(message.from_user.id)
  await message.answer(
    text=Messages.AddTask.task_duration_question,
    reply_markup=keyboard
  )