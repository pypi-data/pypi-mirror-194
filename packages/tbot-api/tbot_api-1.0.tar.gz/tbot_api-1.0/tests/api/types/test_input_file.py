from typing import AsyncIterable

from tbot_api.types import BufferedInputFile, FileSystemInputFile, InputFile


class TestInputFile:
    def test_fs_input_file(self) -> None:
        file = FileSystemInputFile(path=__file__)

        assert isinstance(file, InputFile) and isinstance(file, AsyncIterable)
        assert file.chunk_size > 0

    async def test_fs_input_file_readable(self) -> None:
        file = FileSystemInputFile(path=__file__, chunk_size=1)

        assert file.chunk_size == 1

        size = 0
        async for chunk in file:
            chunk_size = len(chunk)
            assert chunk_size == 1
            size += chunk_size
        assert size > 0

    def test_buffered_input_file(self) -> None:
        file = BufferedInputFile(data=b"\f" * 10, filename="file.bin")

        assert isinstance(file, InputFile) and isinstance(file, AsyncIterable)
        assert file.filename == "file.bin"
        assert isinstance(file.data, bytes)

    async def test_buffered_input_file_readable(self) -> None:
        file = BufferedInputFile(data=b"\f" * 10, filename="file.bin", chunk_size=1)

        size = 0
        async for chunk in file:
            chunk_size = len(chunk)
            assert chunk_size == 1
            size += chunk_size
        assert size == 10
