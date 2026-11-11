
from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select

from app.db.database import DBSession
from app.db.models import Ticket
from app.schemas.ticket import TicketCreate, TicketPublic
from app.schemas.user import UserPublic
from app.core.security import CurrentUser


router = APIRouter()


@router.post(
    "/tickets",
    response_model=TicketPublic,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    data: TicketCreate,
    db: DBSession,
    user: CurrentUser
):

    ticket = Ticket(
        title=data.title,
        description=data.description,
        owner_id=user.id
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.get(
    "/tickets",
    response_model=list[TicketPublic]
)
def list_tickets(
    db: DBSession,
    user: CurrentUser,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=50)
):

    statement = select(Ticket).where(
        Ticket.owner_id == user.id
    )

    tickets = db.scalars(
        statement.offset(offset).limit(limit)
    ).all()

    return list(tickets)


@router.get(
    "/tickets/{ticket_id}",
    response_model=TicketPublic
)
def get_ticket(
    ticket_id: int,
    db: DBSession,
    user: CurrentUser
):

    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if ticket.owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access this ticket"
        )

    return ticket


@router.delete("/tickets/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: DBSession,
    user: CurrentUser
):

    ticket = db.get(Ticket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if ticket.owner_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this ticket"
        )

    db.delete(ticket)
    db.commit()

    return {
        "ok": True,
        "message": "Ticket deleted successfully"
    }


@router.get(
    "/users/me",
    response_model=UserPublic
)
def get_current_user_profile(user: CurrentUser):
    return user
