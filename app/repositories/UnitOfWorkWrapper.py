from django.db import transaction

class UnitOfWorkWrapper:
    def __enter__(self):
        self._ctx = transaction.atomic()
        self._ctx.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._ctx.__exit__(exc_type, exc_value, traceback)
