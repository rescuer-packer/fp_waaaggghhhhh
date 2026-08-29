import random


class Rounder:
    def __init__(self, groups, hash_size = 5, def_noise = 1e-3, tries = 3):
        self.groups = groups
        self.n = sum(groups)
        self.hash_size = hash_size
        self.hash_sums = _init_hash_sums(hash_size, self.n)
        self.tries = tries
        self.def_noise = def_noise

    def round(self, bool_point, double_point, fin_lambda):
        if len(bool_point) != self.n:
            raise ValueError("bool_point must be of length n")
        if len(double_point) != self.n:
            raise ValueError("double_point must be of length n")
        if self._round_noise(bool_point, double_point, fin_lambda, 0):
            return
        noise = self.def_noise
        while True:
            for i in range(self.tries):
                if self._round_noise(bool_point, double_point, fin_lambda, noise):
                    return
            noise *= 2


    def _round_noise(self, bool_point, double_point, fin_lambda, noise):
        start = 0

        for group in self.groups:
            l = _build_lambda(noise)
            t = min([(double_point[i+start]+l(), i) for i in range(group)])[1]
            for i in range(group):
                bool_point[i + start] = (i != t)
            start += group

        return self._check_known(bool_point, fin_lambda)

    def _check_known(self, bool_point, fin_lambda):
        h = [0]*self.hash_size
        for i in range(self.n):
            if not bool_point[i]:
                for j in range(self.hash_size):
                    h[j] += self.hash_sums[j][i]
        return fin_lambda(tuple(h))



def _init_hash_sums(hash_size, n):
    ans = []
    for i in range(hash_size):
        l = []
        for j in range(n):
            l.append(random.randint(0, 1000000007))
        ans.append(l)
    return ans

def _build_lambda(noise):
    if noise == 0:
        return lambda: 0
    up = random.uniform(0, noise)
    return lambda : random.uniform(0, up)