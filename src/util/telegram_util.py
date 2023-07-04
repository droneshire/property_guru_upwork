import asyncio

import telegram

from util import log


class TelegramUtil:
    def __init__(self, token: str) -> None:
        self.bot = telegram.Bot(token=token)

    async def check_token(self) -> bool:
        async with self.bot:
            try:
                its_me = await self.bot.get_me()
                log.print_ok_blue(f"Telegram bot is running as {its_me.username}")
                return True
            except telegram.error.Unauthorized:
                log.print_fail("Telegram bot token is invalid!")
                return False

    async def send_message(self, chat_id: str, message: str) -> None:
        async with self.bot:
            await self.bot.send_message(chat_id=chat_id, text=message)
