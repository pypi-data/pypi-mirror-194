class TAPIError(Exception):
    ...


class DecodeError(TAPIError):
    ...


class TelegramAPIError(TAPIError):
    ...


class TelegramNetworkError(TelegramAPIError):
    ...


class TelegramRetryAfter(TelegramAPIError):
    ...


class TelegramMigrateToChat(TelegramAPIError):
    ...


class TelegramBadRequest(TelegramAPIError):
    ...


class TelegramNotFound(TelegramAPIError):
    ...


class TelegramConflictError(TelegramAPIError):
    ...


class TelegramUnauthorizedError(TelegramAPIError):
    ...


class TelegramForbiddenError(TelegramAPIError):
    ...


class TelegramServerError(TelegramAPIError):
    ...


class RestartingTelegram(TelegramServerError):
    ...


class TelegramEntityTooLarge(TelegramNetworkError):
    ...
