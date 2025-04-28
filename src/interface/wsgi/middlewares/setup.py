import logging

import secure
from fastapi import FastAPI, Request

from src.interface.wsgi.middlewares.auth import SecureHeadersMiddleware

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI) -> None:
    """
    The `setup_middleware` function adds CORS and secure headers middleware to a FastAPI application.

    :param app: The `app` parameter is an instance of the FastAPI application. It represents the FastAPI
    application that the middleware will be added to
    :type app: FastAPI
    """

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        if request.url.path not in ["/healthcheck", "/startup", "/readiness"]:
            logger.debug(
                f"Endpoint called: {request.url.path}, Method: {request.method}, Params: {request.query_params}, Body: {await request.body()}"
            )

        response = await call_next(request)
        return response

    app.add_middleware(
        SecureHeadersMiddleware,
        secure_headers=secure.Secure(
            csp=(
                secure.ContentSecurityPolicy()
                .default_src("'none'")
                .base_uri("'self'")
                .connect_src("'self'")
                .frame_src("'none'")
                .img_src("'self'", "data:", "*")
                .style_src("'self'", "*")
                .script_src("'self'", "'unsafe-inline'", "*")
            ),
            hsts=secure.StrictTransportSecurity().max_age(31536000).include_subdomains(),
            referrer=secure.ReferrerPolicy().no_referrer(),
            cache=secure.CacheControl().no_cache().no_store().max_age(0).must_revalidate(),
            xfo=secure.XFrameOptions().deny(),
        ),
    )
