from fastapi import APIRouter, Depends


router = APIRouter(tags=["users"])


@router.get("/personal")
def get_personal_info():
    return {"message": "Personal info retrieved"}
