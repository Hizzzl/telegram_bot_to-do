from aiogram import Router

def get_handlers_router() -> Router:
  from .daily_page_handers import router as daily_page_router
  from .task_handlers import router as task_handler_router
  from .start_handler import router as start_handler_router
  from .weekly_page_handler import router as weekly_page_router
  from .projects_handler import router as projects_handler_router

  router = Router()
  router.include_router(daily_page_router)
  router.include_router(task_handler_router)
  router.include_router(start_handler_router)
  router.include_router(weekly_page_router)
  router.include_router(projects_handler_router)
  
  return router