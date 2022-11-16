from pathlib import Path


class Settings():
    BASE_PATH = Path(__file__).parent.parent
    DATA_PATH = BASE_PATH / 'data'


config = Settings()
