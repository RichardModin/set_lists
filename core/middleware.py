from django.contrib.messages import get_messages

class ClearMessagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Only clear messages for non-redirect responses
        if hasattr(request, '_messages') and not response.has_header('Location'):
            list(get_messages(request))  # Retrieve and clear messages
        return response