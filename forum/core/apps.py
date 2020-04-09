from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        import core.documents  # noqa
        import core.search.search  # noqa
