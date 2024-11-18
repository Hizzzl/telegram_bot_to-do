from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional

class Task(BaseModel):
  task_id: int
  telegram_id: int
  project_id: Optional[int] = None
  responsible_id: Optional[int] = None
  title: str
  completed: bool
  deadline: Optional[datetime] = None
  week_first_day_date: datetime
  day_date: Optional[datetime] = None
  start_time: Optional[datetime] = None
  duration: int