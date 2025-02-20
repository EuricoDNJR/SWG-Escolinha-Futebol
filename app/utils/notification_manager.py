from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from typing import Optional
from .helper import logging
from .notifications import notify_due_soon_payments, notify_overdue_payments

class NotificationManager:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.due_soon_job = None
        self.overdue_job = None
        self.due_soon_schedule = {"hour": 17, "minute": 3}  # Valores padrão
        self.overdue_schedule = {"hour": 0, "minute": 0}  # Valores padrão

    def start(self):
        if not self.due_soon_job:
            due_soon_trigger = CronTrigger(hour=self.due_soon_schedule["hour"], minute=self.due_soon_schedule["minute"])
            self.due_soon_job = self.scheduler.add_job(notify_due_soon_payments, due_soon_trigger)
        if not self.overdue_job:
            overdue_trigger = CronTrigger(hour=self.overdue_schedule["hour"], minute=self.overdue_schedule["minute"])
            self.overdue_job = self.scheduler.add_job(notify_overdue_payments, overdue_trigger)
        self.scheduler.start()
        print("Notification manager started...")

    def stop(self):
        if self.due_soon_job:
            self.due_soon_job.remove()
            self.due_soon_job = None
        if self.overdue_job:
            self.overdue_job.remove()
            self.overdue_job = None
        self.scheduler.shutdown()
        print("Notification manager stopped...")

    def update_schedule(self, hour_due_soon: Optional[int] = None, minute_due_soon: Optional[int] = None, 
                        hour_overdue: Optional[int] = None, minute_overdue: Optional[int] = None):
        if self.due_soon_job:
            logging.info("Updating due soon notification schedule.")
            if hour_due_soon is not None:
                self.due_soon_schedule["hour"] = hour_due_soon
            if minute_due_soon is not None:
                self.due_soon_schedule["minute"] = minute_due_soon
            
            logging.info(f"Updating due soon notification schedule to {self.due_soon_schedule['hour']}:{self.due_soon_schedule['minute']}")
            new_due_soon_trigger = CronTrigger(
                hour=self.due_soon_schedule["hour"],
                minute=self.due_soon_schedule["minute"]
            )
            self.due_soon_job.reschedule(trigger=new_due_soon_trigger)
            logging.info(f"Due soon notification schedule updated to {self.due_soon_schedule['hour']}:{self.due_soon_schedule['minute']}")

        if self.overdue_job:
            logging.info("Updating overdue notification schedule.")
            if hour_overdue is not None:
                self.overdue_schedule["hour"] = hour_overdue
            if minute_overdue is not None:
                self.overdue_schedule["minute"] = minute_overdue

            logging.info(f"Updating overdue notification schedule to {self.overdue_schedule['hour']}:{self.overdue_schedule['minute']}")
            new_overdue_trigger = CronTrigger(
                hour=self.overdue_schedule["hour"],
                minute=self.overdue_schedule["minute"]
            )
            self.overdue_job.reschedule(trigger=new_overdue_trigger)
            logging.info(f"Overdue notification schedule updated to {self.overdue_schedule['hour']}:{self.overdue_schedule['minute']}")
            
notification_manager = NotificationManager()
