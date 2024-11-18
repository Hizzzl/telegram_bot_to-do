from sqlalchemy import Column, Integer, String, Date, Boolean, BigInteger, Time, DateTime
from database_tables.base_database import Base

class Task_table(Base):
  __tablename__ = 'tasks'

  task_id = Column(Integer, primary_key=True, index=True)
  project_id = Column(Integer, nullable=True, default=0)
  responsible_id = Column(BigInteger, nullable=True, default=0)
  telegram_id = Column(BigInteger, nullable=False, default=0)
  title = Column(String, nullable=False, default='')
  completed = Column(Boolean, nullable=False, default=False)
  deadline = Column(Date, nullable=True, default=None)
  week_first_day_date = Column(Date, nullable=False)
  day_date = Column(Date, nullable=True, default=None)
  duration = Column(Integer, nullable=False, default=0)
  start_time = Column(DateTime, nullable=True, default=None)