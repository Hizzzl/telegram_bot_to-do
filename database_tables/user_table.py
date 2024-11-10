from sqlalchemy import Column, Integer, String, DateTime, JSON, BigInteger
from database_tables.base_database import Base

import datetime

class User_table(Base):
  __tablename__ = 'users'  # Имя таблицы

  telegram_id = Column(BigInteger, primary_key=True, index=True)  # Уникальный идентификатор
  username = Column(String, nullable=False, default='')  # Имя пользователя
  current_streak = Column(Integer, nullable=False, default=0)
  max_streak = Column(Integer, nullable=False, default=0)
  settings = Column(JSON, nullable=False, default={})