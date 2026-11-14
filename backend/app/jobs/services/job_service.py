"""Service for scheduling background jobs."""

from app.jobs.tasks import log_hello_world


class JobService:
    """Schedule work for execution by Celery workers."""

    def schedule_hello_world(self) -> str:
        """Enqueue the hello-world task to run after 60 seconds."""

        result = log_hello_world.apply_async(countdown=60)
        return result.id
