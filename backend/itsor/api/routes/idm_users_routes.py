from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import CurrentUser, get_current_user, get_idm_account_use_cases
from itsor.api.schemas.idm_users_schemas import IdmAccountCreate, IdmAccountResponse, IdmAccountUpdate
from itsor.application.use_cases.identity_use_cases import IdmAccountUseCases

router = APIRouter(tags=["accounts"])

_ACCOUNTS_PATH = "/accounts"
_LEGACY_USERS_PATH = "/users"


@router.get(_ACCOUNTS_PATH, response_model=list[IdmAccountResponse])
@router.get(_LEGACY_USERS_PATH, response_model=list[IdmAccountResponse], include_in_schema=False)
def list_idm_accounts(_: CurrentUser = Depends(get_current_user), use_cases: IdmAccountUseCases = Depends(get_idm_account_use_cases)):
    return use_cases.list_accounts()


@router.post(_ACCOUNTS_PATH, response_model=IdmAccountResponse, status_code=status.HTTP_201_CREATED)
@router.post(_LEGACY_USERS_PATH, response_model=IdmAccountResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_idm_account(
    body: IdmAccountCreate,
    _: CurrentUser = Depends(get_current_user),
    use_cases: IdmAccountUseCases = Depends(get_idm_account_use_cases),
):
    try:
        return use_cases.create_account(
            person_id=body.person_id,
            username=body.username,
            account_status=body.account_status,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get(f"{_ACCOUNTS_PATH}/{{account_id}}", response_model=IdmAccountResponse)
@router.get(f"{_LEGACY_USERS_PATH}/{{account_id}}", response_model=IdmAccountResponse, include_in_schema=False)
def get_idm_account(
    account_id: str,
    _: CurrentUser = Depends(get_current_user),
    use_cases: IdmAccountUseCases = Depends(get_idm_account_use_cases),
):
    account = use_cases.get_account(account_id)
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IDM account not found")
    return account


@router.patch(f"{_ACCOUNTS_PATH}/{{account_id}}", response_model=IdmAccountResponse)
@router.patch(f"{_LEGACY_USERS_PATH}/{{account_id}}", response_model=IdmAccountResponse, include_in_schema=False)
def update_idm_account(
    account_id: str,
    body: IdmAccountUpdate,
    _: CurrentUser = Depends(get_current_user),
    use_cases: IdmAccountUseCases = Depends(get_idm_account_use_cases),
):
    try:
        return use_cases.update_account(
            account_id=account_id,
            username=body.username,
            account_status=body.account_status,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete(f"{_ACCOUNTS_PATH}/{{account_id}}", status_code=status.HTTP_204_NO_CONTENT)
@router.delete(f"{_LEGACY_USERS_PATH}/{{account_id}}", status_code=status.HTTP_204_NO_CONTENT, include_in_schema=False)
def delete_idm_account(
    account_id: str,
    _: CurrentUser = Depends(get_current_user),
    use_cases: IdmAccountUseCases = Depends(get_idm_account_use_cases),
):
    try:
        use_cases.delete_account(account_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


list_idm_users = list_idm_accounts
create_idm_user = create_idm_account
get_idm_user = get_idm_account
update_idm_user = update_idm_account
delete_idm_user = delete_idm_account
