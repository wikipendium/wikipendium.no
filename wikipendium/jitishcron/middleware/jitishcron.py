from django.utils.deprecation import MiddlewareMixin

from wikipendium.jitishcron import registered_tasks


class JITishCronMiddleware(MiddlewareMixin):

    def process_request(self, request):
        for task in registered_tasks:
            task()
        return None
