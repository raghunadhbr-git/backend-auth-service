"""
This file simply exposes the model classes
so that Flask-Migrate (Alembic) can discover them.
"""

from .user import User
from .token_blacklist import TokenBlocklist

__all__ = ["User", "TokenBlocklist"]
