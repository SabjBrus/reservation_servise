from datetime import date

from fastapi import APIRouter, Depends, status

from app.bookings.schemas import SBookings
from app.bookings.service import BookingService
from app.exceptions import RoomCannotBeBooked
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
    booking = await BookingService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked


@router.delete('/{booking_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
        booking_id: int,
        user: Users = Depends(get_current_user),
):
    await BookingService.delete(id=booking_id, user_id=user.id)
