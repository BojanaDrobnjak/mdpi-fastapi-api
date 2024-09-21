import importlib
from typing import Any, Dict, Optional

from loguru import logger
from mdpi_api.localization.i18n_middleware import get_locale


class Translator:
    """Translator class to translate strings from locale files."""

    _instances: Dict[str, "Translator"] = {}

    def __new__(cls, lang: str = "") -> "Translator":
        """
        Create a new instance of Translator class.

        :param lang: Language to be used for translation.
        :return: Translator instance.
        """
        if lang not in cls._instances:
            cls._instances[lang] = super().__new__(cls)
        return cls._instances[lang]

    def __init__(self, lang: Optional[str] = ""):
        if not lang:
            lang = get_locale()
        self.lang = lang

    def t(  # noqa: WPS111, WPS231
        self,
        key: str,
        **kwargs: Any,
    ) -> Optional[str]:
        """
        Translate a string.

        :param key: Key to be translated.
        :param kwargs: Keyword arguments to be used for string formatting.
        :return: Translated string.

        :raises KeyError: If the key is not found in the locale file.
        """
        try:
            file_key, *translation_keys = key.split(".")

            # Construct the module path
            locale_module_path = f"mdpi_api.localization.{self.lang}.{file_key}"

            # Import the module
            locale_module = importlib.import_module(locale_module_path)

            # Get the initial translation
            translation = locale_module.locale

            # Traverse the translation dictionary based on the keys
            for translation_key in translation_keys:
                translation = translation.get(translation_key, None)
                if translation is None:
                    raise KeyError(f"Key {key} not found in {self.lang} locale")

            # Format the translation with kwargs if any
            if kwargs.keys():
                translation = translation.format(**kwargs)

            return translation

        except Exception as exception:
            logger.debug(f"Error while translating key {key}: {exception}")
            return None
