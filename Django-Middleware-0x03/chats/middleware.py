from django.http import JsonResponse
import time
import logging
from datetime import datetime
from django.http import HttpResponse

logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        logging.info(f"User: {request.user.id}")
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        current_hour = datetime.now().hour
        if current_hour < 9 or current_hour > 17:
            return HttpResponse("Access restricted to business hours (9 AM - 5 PM)", status=403)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_log = {}
        self.limit = 5
        self.time_window = 60

    def __call__(self, request):
        if request.method == 'POST':
            ip = self.get_client_ip(request)
            now = time.time()

            timestamps = self.message_log.get(ip, [])
            timestamps = [t for t in timestamps if now - t < self.time_window]

            if len(timestamps) >= self.limit:
                return JsonResponse(
                    {"error": "Too many messages. Please wait before sending more."},
                    status=429
                )

            timestamps.append(now)
            self.message_log[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if not request.user.is_staff:
            return JsonResponse({"error": "Permission denied"}, status=403)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
