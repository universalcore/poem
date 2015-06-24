class ViewsBase(object):

    def __init__(self, request):
        self.request = request

    def context(self, **kwargs):
        defaults = {
            'request': self.request,
        }
        defaults.update(kwargs)
        return defaults
