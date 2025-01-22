import aiofiles
import orjson

from data import LANGUAGES


class AsyncJSONManager:
    def __init__(self):
        self.languages = LANGUAGES
        self.cache = {}
        self.LANGUAGES_TITLES = []

    async def read_messages(self):
        for language_code in self.languages:
            file_path = f"data/locale/{language_code}.json"
            try:
                async with aiofiles.open(file_path, "rb") as file:
                    content = await file.read()
                    data = orjson.loads(content)
                    self.cache[language_code] = data  # Cache the result
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {file_path}")
            except orjson.JSONDecodeError:
                raise ValueError(f"Invalid JSON format in file: {file_path}")

    async def close(self):
        self.cache = {}

    async def preload_texts(self) -> None:
        self.LANGUAGES_TITLES = await self.get_languages_title()

    async def get_message(self, language_code: str, key: str):
        return self.cache[language_code][key]

    async def get_languages_title(self) -> list:
        return [await self.get_message(lang, "language_title") for lang in self.languages]

    async def get_language_code(self, language_title: str) -> str:
        for lang in self.languages:
            if await self.get_message(lang, "language_title") == language_title:
                return lang
