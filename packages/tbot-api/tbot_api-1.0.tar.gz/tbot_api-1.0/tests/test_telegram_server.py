from tbot_api.telegram import (
    TELEGRAM_SERVER_PRODUCTION,
    FilesPathWrapper,
    TelegramAPIServer,
)


def test_method_url() -> None:
    method_url = TELEGRAM_SERVER_PRODUCTION.api_url(
        token="1:TOKEN",
        method="method",
    )
    assert method_url == "https://api.telegram.org/bot1:TOKEN/method"


def test_file_url() -> None:
    file_url = TELEGRAM_SERVER_PRODUCTION.file_url(token="1:TOKEN", path="file")
    assert file_url == "https://api.telegram.org/file/bot1:TOKEN/file"


def test_from_base() -> None:
    server = TelegramAPIServer.from_base("http://localhost:80", is_local=True)

    method_url = server.api_url("1:TOKEN", method="method")
    file_url = server.file_url(token="1:TOKEN", path="file")

    assert method_url == "http://localhost:80/bot1:TOKEN/method"
    assert file_url == "http://localhost:80/file/bot1:TOKEN/file"
    assert server.is_local


def test_to_local() -> None:
    wrapper = FilesPathWrapper()
    assert wrapper.to_local("/home/user/.bashrc") == "/home/user/.bashrc"


def test_to_server() -> None:
    wrapper = FilesPathWrapper()
    assert wrapper.to_server("/home/user/.bashrc") == "/home/user/.bashrc"
