from typing import Any, Dict


class InnerFPConfig:
    def __init__(self,
                 search_solver_name,
                 search_solver_params,
                 bad_jump_prob,
                 check_border,
                 fine_solver_name,
                 fine_solver_params):
        self.search_solver_name = search_solver_name
        self.search_solver_params = search_solver_params
        self.bad_jump_prob = bad_jump_prob
        self.check_border = check_border
        self.fine_solver_name = fine_solver_name
        self.fine_solver_params = fine_solver_params


def ifp_from_dict(config: Dict[str, Any]):
    return InnerFPConfig(
        config.get('search_solver_name', 'HIGHS'),
        config.get('search_solver_params',
                   """
                   solver=simplex
                   output_flag=false
                   simplex_strategy=1
                   """
                   ),
        config.get('bad_jump_prob', 0.003),
        config.get('check_border', 1e-5),
        config.get('fine_solver_name', 'SCIP'),
        config.get('fine_solver_params', None)
    )
