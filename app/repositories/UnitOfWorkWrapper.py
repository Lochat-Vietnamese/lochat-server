from django.db import transaction
from asgiref.sync import sync_to_async


class UnitOfWorkWrapper:
    async def __aenter__(self):
        self._ctx = transaction.atomic()
        await sync_to_async(self._ctx.__enter__, thread_sensitive=True)()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return await sync_to_async(self._ctx.__exit__, thread_sensitive=True)(
            exc_type, exc_value, traceback
        )
