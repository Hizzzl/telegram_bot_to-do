from repositories.database_interface import DatabaseInterface
from models import User, UserSettings

class UserRepository:
  def __init__(self, db: DatabaseInterface):  # Внедряем зависимость от интерфейса базы данных
      self.db = db

  def get_user(self, user_id: int) -> User:
    """
    Возвращает пользователя по его id
    """
    result = self.db.get_user_by_id(user_id)
    if result:
      my_user = User(
        telegram_id=result.telegram_id,
        username=result.username,
        current_streak=result.current_streak,
        max_streak=result.max_streak,
        settings=UserSettings(
          keyboard_type=result.settings["keyboard_type"]
        )
      )
      return my_user
    return None

  def get_user_by_username(self, username: str) -> User:
    """
    Возвращает пользователя по его username
    """
    result = self.db.get_user_by_username(username)
    if result:
      my_user = User(
        telegram_id=result.telegram_id,
        username=result.username,
        current_streak=result.current_streak,
        max_streak=result.max_streak,
        settings=UserSettings(
          keyboard_type=result.settings["keyboard_type"]
        )
      )
      return my_user
    return None

  def create_user(self, user: User) -> None:
    """
    Создает пользователя в базе данных
    """
    self.db.create_user(user)

  def update_user(self, user_id: int, user: User) -> None:  
    """
    Обновляет данные пользователя в базе данных
    """
    self.db.update_user(user_id, user)

  def delete_user(self, user_id: int) -> None:
    """
    Удаляет пользователя из базы данных
    """
    self.db.delete_user(user_id)
  
  def check_user_exists(self, user_id: int) -> bool:
    """
    Проверяет наличие пользователя в базе данных
    """
    return self.db.check_user_exists(user_id)