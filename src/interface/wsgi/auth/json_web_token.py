import logging
from dataclasses import dataclass

import jwt

from src import PROJECT_ENVS
from src.interface.wsgi.auth.exceptions import UnableCredentialsException

logger = logging.getLogger(__name__)


@dataclass
class JsonWebToken:
    """Perform JSON Web Token (JWT) validation using PyJWT"""

    jwt_access_token: str
    auth0_issuer_url: str = PROJECT_ENVS.ISSUER
    auth0_audience: str = PROJECT_ENVS.API_AUDIENCE
    algorithm: str = PROJECT_ENVS.ALGORITHMS
    jwks_uri: str = f"https://{PROJECT_ENVS.DOMAIN}/.well-known/jwks.json"
    options = {
        "verify_iat": True,
        "verify_signature": True,
        "verify_user": True,
        "verify_exp": True,
        "verify_iss": True,
    }

    def validate(self):
        logger.debug(f"Starting Token validation\nAccess token: {self.jwt_access_token}")
        try:
            jwks_client = jwt.PyJWKClient(self.jwks_uri)
            jwt_signing_key = jwks_client.get_signing_key_from_jwt(self.jwt_access_token).key
            payload = jwt.decode(
                self.jwt_access_token,
                jwt_signing_key,
                algorithms=self.algorithm,
                audience=self.auth0_audience,
                issuer=self.auth0_issuer_url,
                options=self.options,
            )
            payload["access_token"] = self.jwt_access_token
        except jwt.exceptions.PyJWKClientError as e:
            logger.error(
                f"PyJWKClientError: {e}",
                extra={"error": e},
                exc_info=PROJECT_ENVS.DEBUG,
            )
            raise UnableCredentialsException
        except jwt.ExpiredSignatureError as e:
            logger.error(f"Token expired: {e}", extra={"error": e}, exc_info=PROJECT_ENVS.DEBUG)
            raise e
        except jwt.exceptions.InvalidTokenError as e:
            logger.error(f"Bad credentials: {e}", extra={"error": e}, exc_info=PROJECT_ENVS.DEBUG)
            raise e
        except Exception as e:
            logger.error(
                f"Unknown jwt validation error: {e}",
                extra={"error": e},
                exc_info=PROJECT_ENVS.DEBUG,
            )
            raise e

        return payload


class DummyJsonWebToken(JsonWebToken):
    options = {
        "verify_iat": False,
        "verify_signature": False,
        "verify_user": False,
        "verify_exp": False,
        "verify_iss": False,
    }

    def validate(self):
        logger.info("Dummy authentication !")
        return super().validate()
