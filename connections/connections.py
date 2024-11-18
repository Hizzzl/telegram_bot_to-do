from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker

from aiogram import Bot

class ConnectionManager:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
        cls._instance = super(ConnectionManager, cls).__new__(cls)
        cls._instance.bot = None
        cls._instance.db_connection = None
    return cls._instance

  def init_bot(self, token: str):
    """
    Инициализация бота
    """
    if self.bot is None:
        self.bot = Bot(token)

  def init_db(self, path_to_db: str):
    """
    Инициализация базы данных
    """
    self.engine = create_engine("sqlite:///{}".format(path_to_db))
    Session = sessionmaker(bind=self.engine)
    connection = Session()
    
    if self.db_connection is None:
        self.db_connection = connection

  def get_bot(self):
    """
    Получение бота
    """        
    return self.bot

  def get_db_connection(self):
    """
    Подключение к базе данных
    """
    return self.db_connection

  def get_engine(self):
    """
    Получить движок базы данных
    """
    return self.engine
    
connection_manager = ConnectionManager()