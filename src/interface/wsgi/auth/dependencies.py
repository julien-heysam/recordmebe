import logging

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src import FAKE_API_KEY, PROJECT_ENVS
from src.constants import Envs
from src.interface.wsgi.auth.exceptions import BadCredentialsException, RequiredOrganizationException
from src.interface.wsgi.auth.json_web_token import DummyJsonWebToken, JsonWebToken
from src.schema.user import UserSchema

logger = logging.getLogger(__name__)


def validate_token(token: HTTPAuthorizationCredentials):
    try:
        if PROJECT_ENVS.ENV_STATE == Envs.LOCAL.value:
            validation = DummyJsonWebToken(token.credentials).validate()
        else:
            validation = JsonWebToken(token.credentials).validate()
    except Exception as e:
        logger.error("Unable to validate token", extra={"error": e}, exc_info=PROJECT_ENVS.DEBUG)
        raise BadCredentialsException
    logger.debug(f"Token validated successfully: {validation}")

    return validation


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    if token != FAKE_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid token")

    return token


class Authenticator:
    dummy_token: str = FAKE_API_KEY
    access_token: str
    auth0_user_id: str
    auth0_org_id: str
    org_name: str
    email: str

    def validate(self, request: Request, token: dict):
        self.access_token = token.get("access_token", "")
        self.auth0_user_id = token.get("sub", "")
        self.auth0_org_id = token.get("org_id", "")
        self.org_name = token.get("org_name") or token.get(
            f"{PROJECT_ENVS.API_AUDIENCE}/{self.auth0_org_id}/org_name", ""
        )
        self.email = token.get("user_email") or token.get(
            f"{PROJECT_ENVS.API_AUDIENCE}/{self.auth0_org_id}/user_email", ""
        )
        logger.debug(
            f"Auth Validation of [auth0_user_id={self.auth0_user_id} auth0_org_id={self.auth0_org_id} org_name={self.org_name} user_email={self.email}]"
        )
        request.state.auth0_user_id = self.auth0_user_id
        request.state.auth0_org_id = self.auth0_org_id
        request.state.org_name = self.org_name
        request.state.email = self.email
        request.state.user = UserSchema(
            org_id=self.org_name,
            email=self.email,
            auth0_user_id=self.auth0_user_id,
            auth0_org_id=self.auth0_org_id,
            name=self.email.split("@")[0],
        )

    def dummy_auth(self, request: Request, token: HTTPAuthorizationCredentials):
        if token.credentials != self.dummy_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

        request.state.auth0_user_id = None
        request.state.org_name = "heysam"
        request.state.email = None
        request.state.auth0_org_id = None
        request.state.user = None

    def web_auth(self, request: Request, token: HTTPAuthorizationCredentials):
        self.validate(request=request, token=validate_token(token))
        if (not self.auth0_org_id or not self.org_name) and PROJECT_ENVS.ENV_STATE != Envs.LOCAL.value:
            logger.error("Error 403, Unable to verify organization")
            raise RequiredOrganizationException
        else:
            logger.debug(
                f"token validated during / web_auth / url:{str(request.url)}, self.email:{self.email} / self.org_name:{self.org_name}"
            )

    def m2m_auth(self, request: Request, token: HTTPAuthorizationCredentials):
        self.validate(request=request, token=validate_token(token))
        logger.debug(
            f"token validated during / m2m_auth / url:{str(request.url)}, self.email:{self.email} / self.org_name:{self.org_name}"
        )

    def __call__(self, request: Request, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        if PROJECT_ENVS.ENV_STATE == Envs.LOCAL.value:
            self.dummy_auth(request=request, token=token)
        else:
            self.web_auth(request=request, token=token)
