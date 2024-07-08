from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from .notifications import notify_due_payments

class NotificationManager:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.job = None

    def start(self):
        if not self.job:
            trigger = CronTrigger(hour=17, minute=3)  # Configura para formato 24h
            self.job = self.scheduler.add_job(notify_due_payments, trigger)
            self.scheduler.start()
            print("Notification manager started...")

    def stop(self):
        if self.job:
            self.job.remove()
            self.job = None
            self.scheduler.shutdown()
            print("Notification manager stopped...")

notification_manager = NotificationManager()
