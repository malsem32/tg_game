from bot.create_bot import dp
from bot.handlers.start import start_router
def include_routers(dp):
    dp.include_routers(start_router)
