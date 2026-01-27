import asyncio
from django.core.management.base import BaseCommand
from app.workers.redisQueueWorker import RedisQueueWorker


class Command(BaseCommand):
    help = "Run redis queue worker"
    
    def handle(self, *args, **options):
        worker = RedisQueueWorker()
        asyncio.run(worker.run())
