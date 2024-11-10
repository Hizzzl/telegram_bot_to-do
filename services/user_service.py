from repositories.user_repository import UserRepository
from models import User, UserSettings, Task
from typing import List

class UserService:
  def __init__(self, user_repository: UserRepository):
    self.user_repository = user_repository

  def get_user_settings(self, user_id: int) -> UserSettings:
    """
    Возвращает настройки пользователя
    """
    user = self.user_repository.get_user(user_id)
    if not user:
      self.create_user(user_id)
      user = self.user_repository.get_user(user_id)
      return user.settings
    return user.settings

  def update_user_settings(self, user_id: int, settings: dict) -> None:
    """
    Обновляет настройки пользователя
    """
    self.user_repository.update_user_settings(user_id, settings)

  def create_user(self, user_id: int) -> None:
    """
    Создает пользователя в базе данных
    """
    user = User(
      telegram_id=user_id,
      current_streak=0,
      max_streak=0,
      settings=UserSettings(
        keyboard_type="reply"
      )
    )
    self.user_repository.create_user(user)
  
  def check_user_exists(self, user_id: int) -> bool:
    """
    Проверяет, существует ли пользователь в базе данных
    """
    return self.user_repository.check_user_exists(user_id)
  
  def update_user_exists(self, user_id: int, user_name: str) -> None:
    """
    Обновляет данные пользователя в базе данных
    """
    if self.user_repository.check_user_exists(user_id):
      user = self.user_repository.get_user(user_id)
      if user.username != user_name:
        user.username = user_name
        self.user_repository.update_user(user_id, user)
      return
    user = User(
      telegram_id=user_id,
      username=user_name,
      current_streak=0,
      max_streak=0,
      settings=UserSettings(
        keyboard_type="reply"
      )
    )
    self.user_repository.create_user(user)

  def get_user(self, user_id: int) -> User:
    """
    Возвращает пользователя по его id
    """
    return self.user_repository.get_user(user_id)
  
  def get_usernames_by_ids(self, user_ids: list) -> List[str]:
    """
    Возвращает список username пользователей по их id
    """
    usernames = []
    for user_id in user_ids:
      user = self.user_repository.get_user(user_id)
      if user:
        usernames.append(user.username)
    return usernames
  
  def get_user_id_by_username(self, username: str) -> int:
    """
    Возвращает id пользователя по его username
    """
    user = self.user_repository.get_user_by_username(username)
    if user:
      return user.telegram_id
    return None