from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import CurrentUser as User, get_current_user, get_user_use_cases
from itsor.api.schemas.auth.user import (
    AuthTokenResponse,
    SigninRequest,
    SignupRequest,
    UserCreate,
    UserReplace,
    UserResponse,
    UserUpdate,
)
from itsor.application.use_cases.auth import UserUseCases
from itsor.domain.ids import UserId

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
def read_users(use_cases: UserUseCases = Depends(get_user_use_cases)):
    return use_cases.list_users()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate, use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        return use_cases.create_user(
            username=body.username,
            email=body.email,
            password=body.password,
            invite_group_id=body.invite_group_id,
            create_tenant_name=body.create_tenant_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/signup", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest, use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        _, token = use_cases.signup(
            username=body.username,
            email=body.email,
            password=body.password,
            invite_group_id=body.invite_group_id,
            create_tenant_name=body.create_tenant_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return AuthTokenResponse(access_token=token)


@router.post("/signin", response_model=AuthTokenResponse)
def signin(body: SigninRequest, use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        _, token = use_cases.login(identifier=body.identifier, password=body.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    return AuthTokenResponse(access_token=token)


@router.post("/signout", status_code=status.HTTP_204_NO_CONTENT)
def signout():
    return None


@router.post("/impersonate", status_code=status.HTTP_204_NO_CONTENT)
def impersonate():
    return None


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: UserId, use_cases: UserUseCases = Depends(get_user_use_cases)):
    user = use_cases.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def replace_user(user_id: UserId, body: UserReplace, use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        return use_cases.replace_user(
            user_id=user_id,
            username=body.username,
            email=body.email,
            password=body.password,
        )
    except ValueError as exc:
        message = str(exc)
        status_code = (
            status.HTTP_409_CONFLICT if "already" in message.lower() else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=status_code, detail=message)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: UserId, body: UserUpdate, use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        return use_cases.update_user(
            user_id=user_id,
            username=body.username,
            email=body.email,
            password=body.password,
        )
    except ValueError as exc:
        message = str(exc)
        status_code = (
            status.HTTP_409_CONFLICT if "already" in message.lower() else status.HTTP_404_NOT_FOUND
        )
        raise HTTPException(status_code=status_code, detail=message)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UserId, use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        use_cases.delete_user(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None

