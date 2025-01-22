import aiofiles
import orjson

from data import LANGUAGES


class AsyncJSONManager:
    def __init__(self):
        self.languages = LANGUAGES
        self.cache = {}
        self.LANGUAGES_TITLES = []
        self.MAIN_MENU_BUTTON1 = []
        self.MAIN_MENU_BUTTON2 = []
        self.MAIN_MENU_BUTTON3 = []
        self.MAIN_MENU_BUTTON4 = []
        self.READY_GAME_BUTTON = []
        self.READY_ROBOT_GAME_BUTTON = []
        self.SET_LANGUAGE_BUTTON = []
        self.BACK_BUTTON = []
        self.TRUE_ROBOT_NUMBER_BUTTON = []
        self.SMALL_ROBOT_NUMBER_BUTTON = []
        self.BIG_ROBOT_NUMBER_BUTTON = []

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
        self.MAIN_MENU_BUTTON1 = await self.get_menu_title(1)
        self.MAIN_MENU_BUTTON2 = await self.get_menu_title(2)
        self.MAIN_MENU_BUTTON3 = await self.get_menu_title(3)
        self.MAIN_MENU_BUTTON4 = await self.get_menu_title(4)
        self.READY_GAME_BUTTON = await self.get_ready_game_title()
        self.READY_ROBOT_GAME_BUTTON = await self.get_ready_robot_game_title()
        self.SET_LANGUAGE_BUTTON = await self.get_menu_title(5)
        self.BACK_BUTTON = await self.get_menu_title(6)
        self.TRUE_ROBOT_NUMBER_BUTTON = await self.get_true_robot_num_title()
        self.SMALL_ROBOT_NUMBER_BUTTON = await self.get_small_robot_num_title()
        self.BIG_ROBOT_NUMBER_BUTTON = await self.get_big_robot_num_title()

    async def get_message(self, language_code: str, key: str):
        return self.cache[language_code][key]

    async def get_languages_title(self) -> list:
        return [await self.get_message(lang, "language_title") for lang in self.languages]

    async def get_language_code(self, language_title: str) -> str:
        for lang in self.languages:
            if await self.get_message(lang, "language_title") == language_title:
                return lang

    async def get_menu_title(self, code: int = 1) -> list:
        return [await self.get_message(lang, f"main_menu_button{code}") for lang in self.languages]

    async def get_ready_game_title(self) -> list:
        return [await self.get_message(lang, "ready_game_button") for lang in self.languages]

    async def get_ready_robot_game_title(self) -> list:
        return [await self.get_message(lang, "ready_robot_game_button") for lang in self.languages]

    async def get_true_robot_num_title(self) -> list:
        return [await self.get_message(lang, "true_robot_number_button") for lang in self.languages]

    async def get_small_robot_num_title(self) -> list:
        return [await self.get_message(lang, "small_robot_number_button") for lang in self.languages]

    async def get_big_robot_num_title(self) -> list:
        return [await self.get_message(lang, "big_robot_number_button") for lang in self.languages]
