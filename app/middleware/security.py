"""
Security Middleware

Handles request security, authentication, and input validation.
"""

from fastapi import Request, Response
from typing import Optional, Dict
import time
import re
from loguru import logger
from .base import BaseMiddleware
from ..utils.exceptions import AuthenticationError, ValidationError
from ..config.settings import settings

class SecurityMiddleware(BaseMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.api_key_pattern = re.compile(r'^[A-Za-z0-9-_=]+$')
        self.blocked_ips: Dict[str, float] = {}
        self.max_failed_attempts = 5
        self.block_duration = 300  # 5 minutes

    async def before_request(self, request: Request) -> None:
        """Process security checks before request"""
        client_ip = request.client.host
        
        # Check if IP is blocked
        if self._is_ip_blocked(client_ip):
            raise AuthenticationError("IP temporarily blocked")
        
        # Validate API key if required
        if self._requires_auth(request.url.path):
            await self._validate_api_key(request, client_ip)
        
        # Validate input
        await self._validate_input(request)

    async def after_request(self, response: Response) -> None:
        """Add security headers to response"""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["X-XSS-Protection"] = "1; mode=block"

    def _is_ip_blocked(self, ip: str) -> bool:
        """Check if IP is currently blocked"""
        if ip in self.blocked_ips:
            if time.time() - self.blocked_ips[ip] > self.block_duration:
                del self.blocked_ips[ip]
                return False
            return True
        return False

    def _requires_auth(self, path: str) -> bool:
        """Check if path requires authentication"""
        public_paths = ['/health', '/docs', '/redoc', '/openapi.json']
        return not any(path.startswith(p) for p in public_paths)

    async def _validate_api_key(self, request: Request, client_ip: str) -> None:
        """Validate API key in request"""
        api_key = request.headers.get(settings.API_KEY_HEADER)
        
        if not api_key:
            self._record_failed_attempt(client_ip)
            raise AuthenticationError("API key required")
            
        if not self.api_key_pattern.match(api_key):
            self._record_failed_attempt(client_ip)
            raise AuthenticationError("Invalid API key format")

    async def _validate_input(self, request: Request) -> None:
        """Validate request input"""
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
                if not self._is_safe_input(body):
                    raise ValidationError("Invalid input detected")
            except Exception as e:
                raise ValidationError(f"Invalid request body: {str(e)}")

    def _record_failed_attempt(self, ip: str) -> None:
        """Record failed authentication attempt"""
        if ip in self.blocked_ips:
            return
            
        failed_attempts = getattr(self, f"_failed_{ip}", 0) + 1
        setattr(self, f"_failed_{ip}", failed_attempts)
        
        if failed_attempts >= self.max_failed_attempts:
            self.blocked_ips[ip] = time.time()
            logger.warning(f"IP {ip} blocked due to multiple failed attempts")

    def _is_safe_input(self, data: Dict) -> bool:
        """Check if input data is safe"""
        if isinstance(data, dict):
            return all(
                isinstance(k, str) and self._is_safe_input(v)
                for k, v in data.items()
            )
        if isinstance(data, list):
            return all(self._is_safe_input(item) for item in data)
        return isinstance(data, (str, int, float, bool, type(None))) 