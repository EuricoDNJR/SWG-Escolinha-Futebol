from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ...dependencies import get_token_header
from app.utils.notification_manager import notification_manager
from app.utils.notifications import send_notifications_now

router = APIRouter()

@router.post("/notifications/send_now", tags=["notifications"], dependencies=[Depends(get_token_header)])
async def force_send_notifications():
    return send_notifications_now()

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
    hour: int
    minute: int

@router.patch("/notifications/schedule", tags=["notifications"], dependencies=[Depends(get_token_header)])
async def update_notification_schedule(schedule: ScheduleUpdate):
    """Update the notification schedule.
    E.g:

        {
            "hour": 15,
            "minute": 07
        }
    
    """
    try:
        notification_manager.update_schedule(schedule.hour, schedule.minute)
        return {"message": f"Notification schedule updated to {schedule.hour}:{schedule.minute}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))