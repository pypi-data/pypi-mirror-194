from reactivex import scheduler
import threading
import functools

def named_thread_factory(target, name) -> threading.Thread:
    return threading.Thread(target=target, daemon=True, name=name)

class NamedNewThreadScheduler(scheduler.NewThreadScheduler):
    def __init__(self, name: str):
        return super().__init__(functools.partial(
            named_thread_factory, name=name
        ))