import asyncio
import platform
import logging
from telegram.ext import Application
from config import BOT_TOKEN, ADMIN_IDS
from handlers import setup_user_handlers, setup_admin_handlers

# Настройка логгирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SurveyBot:
    def __init__(self):
        self.application = None

    async def start(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Используем правильные имена функций
        setup_user_handlers(self.application)
        setup_admin_handlers(self.application)
        
        await self._run_polling()

    async def _run_polling(self):
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        try:
            while True:
                await asyncio.sleep(3600)
        except asyncio.CancelledError:
            logger.info("Получен сигнал остановки...")
        finally:
            await self._shutdown()

    async def _shutdown(self):
        logger.info("Завершение работы бота...")
        if self.application:
            if self.application.updater.running:
                await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()

def main():
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    bot = SurveyBot()
    loop = asyncio.new_event_loop()
    
    try:
        loop.run_until_complete(bot.start())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    finally:
        if not loop.is_closed():
            loop.close()

if __name__ == "__main__":
    main()