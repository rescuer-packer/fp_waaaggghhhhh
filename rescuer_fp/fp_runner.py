
from rescuer_task.task import RescuerTask
from rescuer_fp.single_thread_fp.single_thread_solver import  solve as solve_single
from rescuer_fp.multi_thread_fp.multi_thread_solver import solve as solve_multi



class FPResultStore:
    def __init__(self, exit_fast: bool = False, log_improve: int = 0):
        self.exit_fast = exit_fast
        self.log_improve = log_improve
        self.conts = None
        self.rescuers = None

    def call(self, conts, rescuers):
        self.conts = conts
        self.rescuers = rescuers
        log_arr = []
        if self.log_improve >= 0:
            log_arr.append(conts[0])
        if self.log_improve >= 1:
            log_arr.append(conts)
        if self.log_improve >= 2:
            log_arr.append(rescuers)
        if len(log_arr)>0:
            print(log_arr)


def run_feasibility_pump(task: RescuerTask,  callback_wrapper = None, thread_count: int = 1, config=None, ttl_init=None):
    if config is None:
        config = {}
    if callback_wrapper is None:
        callback_wrapper = FPResultStore()

    if thread_count == 1:
        solve_single(task, config, callback_wrapper.call, ttl_init=ttl_init)
        return callback_wrapper

    return solve_multi(task, thread_count,  callback_wrapper, config, ttl_init=ttl_init)
