import asyncio
import logging
import sys

from django.core.management.base import BaseCommand

from tgbot.bot.loader import bot, dp


class Command(BaseCommand):
    help = 'Run bot in polling'

    async def run_telegram_bot(self) -> None:
        await dp.start_polling(bot, skip_updates=True)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Bot started"))
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(self.run_telegram_bot())
