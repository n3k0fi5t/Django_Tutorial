import threading
import queue
import time

TASK_QUEUE_SIZE = 100

class PoolLock():
    def __init__(self):
        self._lock = threading.Condition()

    def __enter__(self):
        self._lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()


class TaskPool():
    def __init__(self, size):
        self._lock = PoolLock()
        self._q = queue.Queue(TASK_QUEUE_SIZE)
        self._pool_size = size
        self.tasks = {}

    def add(self, task, tid, *args):
        task = threading.Thread(target=task, args=args)

        try_count = 10
        while try_count > 0:
            with self._lock:
                if not self._q.full():
                    self._q.put_nowait((tid, task))
                    break
            try_count -= 1
        
        return True if try_count > 0 else False

    def run(self):
        while True:
            # add queuing tasks
            with self._lock:
                while len(self.tasks) < self._pool_size and not self._q.empty():
                    tid, task = self._q.get_nowait()
                    self.tasks[tid] = task
                    task.start()

            # try to remove finished tasks
            with self._lock:
                task_ids = set(self.tasks.keys())

            for tid in task_ids:
                with self._lock:
                    task = self.tasks[tid]
                    if not task.is_alive():
                        self.tasks.pop(tid)
            time.sleep(1)