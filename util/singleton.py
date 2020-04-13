class Singleton(object):
    def __init__(self, klass):
        self.klass = klass
        self.obj = {}

    def __call__(self, *args, **kwargs):
        url = args[0]

        if url not in self.obj:
            self.obj[url] = self.klass(*args, **kwargs)
        return self.obj[url]
