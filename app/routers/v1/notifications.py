from fastapi import APIRouter, HTTPException
from app.utils.notification_manager import notification_manager
from app.utils.notifications import send_notifications_now

router = APIRouter()

@router.patch("/notifications/{action}", tags=["notifications"])
async def toggle_notifications(action: str):
    if action == "start":
        notification_manager.start()
        return {"message": "Email notifications started."}
    elif action == "stop":
        notification_manager.stop()
        return {"message": "Email notifications stopped."}
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'start' or 'stop'.")

@router.post("/notifications/send_now", tags=["notifications"])
async def force_send_notifications():
    return send_notifications_now()