from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit

class Scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        # Shut down the scheduler when exiting the app
        atexit.register(lambda: self.scheduler.shutdown())

    def schedule_daily(self, task):
        trigger = CronTrigger(hour=0, minute=0)  # 每天午夜执行一次
        self.scheduler.add_job(task, trigger)

    def schedule_weekly(self, task):
        trigger = CronTrigger(day_of_week='sun', hour=0, minute=0)  # 每周日午夜执行一次
        self.scheduler.add_job(task, trigger)

    def schedule_custom(self, cron_expression, task):
        trigger = CronTrigger.from_crontab(cron_expression)
        self.scheduler.add_job(task, trigger)
