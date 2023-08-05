import asyncio
from contextlib import contextmanager
from typing import Callable, Dict, Tuple

from telegrambotclient.api import TelegramBotAPI
from telegrambotclient.base import Message, TelegramBotException, logger
from telegrambotclient.storage import (MemoryStorage, TelegramSession,
                                       TelegramStorage)
from telegrambotclient.utils import (build_force_reply_data,
                                     parse_force_reply_data, pretty_format)


class TelegramBot:
    _force_reply_key_format = "bot:force_reply:{0}"
    __slots__ = ("id", "token", "router", "api", "_storage", "_i18n_source",
                 "last_update_id", "_bot_user")

    def __init__(
        self,
        token: str,
        router,
        storage: TelegramStorage = None,
        i18n_source: Dict = None,
        bot_api: TelegramBotAPI = None,
    ):
        try:
            self.id = int(token.split(":")[0])
        except IndexError as error:
            raise TelegramBotException(
                "wrong token format: {0}".format(token)) from error
        self.token = token
        self.router = router
        if storage:
            assert isinstance(storage, TelegramStorage), True
        else:
            logger.warning(
                "You are using a memory storage which can not be persisted.")
            storage = MemoryStorage()
        self._storage = storage
        self._i18n_source = i18n_source
        if bot_api:
            assert isinstance(bot_api, TelegramBotAPI), True
        else:
            logger.warning(
                "Your bot API object is not a TelegramBotAPI instance. A default bot api is using."
            )
            bot_api = TelegramBotAPI()
        self.api = bot_api
        self.last_update_id = 0
        self._bot_user = None

    @property
    def user(self):
        if self._bot_user is None:
            self._bot_user = self.get_me()
        return self._bot_user

    @property
    def next_call(self):
        return self.router.next_call

    @property
    def stop_call(self):
        return self.router.stop_call

    def join_force_reply(self,
                         user_id: int,
                         callback: Callable,
                         *force_reply_args,
                         expires: int = 1800):
        force_reply_callback_name = "{0}.{1}".format(callback.__module__,
                                                     callback.__name__)
        if not self.router.has_force_reply_callback(force_reply_callback_name):
            raise TelegramBotException(
                "{0} is not a force reply callback".format(
                    force_reply_callback_name))
        field = self._force_reply_key_format.format(user_id)
        with self.session(user_id, expires) as session:
            if force_reply_args:
                session[field] = build_force_reply_data(
                    force_reply_callback_name, *force_reply_args)
            else:
                session[field] = build_force_reply_data(
                    force_reply_callback_name)

    def force_reply_done(self, user_id):
        session = self.get_session(user_id)
        del session[self._force_reply_key_format.format(user_id)]

    def get_force_reply(self, user_id):
        session = self.get_session(user_id)
        force_reply_data = session.get(
            self._force_reply_key_format.format(user_id), None)
        if not force_reply_data:
            return None, None
        return parse_force_reply_data(force_reply_data)

    def get_session(self, user_id: int, expires: int = 1800):
        return TelegramSession(self.id, user_id, self._storage, expires)

    @contextmanager
    def session(self, user_id: int, expires: int = 1800):
        session = self.get_session(user_id, expires)
        try:
            yield session
        finally:
            session.save()

    def push_ui(self, user_id: int, message):
        with self.session(user_id) as session:
            ui_stack = session.get("_ui_", [])
            ui_stack.append(message)
            session["_ui_"] = ui_stack

    def pop_ui(self, user_id: int):
        with self.session(user_id) as session:
            return session.get("_ui_", []).pop()

    def get_text(self, language_code: str, text: str):
        if self._i18n_source:
            lang_source = self._i18n_source.get(language_code, None)
            if lang_source:
                if isinstance(lang_source, dict):
                    return lang_source.get(text, text)
                return lang_source.gettext(text)
        return text

    def reply_message(self, message: Message, **kwargs):
        kwargs["reply_to_message_id"] = message.message_id
        return self.send_message(chat_id=message.chat.id, **kwargs)

    def get_file_url(self, file_path: str):
        return "{0}{1}".format(
            self.api.host, self.api.download_url.format(self.token, file_path))

    def get_deep_link(self,
                      payload: str,
                      host: str = "https://t.me",
                      startgroup: bool = False):
        return "{0}/{1}?{2}={3}".format(
            host, self.user.username, "startgroup" if startgroup else "start",
            payload)

    async def dispatch(self, update):
        logger.debug(pretty_format(update))
        await self.router.route(self, update)

    def run_polling(self,
                    limit: int = None,
                    timeout: int = 10,
                    allowed_updates: Tuple[str] = None,
                    **kwargs):
        if timeout == 0:
            logger.warning(
                "You are using 0 as timeout in seconds for long polling which should be used for testing purposes only."
            )
        while True:
            updates = self.api.get_updates(
                self.token,
                offset=self.last_update_id + 1,
                limit=limit,
                timeout=timeout,
                allowed_updates=allowed_updates,
                **kwargs,
            )
            if updates:
                self.last_update_id = updates[-1].update_id
                for update in updates:
                    asyncio.run(self.dispatch(update))

    def __getattr__(self, api_name):
        def api_method(**kwargs):
            return getattr(self.api, api_name)(self.token, **kwargs)

        return api_method
