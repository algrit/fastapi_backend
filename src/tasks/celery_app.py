from celery import Celery

from src.config import settings

celery_instance: Celery = Celery(
    "celery_tasks", broker=settings.REDIS_URL, include=["src.tasks.tasks"]
)

celery_instance.conf.beat_schedule = {"first": {"task": "today_checkin", "schedule": 30}}
