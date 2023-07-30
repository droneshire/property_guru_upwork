import asyncio
import functools
import typing as T

import telegram

from util import log


def force_sync(function_handle: T.Callable) -> T.Callable:
    @functools.wraps(function_handle)
    def wrapper(*args: T.Any, **kwargs: T.Any) -> T.Any:
        response = function_handle(*args, **kwargs)
        if asyncio.iscoroutine(response):
            return asyncio.get_event_loop().run_until_complete(response)
        return response

    return wrapper


class TelegramUtil:
    def __init__(self, token: str, dry_run: bool = False) -> None:
        self.bot = telegram.Bot(token=token)
        self.dry_run = dry_run

    def check_token(self) -> bool:
        if self.dry_run:
            log.print_normal("TelegramUtil: check_token (dry run)")
            return True

        return self._check_token()  # type: ignore[no-any-return]

    @force_sync
    async def _check_token(self) -> bool:
        async with self.bot:
            try:
                its_me = await self.bot.get_me()
                log.print_ok_arrow(f"Telegram bot is running as {its_me.username}")
                return True
            except:  # pylint: disable=bare-except
                log.print_fail("Telegram bot token is invalid!")
                return False
        return False

    def get_channel_chats(self) -> T.List[telegram.Chat]:
        if self.dry_run:
            log.print_normal("TelegramUtil: get_channel_chats (dry run)")
            return []

        return self._get_channel_chats()  # type: ignore[no-any-return]

    @force_sync
    async def _get_channel_chats(self) -> T.List[telegram.Chat]:
        chats: T.List[telegram.Chat] = []
        async with self.bot:
            updates = await self.bot.get_updates()
        for update in updates:
            if update.channel_post:
                chats.append(update.channel_post.chat)
        return chats

    def get_chat_id(self, title: str) -> T.Optional[int]:
        if self.dry_run:
            log.print_normal("TelegramUtil: get_chat_id (dry run)")
            return None

        chats: T.List[telegram.Chat] = self.get_channel_chats()
        for chat in chats:
            if chat.title == title:
                return chat.id
        return None

    def send_message(self, chat_id: int, message: str) -> None:
        if self.dry_run:
            log.print_normal("TelegramUtil: send_message (dry run)")
            return
        self._send_message(chat_id, message)  # type: ignore[no-any-return]

    @force_sync
    async def _send_message(self, chat_id: str, message: str) -> None:
        async with self.bot:
            await self.bot.send_message(chat_id=chat_id, text=message)
