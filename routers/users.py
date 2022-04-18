from fastapi import APIRouter, Depends, HTTPException, Response, status
from auth.dependencies import current_user_admin, get_current_user, get_password_hash, oauth2_scheme
from sql.dal.user import UserDAL
from sql.database import async_session
from models.user import UserRead, UserCreate, UserUpdate


router = APIRouter(
    prefix="/users",
    dependencies=[Depends(oauth2_scheme), Depends(current_user_admin)]
)


@router.get("/", response_model=list[UserRead])
async def get_users(limit: int = 20, skip: int = 0) -> list[UserRead]:
    async with async_session() as session:
        async with session.begin():
            userStream = UserDAL(session)
            stream = await userStream.get_all_users(limit, skip)
            return [UserRead(**user.dict()) for user in stream]


@router.post('/', response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> None:
    async with async_session() as session:
        async with session.begin():
            new_user = UserDAL(session)
            try:
                user.hashed_password=get_password_hash(user.hashed_password)
                await new_user.create_user(user)
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            except Exception:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The input data is not valid")


@router.put("/", status_code=status.HTTP_204_NO_CONTENT, dependencies=get_current_user)
async def update_user(user: UserUpdate) -> None:
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            try:
                if user.hashed_password: user.hashed_password=get_password_hash(user.hashed_password)
                await user_dal.update_user(user)
            except Exception:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="The input data is not valid")
            else:
                return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            await user_dal.delete_user(user_id)
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        