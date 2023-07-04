import asyncio

import telegram


class TelegramUtil:

    def __init__(self, token: str) -> None:
        self.bot = telegram.Bot(token=token)

    async def check_token(self) -> bool:
        async with self.bot:
            try:
                await self.bot.get_me()
                return True
            except telegram.error.Unauthorized:
                return False

    async def send_message(self, chat_id: str, message: str) -> None:
        async with self.bot:
            await self.bot.send_message(chat_id=chat_id, text=message)
