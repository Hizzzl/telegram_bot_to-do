from sqlalchemy import Column, Integer, String, Date, Boolean, BigInteger
from database_tables.base_database import Base

class Project_table(Base):
  __tablename__ = 'projects'

  project_id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False, default='')