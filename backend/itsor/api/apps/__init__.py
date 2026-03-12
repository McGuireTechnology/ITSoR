from .auth import app as auth_app
from .itam import app as itam_app
from .oscal import app as oscal_app

__all__ = ["auth_app", "itam_app", "oscal_app"]
