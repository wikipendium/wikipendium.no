from wikipendium.jitishcron import registered_tasks


class JITishCronMiddleware(object):

    def process_request(self, request):
        for task in registered_tasks:
            task()
        return None
