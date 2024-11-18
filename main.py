from dotenv import load_dotenv
from aiogram import Dispatcher
from aiogram_sqlite_storage.sqlitestore import SQLStorage
import asyncio
import os
from connections import connection_manager
# from connections.initialize_sql_table import create_db_and_tables
from handlers import get_handlers_router


load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

connection_manager.init_bot(API_TOKEN)

FSM_STORAGE_PATH = os.getenv("FSM_STORAGE_PATH")
fsm_storage = SQLStorage(FSM_STORAGE_PATH, serializing_method = 'pickle')

DB_PATH = os.getenv("DB_PATH")
connection_manager.init_db(DB_PATH)

# conn_db = connection_manager.get_db_connection()

# SQLAlchemyRepository = SQLAlchemyRepository(conn_db, connection_manager.get_engine())

# userRepo = UserRepository(SQLAlchemyRepository)
# UserService = UserService(userRepo)

bot = connection_manager.get_bot()
dp = Dispatcher(storage=fsm_storage)
dp.include_router(get_handlers_router())

asyncio.run(dp.start_polling(bot))