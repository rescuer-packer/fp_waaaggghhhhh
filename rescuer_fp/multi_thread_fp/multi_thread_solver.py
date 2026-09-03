from typing import Dict, Any
from datetime import datetime, timedelta
import multiprocessing as mp
from multiprocessing.managers import SyncManager

from rescuer_task.task import RescuerTask

from rescuer_fp.multi_thread_fp.multi_thread_worker import multi_thread_worker
from rescuer_fp.rounder.rounder import Rounder


class MultithreadFpManager:
    def __init__(self, task_jump, ttl_init, callback_wrapper):
        self._state = [0, None]
        self._callback_wrapper = callback_wrapper
        self._task_jump = task_jump
        self._storage = set()
        self._ttl = None
        if ttl_init is not None:
            self._ttl = datetime.now() + timedelta(seconds=ttl_init)

    def store(self, v):
        if v in self._storage:
            return False
        self._storage.add(v)
        return True

    def state(self):
        if self._ttl is not None:
            if datetime.now() > self._ttl:
                self._state[0] = -1
        return self._state

    def register(self, conts, point):
        if self._state[0] != -1:
            if self._state[1] is None or self._state[1] >= conts[0]:
                if self._callback_wrapper.call(conts, point):
                    self._state[0] = -1
                else:
                    self._state[0] += 1
                    self._state[1] = conts[0] - self._task_jump

    def last_wrapper(self):
        return self._callback_wrapper


class FPManager(SyncManager):
    pass


FPManager.register('MultithreadFpManager', callable=MultithreadFpManager,
                   exposed=["store", "state", "register", "last_wrapper"])


def solve(task: RescuerTask, thread_count: int, callback_wrapper, config: Dict[str, Any], ttl_init=None):
    with FPManager() as spawn:
        hash_size = config.get("hash_size", 5)
        rounder = Rounder(task.rescuer_groups, hash_size)
        task_jump = config.get('task_jump', 0.001)
        manager = spawn.MultithreadFpManager(task_jump, ttl_init, callback_wrapper)
        processes = [mp.Process(target=multi_thread_worker, args=(task, rounder, config, manager)) for _ in
                     range(thread_count)]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        return manager.last_wrapper()
