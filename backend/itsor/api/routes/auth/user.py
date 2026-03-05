from fastapi import APIRouter, status

from itsor.api.schemas.auth.user import (
    AuthTokenResponse,
    SigninRequest,
    SignupRequest,
    UserCreate,
    UserReplace,
    UserResponse,
    UserUpdate,
)

router = APIRouter(tags=["users"])


@router.get("/users", response_model=list[UserResponse])
def read_users():
    pass


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate):
    pass


@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: str):
    pass


@router.put("/users/{user_id}", response_model=UserResponse)
def replace_user(user_id: str, body: UserReplace):
    pass


@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, body: UserUpdate):
    pass


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    pass


@router.get("/users/me", response_model=UserResponse)
def read_current_user():
    pass


@router.post("/signup", response_model=AuthTokenResponse, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest):
    pass


@router.post("/signin", response_model=AuthTokenResponse)
def signin(body: SigninRequest):
    pass


@router.post("/signout", status_code=status.HTTP_204_NO_CONTENT)
def signout():
    pass

