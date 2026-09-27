"""
Complaint route handlers.

Thin layer only — validate input, call service, return response.
No business logic or direct store access here.
"""
from __future__ import annotations

from fastapi import APIRouter, status

from schemas.complaint import ComplaintCreate, ComplaintOut, StatusUpdate
from services import complaint_service

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.post(
    "",
    response_model=ComplaintOut,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new complaint",
)
async def create_complaint(body: ComplaintCreate) -> ComplaintOut:
    return await complaint_service.create_complaint(body)


@router.get(
    "",
    response_model=list[ComplaintOut],
    summary="List all complaints",
)
def list_complaints() -> list[ComplaintOut]:
    return complaint_service.list_complaints()


@router.get(
    "/{complaint_id}",
    response_model=ComplaintOut,
    summary="Get a single complaint by ID",
)
def get_complaint(complaint_id: str) -> ComplaintOut:
    return complaint_service.get_complaint(complaint_id)


@router.patch(
    "/{complaint_id}/status",
    response_model=ComplaintOut,
    summary="Update complaint status (enforces legal transitions)",
    responses={
        409: {"description": "Illegal status transition"},
        404: {"description": "Complaint not found"},
    },
)
def update_status(complaint_id: str, body: StatusUpdate) -> ComplaintOut:
    return complaint_service.update_status(complaint_id, body)
