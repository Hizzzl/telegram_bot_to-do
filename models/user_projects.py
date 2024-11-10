from pydantic import BaseModel

class UserProjects(BaseModel):
  user_id: int
  project_id: int