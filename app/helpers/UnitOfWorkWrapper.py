from django.db import transaction

class UnitOfWorkWrapper:
    def __init__(self):
        self._transaction = None

    async def __aenter__(self):
        self._transaction = transaction.atomic()
        self._transaction.__enter__()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        return self._transaction.__exit__(exc_type,exc_value, traceback)
