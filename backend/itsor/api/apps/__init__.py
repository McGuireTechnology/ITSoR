from .auth import app as auth_app
from .custom_app import app as custom_app
from .idm_app import app as idm_app

__all__ = ["auth_app", "idm_app", "custom_app"]
