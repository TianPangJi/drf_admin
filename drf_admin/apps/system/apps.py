from django.apps import AppConfig


class SystemConfig(AppConfig):
    name = 'system'

    def ready(self):
        import system.jobs.run
        import system.signals
