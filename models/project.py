from pydantic import BaseModel
from typing import Optional

class Project(BaseModel):
  project_id: Optional[int] = None
  name: str