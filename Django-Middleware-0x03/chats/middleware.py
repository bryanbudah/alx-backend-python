import os
from datetime import datetime

class RequestLoggingMiddleware:
    """
    Middleware to log each user's request to a file with:
    - timestamp
    - user (authenticated or anonymous)
    - request path
    """

    def __init__(self, get_response):
        """
        Middleware initialization.
        Called only once when the server starts.
        """
        self.get_response = get_response
        # Ensure log file is in project root
        self.log_file = os.path.join(os.path.dirname(__file__), "..", "requests.log")

    def __call__(self, request):
        """
        Called for each request before the view is executed.
        """
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        # Append to the log file
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

        # Continue processing the request
        response = self.get_response(request)
        return response
