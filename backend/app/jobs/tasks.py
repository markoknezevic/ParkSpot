"""Celery tasks executed by background workers."""

import logging

from app.jobs.celery_app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(name="jobs.log_hello_world")
def log_hello_world() -> None:
    """Write a hello-world message to the Celery worker log."""

    logger.info("Hello World")

