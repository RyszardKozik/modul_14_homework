# app/views.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    """
    Root endpoint of the application.
    Returns a simple welcome message.
    """
    return {"message": "Welcome to the API"}

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    Endpoint to retrieve an item by its ID.

    Args:
        item_id (int): The ID of the item.

    Returns:
        dict: A dictionary containing the item details.
    """
    return {"item_id": item_id, "name": "Sample Item"}
