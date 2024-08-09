from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_contacts():
    return {"message": "List of contacts"}
