from aiogram import Router


def setup_routers() -> Router:
    from .handlers.users import main_dialog,registration,slider,specialties,contacts,profile,quiz
    router = Router()
    router.include_routers(main_dialog.router,registration.router,slider.router,specialties.router,contacts.router,profile.router,quiz.router)

    return router
