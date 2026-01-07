from fastapi import APIRouter, Depends
from controllers.users.process import UserProcess
from db_manager.session import get_db
from db_manager.schemas import ResponseSchema, UserInfo
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["users"])


def user_to_dict(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat() if getattr(user, "created_at", None) else None,
        "updated_at": user.updated_at.isoformat() if getattr(user, "updated_at", None) else None,
    }


@router.post("/create", status_code=201,
            response_model=ResponseSchema)
async def create_user(user_data: UserInfo, db: AsyncSession = Depends(get_db)):

    try:
        insert_dt = UserProcess(db)

        usr = await insert_dt.create_user(user_data.model_dump())
    except Exception as e:
        return ResponseSchema(
            status="error",
            status_code=500,
            message=str(e),
            payload=None
        )

    return ResponseSchema(
        status="success",
        status_code=201,
        message="User created successfully",
        payload=user_to_dict(usr)
    )

@router.post("/get/user", status_code=200,
            response_model=ResponseSchema)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    insert_dt = UserProcess(db)
    usr = await insert_dt.get_user_by_id(user_id)
    return ResponseSchema(
        status="success",
        status_code=200,
        message="User retrieved successfully",
        payload=(user_to_dict(usr) if usr else None)
    )

@router.get("/get/all", status_code=200,
            response_model=ResponseSchema)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    insert_dt = UserProcess(db)
    users = await insert_dt.get_all_users()

    # Convert users to a list of dictionaries
    users_list = [user_to_dict(user) for user in users]
    return ResponseSchema(
        status="success",
        status_code=200,
        message="Users retrieved successfully",
        payload=users_list
    )
    
