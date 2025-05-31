import time
from django.http import JsonResponse


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        user_ip = self.get_client_ip(request)

        if user_ip not in self.requests:
            self.requests[user_ip] = []

        current_time = time.time()

        self.requests[user_ip] = [timestamp for timestamp in self.requests[user_ip] if current_time - timestamp < 60]

        if len(self.requests[user_ip]) >= 100:
            return JsonResponse({'error': 'Too many requests'})

        self.requests[user_ip].append(current_time)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
