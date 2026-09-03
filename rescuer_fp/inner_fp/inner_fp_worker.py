import random

from ortools.linear_solver import pywraplp
from rescuer_task.task import RescuerTask
from rescuer_task.solvers import as_lp_task, as_lp_task_with_point

from rescuer_fp.inner_fp.inner_fp_config import InnerFPConfig
from rescuer_fp.rounder.rounder import Rounder


def inner_fp_worker(
        task: RescuerTask,
        config: InnerFPConfig,
        rounder: Rounder,
        rounder_call,
        read_state_call,
        task_call
):
    solver = pywraplp.Solver.CreateSolver(config.search_solver_name)
    if config.search_solver_params is not None:
        solver.SetSolverSpecificParametersAsString(config.search_solver_params)
    conts, rescuers = as_lp_task(solver, task)
    cnt = len(rescuers)
    double_point = [random.uniform(0, 1) for _ in range(cnt)]
    bool_point = [False] * cnt
    quality = 1e15  # inf
    state = 0
    while True:
        ns, nb = read_state_call()
        if ns == -1:
            return
        if ns != state:
            state = ns
            solver.Add(conts[0] <= nb)
            quality = 1e15
        rounder.round(bool_point, double_point, rounder_call)
        rs = []
        for i in range(cnt):
            if not bool_point[i]:
                rs.append(rescuers[i])
        rss = solver.Sum(rs)
        solver.Minimize(rss)
        status = solver.Solve()
        if status not in config.search_possible_states:
            raise ValueError("WTF")
        nq = rss.solution_value()
        if nq < quality or random.uniform(0, 1) < config.bad_jump_prob:
            quality = nq
            for i in range(cnt):
                double_point[i] = rescuers[i].solution_value()
        if nq < config.check_border:
            _try_find_solution(task, config, bool_point, task_call)


def _try_find_solution(task, config, bool_point, task_call):
    solver = pywraplp.Solver.CreateSolver(config.fine_solver_name)
    if config.fine_solver_params is not None:
        solver.SetSolverSpecificParametersAsString(config.fine_solver_params)
    conts = as_lp_task_with_point(solver, task, bool_point)
    solver.Minimize(conts[0])
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL and status != pywraplp.Solver.FEASIBLE:
        return
    ans = [cont.solution_value() for cont in conts]
    task_call(ans, bool_point)
