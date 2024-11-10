from models import ReplyKeyboard as Keyboard, Messages
from states.states import UserState
from aiogram.fsm.context import FSMContext
from services.services_init import user_service
from .common import get_username_from_message

async def return_to_main_page(message, state: FSMContext) -> None:
  """
  Функция, которая возвращает на главную страницу
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await state.clear()
  await message.answer(
        text=Messages.main_page,
        reply_markup=Keyboard.main_page_keyboard
    )
  await state.set_state(UserState.on_start_page)

async def add_daily_task(message, state: FSMContext) -> None:
  """
  Функция, которая начинает цикл добавление задач
  """
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await message.answer(
    text=Messages.AddTask.get_task_name,
    reply_markup=Keyboard.return_main_page_keyboard
  )
  
  await state.set_state(UserState.waiting_for_task_name)