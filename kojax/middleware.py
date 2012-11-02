class KojaxMiddleware(object):
    def process_request(self, request):
        request.kojax = ('application/x-kojax' in
            request.META.get('HTTP_ACCEPT', '').split(','))
