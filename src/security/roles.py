from fastapi import Depends, HTTPException, status
from src.security.auth import get_current_user  # or wherever this lives

def require_roles(*allowed_roles: str):
    def dependency(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
    return dependency
