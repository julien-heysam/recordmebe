# HeySam Core Middleware

This README provides an overview of the middleware components used in the HeySam Core project. The middleware is designed to enhance the security and functionality of a FastAPI application by adding secure headers, logging requests, and serving Sphinx documentation.

## Table of Contents

- [Overview](#overview)
- [SecureHeadersMiddleware](#secureheadersmiddleware)
- [Setup Middleware](#setup-middleware)
- [Sphinx Documentation Setup](#sphinx-documentation-setup)
- [Usage](#usage)
- [Installation](#installation)
- [License](#license)

## Overview

The middleware components in this project are designed to:

- **Enhance Security**: By adding secure headers to HTTP responses.
- **Log Requests**: By logging incoming HTTP requests for monitoring and debugging.
- **Serve Documentation**: By serving Sphinx-generated documentation if available.

## SecureHeadersMiddleware

The `SecureHeadersMiddleware` class is a custom middleware that integrates with FastAPI to add secure headers to HTTP responses. It utilizes the `secure` library to configure various security policies.

### Key Features

- **Content Security Policy (CSP)**: Restricts the sources from which content can be loaded.
- **HTTP Strict Transport Security (HSTS)**: Enforces secure (HTTPS) connections to the server.
- **Referrer Policy**: Controls the amount of referrer information sent with requests.
- **Cache Control**: Prevents caching of sensitive data.
- **X-Frame-Options**: Prevents clickjacking by disallowing the site to be framed.

### Code Example

```python
class SecureHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, secure_headers: secure.Secure) -> None:
        super().__init__(app)
        self.secure_headers = secure_headers

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        self.secure_headers.framework.fastapi(response)
        return response
```

## Setup Middleware

The `setup_middleware` function is responsible for adding middleware to a FastAPI application. It includes both logging and secure headers middleware.

### Functionality

- **Request Logging**: Logs details of incoming HTTP requests except for health check endpoints.
- **Secure Headers**: Adds the `SecureHeadersMiddleware` to the application.

### Code Example

```python
def setup_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        if request.url.path not in ["/healthcheck", "/startup", "/readiness"]:
            logger.info(
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
```

## Sphinx Documentation Setup

The `setup_sphinx_doc` function configures the FastAPI application to serve Sphinx documentation if it exists. It checks for the presence of the documentation and mounts it to the `/sphinx` endpoint.

### Code Example

```python
def setup_sphinx_doc(app: FastAPI) -> None:
    if os.path.exists(PROJECT_PATHS.SPHINX_PATH):
        app.mount("/sphinx", StaticFiles(directory=PROJECT_PATHS.SPHINX_PATH, html=True), name="sphinx")
    elif importlib.util.find_spec("sphinx"):
        os.system("make build_doc")
        app.mount("/sphinx", StaticFiles(directory=PROJECT_PATHS.SPHINX_PATH, html=True), name="sphinx")
    else:
        logging.warning("Can't build/display the sphinx documentation")
```

## Usage

To use the middleware in your FastAPI application, you need to call the `setup_middleware` and `setup_sphinx_doc` functions during the application setup.

### Example

```python
from fastapi import FastAPI
from src.interface.wsgi.middlewares.setup import setup_middleware
from src.interface.wsgi.middlewares.sphinx_doc import setup_sphinx_doc

app = FastAPI()

setup_middleware(app)
setup_sphinx_doc(app)
```

## Installation

To install the necessary dependencies for this middleware, ensure you have the `secure` library and FastAPI installed:

```bash
pip install secure fastapi
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
