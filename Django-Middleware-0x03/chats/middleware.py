import os
import logging
from datetime import datetime
from django.http import HttpRequest, HttpResponseForbidden
from typing import Callable
class RequestLoggingMiddleware:
    """Logs every request's method, path, and timestamp."""
    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        print(f"[LOG] {datetime.now()} - {request.method} {request.path}")
        return self.get_response(request)

class RestrictAccessByTimeMiddleware:
    """
    Middleware that:
    - Restricts access to the site outside allowed hours (8 AM to 6 PM)
    - Logs each request with timestamp, user, path, method, status, and IP
    """

    ALLOWED_START_HOUR = 8   # 8 AM
    ALLOWED_END_HOUR = 18    # 6 PM

    def __init__(self, get_response: Callable):
        self.get_response = get_response
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Configure and return a logger instance"""
        logger = logging.getLogger('request_logger')
        logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Log file handler
        log_file = os.path.join(log_dir, "requests.log")
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

        logger.addHandler(file_handler)
        return logger

    def __call__(self, request: HttpRequest):
        """Restrict access by time and log requests"""
        try:
            # Restrict access based on current hour
            current_hour = datetime.now().hour
            if current_hour < self.ALLOWED_START_HOUR or current_hour >= self.ALLOWED_END_HOUR:
                return HttpResponseForbidden("Access is restricted at this time.")

            # Get user info safely
            user = "Anonymous"
            if hasattr(request, 'user'):
                user = request.user.username if request.user.is_authenticated else "Anonymous"

            # Process the request
            response = self.get_response(request)

            # Log request info
            log_data = {
                'user': user,
                'method': request.method,
                'path': request.path,
                'status': response.status_code,
                'ip': self._get_client_ip(request)
            }
            self.logger.info(
                "User: %(user)s - %(method)s %(path)s - Status: %(status)s - IP: %(ip)s",
                log_data
            )

            return response

        except Exception as e:
            self.logger.error("Error processing request: %s", str(e))
            raise

    def _get_client_ip(self, request: HttpRequest) -> str:
        """Extract client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR', 'unknown')
