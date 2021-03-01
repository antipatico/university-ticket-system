from django.apps import AppConfig


class UtsCommonConfig(AppConfig):
    name = 'uts_common'

    def ready(self):
        import uts_common.signals
