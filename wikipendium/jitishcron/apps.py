from django.apps import AppConfig


class JitishcronConfig(AppConfig):
    name = 'wikipendium.jitishcron'
    label = 'wikipendium__jitishcron'

    def ready(self):
        import wikipendium.jitishcron.tasks  # noqa
