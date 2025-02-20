from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional
from ...dependencies import get_token_header
from app.utils.notification_manager import notification_manager
from app.utils.notifications import send_notifications_now

router = APIRouter()

@router.post("/notifications/send_now", tags=["notifications"], dependencies=[Depends(get_token_header)])
async def force_send_notifications(due_soon: bool = Query(True), overdue: bool = Query(True)):
    return send_notifications_now(due_soon, overdue)


@router.patch("/notifications/toggle", tags=["notifications"], dependencies=[Depends(get_token_header)])
async def toggle_notifications(action: str):
    if action == "start":
        notification_manager.start()
        return {"message": "Email notifications started."}
    elif action == "stop":
        notification_manager.stop()
        return {"message": "Email notifications stopped."}
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'start' or 'stop'.")

class ScheduleUpdate(BaseModel):
    hour_due_soon: Optional[int] = None
    minute_due_soon: Optional[int] = None
    hour_overdue: Optional[int] = None
    minute_overdue: Optional[int] = None

@router.patch("/notifications/schedule", tags=["notifications"], dependencies=[Depends(get_token_header)])
async def update_notification_schedule(schedule: ScheduleUpdate):
    """Update the notification schedule.
    E.g:

        {
            "hour_due_soon": 15,
            "minute_due_soon": 7,
            "hour_overdue": 1,
            "minute_overdue": 5
        }
    
    """
    try:
        notification_manager.update_schedule(
            hour_due_soon=schedule.hour_due_soon if schedule.hour_due_soon != 0 else None,
            minute_due_soon=schedule.minute_due_soon if schedule.minute_due_soon != 0 else None,
            hour_overdue=schedule.hour_overdue if schedule.hour_overdue != 0 else None,
            minute_overdue=schedule.minute_overdue if schedule.minute_overdue != 0 else None
        )
        return {"message": "Notification schedule(s) updated!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
