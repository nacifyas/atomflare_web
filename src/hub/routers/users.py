from fastapi import APIRouter, Depends, HTTPException, Response, status
from hub.auth.dependencies import current_user_admin
from hub.auth.dependencies import get_current_user
from hub.auth.dependencies import get_password_hash
from hub.auth.dependencies import oauth2_scheme
from hub.dal.user import begin
from sqlalchemy.exc import IntegrityError
from hub.models.user import UserRead, UserCreate, UserUpdate


router = APIRouter(
    prefix="/users",
    dependencies=[Depends(oauth2_scheme), Depends(current_user_admin)]
)


@router.get("/", response_model=list[UserRead])
async def get_users(limit: int = 20, skip: int = 0) -> list[UserRead]:
    user_dal = await begin()
    return user_dal.get_all_users(limit, skip)


@router.post('/', response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> Response:
    user_dal = await begin()
    try:
        user.hashed_password = get_password_hash(user.hashed_password)
        await user_dal.create_user(user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=e.orig.args[0]
            )


@router.put(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)]
    )
async def update_user(user: UserUpdate) -> Response:
    user_dal = await begin()
    try:
        if user.hashed_password is not None:
            user.hashed_password = get_password_hash(user.hashed_password)
        updated_user = await user_dal.update_user(user)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=e.orig.args[0]
            )
    else:
        if updated_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such user"
                )
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int) -> Response:
    user_dal = await begin()
    await user_dal.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
