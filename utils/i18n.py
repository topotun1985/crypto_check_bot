from fluent_compiler.bundle import FluentBundle

from fluentogram import FluentTranslator, TranslatorHub


def create_translator_hub() -> TranslatorHub:
    translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en", "ru"),
            "fr": ("fr", "en"),
            "it": ("it", "en"),
            "es": ("es", "en"),
            "de": ("de", "en"),
            "pt": ("pt", "en")
        },
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU",
                    filenames=["locales/ru/LC_MESSAGES/txt.ftl"]
                )
            ),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en-US",
                    filenames=["locales/en/LC_MESSAGES/txt.ftl"]
                )
            ),
            FluentTranslator(
                locale="fr",
                translator=FluentBundle.from_files(
                    locale="fr-FR",
                    filenames=["locales/fr/LC_MESSAGES/txt.ftl"]
                )
            ),
            FluentTranslator(
                locale="it",
                translator=FluentBundle.from_files(
                    locale="it-IT",
                    filenames=["locales/it/LC_MESSAGES/txt.ftl"]
                )
            ),
            FluentTranslator(
                locale="es",
                translator=FluentBundle.from_files(
                    locale="es-ES",
                    filenames=["locales/es/LC_MESSAGES/txt.ftl"]
                )
            ),
            FluentTranslator(
                locale="de",
                translator=FluentBundle.from_files(
                    locale="de-DE",
                    filenames=["locales/de/LC_MESSAGES/txt.ftl"]
                )
            ),
            FluentTranslator(
                locale="pt",
                translator=FluentBundle.from_files(
                    locale="pt-PT",
                    filenames=["locales/pt/LC_MESSAGES/txt.ftl"]
                )
            )
        ],
    )
    return translator_hub