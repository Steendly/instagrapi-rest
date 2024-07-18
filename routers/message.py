from typing import Optional, Dict, List
from enum import Enum

from fastapi import APIRouter, Depends, Form
from instagrapi.types import (
    User, UserShort, DirectThread
)

from dependencies import ClientStorage, get_clients

router = APIRouter(
    prefix="/message",
    tags=["message", "thread"],
    responses={404: {"description": "Not found"}},
)


class FilterThreadsOptions(str, Enum):
    flagged = "flagged"
    unread = "unread"


@router.post("/threads", response_model=List[DirectThread])
async def threads(sessionid: str = Form(...),
                  amount: Optional[int] = Form(20),
                  selected_filter: Optional[FilterThreadsOptions] = Form(""),
                  thread_message_limit: Optional[int] = Form(None),
                  clients: ClientStorage = Depends(get_clients)) -> List[DirectThread]:
    """Get all threads from inbox
    """
    cl = clients.get(sessionid)
    return cl.direct_threads(amount, selected_filter, thread_message_limit=thread_message_limit)
