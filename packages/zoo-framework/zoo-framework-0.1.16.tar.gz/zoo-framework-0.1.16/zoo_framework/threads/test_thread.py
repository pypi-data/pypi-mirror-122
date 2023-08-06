from zoo_framework.threads import BaseThread

class TestThread(BaseThread):
    def __init__(self):
        BaseThread.__init__(self, {
            "is_loop": True,
            "delay_time": 10,
            "name": "test_thread"
        })

    def _execute(self):
        pass

    def _destroy(self):
        pass

    def _on_error(self):
        pass

    def _on_done(self):
        pass