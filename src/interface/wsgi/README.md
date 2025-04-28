# HeySam Core WSGI Interface

This repository contains the WSGI interface for the HeySam Core application. It is built using FastAPI and provides a set of RESTful APIs for managing various resources such as users, organizations, deals, meetings, and more. The interface is designed to be scalable, secure, and easy to integrate with other services.

## Table of Contents

- [Overview](#overview)
- [Setup and Installation](#setup-and-installation)
- [Modules and Functionality](#modules-and-functionality)
- [Routes](#routes)
- [Authentication](#authentication)
- [Middleware](#middleware)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Overview

The HeySam Core WSGI Interface is a backend service that provides APIs for managing and interacting with various entities such as users, organizations, deals, meetings, and more. It leverages FastAPI for building the APIs and integrates with various third-party services for enhanced functionality, including Datadog for monitoring and Ably for real-time messaging.

## Setup and Installation

To set up and run the HeySam Core WSGI Interface, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/julienwuthrich/heysam-core.git
   cd heysam-core/src/interface/wsgi
   ```

2. **Install Dependencies:**
   Ensure you have Python 3.8+ installed. Then, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables:**
   Set up the necessary environment variables. You can use a `.env` file or export them directly in your shell. Key variables include:
   - `DATABASE_URI`
   - `PROJECT_ENVS`
   - `API_KEYS`
   - `DD_AGENT_HOST`
   - `DD_TRACE_AGENT_PORT`

4. **Run the Application:**
   Start the FastAPI application using a WSGI server like Uvicorn:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

## Modules and Functionality

### Setup Module

- **Datadog Integration:** Configures Datadog for monitoring and tracing.
- **Database Session Management:** Provides utilities for managing database sessions using SQLAlchemy.

### Authentication Module

- **JWT Validation:** Validates JSON Web Tokens (JWT) for secure API access.
- **Webhook Verification:** Verifies incoming webhooks using tokens.

### Middleware

- **Secure Headers:** Adds security headers to HTTP responses.
- **Request Logging:** Logs incoming requests for monitoring and debugging.

### Routes

The application provides a wide range of routes for managing different resources. Below is a summary of the key routes:

| Route Prefix                  | Description                                           |
|-------------------------------|-------------------------------------------------------|
| `/user`                       | Manage user resources.                                |
| `/org`                        | Manage organization resources.                        |
| `/deal`                       | Manage deal resources.                                |
| `/meeting_transcription`      | Handle meeting transcription data.                    |
| `/meeting_email_summary`      | Manage meeting email summaries.                       |
| `/meeting_gap_extraction`     | Extract gaps from meeting data.                       |
| `/meeting_question_extraction`| Extract questions from meeting data.                  |
| `/meeting_sizzle`             | Manage meeting sizzle data.                           |
| `/meeting_topic`              | Manage meeting topics.                                |
| `/recording`                  | Manage meeting recordings.                            |
| `/ask_about`                  | Handle "ask about" queries.                           |
| `/debugger`                   | Debugging and environment information.                |
| `/probes`                     | Health and readiness probes.                          |

### Authentication

The application uses JWT for authentication. Tokens are validated using the `JsonWebToken` class, which checks the token's signature, issuer, audience, and expiration. The `Authenticator` class provides dependency injection for securing routes.

### Middleware

The application includes middleware for adding security headers and logging requests. The `SecureHeadersMiddleware` class uses the `secure` library to add headers like Content Security Policy (CSP) and Strict Transport Security (HSTS).

### Error Handling

The application uses FastAPI's exception handling to manage errors. Custom exceptions are defined for common error scenarios, such as `UnableCredentialsException` and `BadCredentialsException`.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
