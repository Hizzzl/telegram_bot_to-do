from aiogram.types import (
  ReplyKeyboardMarkup,
  KeyboardButton,
  InlineKeyboardMarkup,
  InlineKeyboardButton,

)

class ReplyKeyboard:
  main_page_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="Ежедневные задачи 📅")],
      [KeyboardButton(text="Недельные задачи 📅")],
      [KeyboardButton(text="Проекты 📝")]
    ],
    resize_keyboard=True
  )

  daily_tasks_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="➕ Добавить задачу")],
      [KeyboardButton(text="✏️ Редактировать задачу")],
      [KeyboardButton(text="✅ Отметить выполненной")],
      [KeyboardButton(text="🔄 Перенести на завтра")],
      [KeyboardButton(text="📅 Недельные задачи")],
      [KeyboardButton(text="➡️ Завтрашние задачи")],
      [KeyboardButton(text="🔙 Главное меню")]
    ],
    resize_keyboard=True
  )

  return_main_page_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="🔙 Главное меню")]
    ],
    resize_keyboard=True
  )

  task_duration_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="30 минут"), KeyboardButton(text="1 час")],
      [KeyboardButton(text="2 часа"), KeyboardButton(text="4 часа")],
      [KeyboardButton(text="Ввести свое время")],  # Кнопка для ввода своего времени
      [KeyboardButton(text="🔙 Изменить название задачи")],
      [KeyboardButton(text="🔙 Главное меню")]
    ],
    resize_keyboard=True
  )

  task_deadline_exists_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="Да, дедлайн будет")],
      [KeyboardButton(text="Нет, дедлайна не будет")]
    ],
    resize_keyboard=True
  )

  task_start_time_exists_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="Да, будет время начала"), KeyboardButton(text="Нет, не будет времени начала")],
      [KeyboardButton(text="🔙 Главное меню")]
    ],
    resize_keyboard=True
  )

  edit_task_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="Название задачи")],
      [KeyboardButton(text="Длительность задачи")],
      [KeyboardButton(text="Дедлайн задачи")],
      [KeyboardButton(text="Изменить статус задачи")],
      [KeyboardButton(text="Время начала задачи")],
      [KeyboardButton(text="🔙 Главное меню")]
    ],
    resize_keyboard=True
  )

  weekly_tasks_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="✏️ Редактировать задачу")],
      [KeyboardButton(text="✅ Отметить выполненной")],
      [KeyboardButton(text="⏩ Автораспределение")],
      [KeyboardButton(text="📝 Добавить задачу")],
      [KeyboardButton(text="🔄 Перенести на следующую неделю")],
      [KeyboardButton(text="⬅️ Ежедневные задачи")],
      [KeyboardButton(text="🔙 Главное меню")]
    ],
    resize_keyboard=True
  )

  edit_weekly_task_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="Название задачи")],
      [KeyboardButton(text="Длительность задачи")],
      [KeyboardButton(text="Дедлайн задачи")],
      [KeyboardButton(text="Изменить статус задачи")],
      [KeyboardButton(text="Изменить назначенный день задачи")],
      [KeyboardButton(text="Время начала задачи")],
      [KeyboardButton(text="🔙 Главное меню")]
    ],
    resize_keyboard=True
  )

  edit_task_date_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="Понедельник")],
      [KeyboardButton(text="Вторник")],
      [KeyboardButton(text="Среда")],
      [KeyboardButton(text="Четверг")],
      [KeyboardButton(text="Пятница")],
      [KeyboardButton(text="Суббота")],
      [KeyboardButton(text="Воскресенье")],
    ]
  )

  yes_or_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="Да")],
      [KeyboardButton(text="Нет")]
    ],
    resize_keyboard=True
  )

  project_page_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="🏠 На главную")],
      [KeyboardButton(text="➕ Добавить проект")],
      [KeyboardButton(text="📂 Открыть проект")]
    ],
    resize_keyboard=True
  )

  current_project_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="👥 Участники проекта")],
      [KeyboardButton(text="📝 Задачи проекта")],    
      [KeyboardButton(text="➕ Добавить участника")],
      [KeyboardButton(text="➖ Удалить участника")],
      [KeyboardButton(text="⬅️ Вернуться назад")],
      [KeyboardButton(text="🏠 На главную страницу")]
    ],
    resize_keyboard=True
  )

  project_tasks_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="✅ Отметить выполненной")],
      [KeyboardButton(text="✏️ Редактировать задачу")],
      [KeyboardButton(text="➕ Добавить задачу")],
      [KeyboardButton(text="🔙 Вернуться назад")],
      [KeyboardButton(text="🏠 На главную страницу")]
    ]
  )

  return_main_page_or_back_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="🔙 Вернуться назад")],
      [KeyboardButton(text="🏠 На главную страницу")]
    ]
  )

  edit_project_task_keyboard = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text="Название задачи")],
      [KeyboardButton(text="Длительность задачи")],
      [KeyboardButton(text="Дедлайн задачи")],
      [KeyboardButton(text="Изменить статус задачи")],
      [KeyboardButton(text="Изменить ответственного")],
      [KeyboardButton(text="Прикрепленный день")],
      [KeyboardButton(text="Время начала задачи")],
      [KeyboardButton(text="🔙 Вернуться назад")],
      [KeyboardButton(text="🏠 На главную страницу")]
    ],
    resize_keyboard=True
  )

