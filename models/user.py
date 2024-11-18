from pydantic import BaseModel

class UserSettings(BaseModel):
  keyboard_type: str

class User(BaseModel):
  telegram_id: int
  username: str
  current_streak: int
  max_streak: int
  settings: UserSettings
