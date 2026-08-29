from cachetools import LRUCache


def single_thread_storage():
    storage = set()
    def _st_check(s):
        if s not in storage:
            storage.add(s)
            return True
        return False
    return lambda x: _st_check(x)


def multy_thread_storage(count, fin_lambda):
    storage = LRUCache(maxsize=count)
    def _st_check(s):
        if s not in storage:
            storage.pop(s)
            return fin_lambda(s)
        return False
    return lambda x: _st_check(x)