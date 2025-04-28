import secure
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class SecureHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, secure_headers: secure.Secure) -> None:
        super().__init__(app)
        self.secure_headers = secure_headers

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        self.secure_headers.framework.fastapi(response)
        return response
