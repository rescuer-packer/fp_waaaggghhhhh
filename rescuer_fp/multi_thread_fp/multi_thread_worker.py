from typing import Dict, Any

from rescuer_task.task import RescuerTask

from rescuer_fp.inner_fp.inner_fp_config import ifp_from_dict
from rescuer_fp.inner_fp.inner_fp_worker import inner_fp_worker
from rescuer_fp.rounder.hash_storage import multy_thread_storage
from rescuer_fp.rounder.rounder import Rounder


def multi_thread_worker(task: RescuerTask, rounder: Rounder, config: Dict[str, Any], manager):
    inner_config = ifp_from_dict(config)
    thread_cache_size = config.get('thread_cache_size', 10000)
    storage = multy_thread_storage(thread_cache_size, manager.store)
    inner_fp_worker(task, inner_config, rounder, storage, manager.state, manager.register)
