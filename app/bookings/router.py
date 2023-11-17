from datetime import date

from fastapi import APIRouter, Depends


from app.bookings.schemas import SBookings
from app.bookings.service import BookingService
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования'],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingService.find_all(user_id=user.id)


@router.post('')
async def add_bookings(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user),
):
    booking = BookingService.add(user.id, room_id, date_from, date_to)
