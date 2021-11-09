import celery


class WatchGuardian(celery.Task):
    def run(self, *args, **kwargs):
        print("Guardian is awake")

