from database_tables.base_database import Base
from sqlalchemy import Column, Integer, BigInteger

class User_projects_table(Base):
  __tablename__ = 'user_projects'
  user_id = Column(BigInteger, primary_key=True, index=True)
  project_id = Column(Integer, primary_key=True, index=True)