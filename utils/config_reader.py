import configparser
from pathlib import Path


class ConfigReader:
    """
    Utility class to load and expose configuration parameters for Playwright tests.
    Resolves configuration file relative to the project root.
    """
    _config = None

    @classmethod
    def _load_config(cls):
        if cls._config is None:
            cls._config = configparser.ConfigParser()
            project_root = Path(__file__).resolve().parent.parent
            config_path = project_root / "config" / "config.ini"

            if not config_path.exists():
                raise FileNotFoundError(f"Configuration file not found at: {config_path}")

            cls._config.read(config_path)

    @classmethod
    def get_base_url(cls) -> str:
        cls._load_config()
        return cls._config.get("DEFAULT", "base_url")

    @classmethod
    def get_browser(cls) -> str:
        cls._load_config()
        return cls._config.get("DEFAULT", "browser", fallback="chromium")

    @classmethod
    def is_headless(cls) -> bool:
        cls._load_config()
        return cls._config.getboolean("DEFAULT", "headless", fallback=False)

    @classmethod
    def get_timeout(cls) -> int:
        cls._load_config()
        return cls._config.getint("DEFAULT", "timeout", fallback=15000)

    @classmethod
    def get_search_term(cls) -> str:
        cls._load_config()
        return cls._config.get("TEST_DATA", "search_term", fallback="laptop")