class InlineKeyboard:
  main_page_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="Ежедневные задачи 📅", callback_data="daily_tasks")],
      [InlineKeyboardButton(text="Недельные задачи 📅", callback_data="weekly_tasks")],
      [InlineKeyboardButton(text="Проекты 📝", callback_data="projects")],
      [InlineKeyboardButton(text="Стрик 🔥", callback_data="strike")],
      [InlineKeyboardButton(text="Статистика 📊", callback_data="stats")],
      [InlineKeyboardButton(text="Настройки ⚙️", callback_data="settings")]
    ]
  )

  return_main_page_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_page")]
    ]
  )

  daily_tasks_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="➕ Добавить задачу", callback_data="add_daily_task")],
      [InlineKeyboardButton(text="✏️ Редактировать задачу", callback_data="edit_daily_task")],
      [InlineKeyboardButton(text="✅ Отметить выполненной", callback_data="mark_as_done")],
      [InlineKeyboardButton(text="🔄 Перенести на завтра", callback_data="move_to_tomorrow")],
      [InlineKeyboardButton(text="📅 Недельные задачи", callback_data="weekly_tasks")],
      [InlineKeyboardButton(text="➡️ Завтрашние задачи", callback_data="tomorrow_tasks")],
      [InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_page")]
    ]
  )

  task_duration_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="30 минут", callback_data="30_min")],
      [InlineKeyboardButton(text="1 час", callback_data="1_hour")],
      [InlineKeyboardButton(text="2 часа", callback_data="2_hour")],
      [InlineKeyboardButton(text="4 часа", callback_data="4_hour")],
      [InlineKeyboardButton(text="Ввести свое время", callback_data="custom_time")]
    ]
  )

  task_deadline_exists_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="Да, дедлайн будет", callback_data="deadline_exists")],
      [InlineKeyboardButton(text="Нет, дедлайна не будет", callback_data="deadline_does_not_exist")],
    ]
  )

  task_start_time_exists_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="Да, будет время начала", callback_data="start_time_exists")],
      [InlineKeyboardButton(text="Нет, не будет времени начала", callback_data="start_time_does_not_exist")],
    ]
  )

  edit_task_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="Название задачи", callback_data="edit_title")],
      [InlineKeyboardButton(text="Длительность задачи", callback_data="edit_duration")],
      [InlineKeyboardButton(text="Дедлайн задачи", callback_data="edit_deadline")],
      [InlineKeyboardButton(text="Изменить статус задачи", callback_data="edit_status")],
      [InlineKeyboardButton(text="Время начала задачи", callback_data="edit_start_time")],
      [InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_page")]
    ]
  )

  edit_task_date_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="✏️ Редактировать задачу", callback_data="edit_daily_task")],
      [InlineKeyboardButton(text="✅ Отметить выполненной", callback_data="mark_as_done")],
      [InlineKeyboardButton(text="⏩ Автораспределение", callback_data="mark_as_done")],
      [InlineKeyboardButton(text="📝 Добавить задачу", callback_data="move_to_tomorrow")],
      [InlineKeyboardButton(text="🔄 Перенести на следующую неделю", callback_data="weekly_tasks")],
      [InlineKeyboardButton(text="⬅️ Ежедневные задачи", callback_data="tomorrow_tasks")],
      [InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_page")]
    ]
  )

  edit_weekly_task_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="Название задачи", callback_data="edit_title")],
      [InlineKeyboardButton(text="Длительность задачи", callback_data="edit_duration")],
      [InlineKeyboardButton(text="Дедлайн задачи", callback_data="edit_deadline")],
      [InlineKeyboardButton(text="Изменить статус задачи", callback_data="edit_status")],
      [InlineKeyboardButton(text="Изменить назначенный день задачи", callback_data="edit_day")],
      [InlineKeyboardButton(text="Время начала задачи", callback_data="edit_start_time")],
      [InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_page")]
    ]
  )

  edit_task_date_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="Понедельник", callback_data="monday")],
      [InlineKeyboardButton(text="Вторник", callback_data="tuesday")],
      [InlineKeyboardButton(text="Среда", callback_data="wednesday")],
      [InlineKeyboardButton(text="Четверг", callback_data="thursday")],
      [InlineKeyboardButton(text="Пятница", callback_data="friday")],
      [InlineKeyboardButton(text="Суббота", callback_data="saturday")],
      [InlineKeyboardButton(text="Воскресенье", callback_data="sunday")]
    ]
  )

  yes_or_no_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="Да", callback_data="yes")],
      [InlineKeyboardButton(text="Нет", callback_data="no")]
    ]
  )

  project_page_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="🏠 На главную", callback_data="main_page")],
      [InlineKeyboardButton(text="➕ Добавить проект", callback_data="add_project")],
      [InlineKeyboardButton(text="📂 Открыть проект", callback_data="open_project")]
    ]
  )

  current_project_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="👥 Участники проекта", callback_data="view_project_members")],
      [InlineKeyboardButton(text="📝 Задачи проекта", callback_data="view_project_tasks")],
      [InlineKeyboardButton(text="➕ Добавить участника", callback_data="add_member")],
      [InlineKeyboardButton(text="➖ Удалить участника", callback_data="remove_member")],
      [InlineKeyboardButton(text="⬅️ Вернуться назад", callback_data="go_back")],
      [InlineKeyboardButton(text="🏠 На главную страницу", callback_data="go_home")],
    ]
  )

  project_tasks_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="✅ Отметить выполненной", callback_data="mark_completed")],
      [InlineKeyboardButton(text="✏️ Редактировать задачу", callback_data="edit_task")],
      [InlineKeyboardButton(text="➕ Добавить задачу", callback_data="add_task")],
      [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="go_back")],
      [InlineKeyboardButton(text="🏠 На главную страницу", callback_data="go_home")],
    ]
  )

  return_main_page_or_back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="🔙 Вернуться назад", callback_data="go_back")],
      [InlineKeyboardButton(text="🏠 На главную страницу", callback_data="go_home")],
    ]
  )

  edit_project_task_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
      [InlineKeyboardButton(text="Ответственный за задачу", callback_data="edit_responsible")],
      [InlineKeyboardButton(text="Название задачи", callback_data="edit_title")],
      [InlineKeyboardButton(text="Длительность задачи", callback_data="edit_duration")],
      [InlineKeyboardButton(text="Дедлайн задачи", callback_data="edit_deadline")],
      [InlineKeyboardButton(text="Изменить статус задачи", callback_data="edit_status")],
      [InlineKeyboardButton(text="Изменить назначенный день задачи", callback_data="edit_day")],
      [InlineKeyboardButton(text="Время начала задачи", callback_data="edit_start_time")],
      [InlineKeyboardButton(text="🔙 Главное меню", callback_data="go_home")]
    ]
  )
