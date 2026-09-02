from typing import Dict, Any

from rescuer_task.task import RescuerTask

from rescuer_fp.inner_fp.inner_fp_config import ifp_from_dict
from rescuer_fp.inner_fp.inner_fp_worker import inner_fp_worker
from rescuer_fp.rounder.hash_storage import single_thread_storage
from rescuer_fp.rounder.rounder import Rounder


def solve(task: RescuerTask, config: Dict[str, Any], callback):
    rounder = Rounder(task.rescuer_groups)
    inner_config = ifp_from_dict(config)
    task_jump = config.get('task_jump', 0.001)
    ttl_init = config.get('ttl_init', None)
    ttl = None
    if ttl_init is not None:
        pass  # время окончания
    state = [0, None]

    def read_state_call():
        # TODO - exit on time limit
        return state[0], state[1]

    def register_solution(conts, point):
        if state[0] != -1:
            if state[1] is None or state[1] >= conts[0]:
                if callback(conts, point):
                    state[0] = -1
                else:
                    state[0] += 1
                    state[1] = conts[0] - task_jump

    inner_fp_worker(task, inner_config, rounder, single_thread_storage(), read_state_call, register_solution)
