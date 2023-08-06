import threading
import time
from typing import Callable

import uvicorn


class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    def run_in_thread(
        self, thread: threading.Thread | None = None
    ) -> Callable[[], None]:
        """Returns a function which can be used to stop the http server"""
        thread = thread or threading.Thread(target=self.run, name="UvicornServer")
        thread.start()
        while not self.started:
            time.sleep(1e-3)

        def stop():
            self.should_exit = True
            thread.join()

        return stop
