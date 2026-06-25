from fastapi import Header, HTTPException, status
from .config import get_settings
from .models import UserRole


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """Simple API key check for local demo.

    In production, replace this with Cognito or Azure AD B2C JWT validation.
    """
    settings = get_settings()
    if settings.app_env.lower() == "local" and x_api_key is None:
        return

    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )


def ensure_role_can_access_ai(role: UserRole) -> None:
    allowed_roles = {UserRole.admin, UserRole.analyst, UserRole.engineer}
    if role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Viewer role can read reports but cannot query the AI layer.",
        )
