

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

