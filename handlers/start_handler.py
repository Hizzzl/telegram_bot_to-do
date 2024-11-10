from aiogram import Router
from aiogram.filters import Command
from states.states import UserState
from aiogram.fsm.context import FSMContext
import datetime
from services import user_service, task_service
from utils import return_to_main_page, get_username_from_message

router = Router()

@router.message(Command("start"))
async def main_page(message, state: FSMContext):
  user_service.update_user_exists(message.from_user.id, get_username_from_message(message))
  await return_to_main_page(message, state)