"""Celery application configuration."""

import os

from celery import Celery


celery_app = Celery(
    "parkspot",
    broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
    include=["app.jobs.tasks"],
)
celery_app.conf.task_default_queue = "jobs"
