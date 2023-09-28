from fastapi import Depends, HTTPException, status

from .oauth2 import get_current_user


class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user=Depends(get_current_user)):
        if user.user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted! Access closed!"
            )


super_admin_access = RoleChecker(allowed_roles=["admin"])
moderator_access = RoleChecker(allowed_roles=["admin", "moderator"])
user_access = RoleChecker(allowed_roles=["admin", "moderator", "user"])


