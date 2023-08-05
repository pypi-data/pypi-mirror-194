import numpy as np
import scipy.interpolate
from numpy.typing import NDArray

from .phase import Phase


def V_interpolation(x_old: NDArray[np.float64], x_new: NDArray[np.float64]) -> NDArray[np.float64]:
    if not len(x_new):
        return np.array([], dtype=np.float64).reshape(0, len(x_old))
    # scale to [0, 1]
    x_new = (x_new - x_old[0]) / (x_old[-1] - x_old[0])
    x_old = (x_old - x_old[0]) / (x_old[-1] - x_old[0])
    V = []
    for i in range(len(x_old)):
        y = np.zeros_like(x_old)
        y[i] = 1
        poly = scipy.interpolate.lagrange(x_old, y)
        V.append(np.polyval(poly, x_new))
    return np.array(V, dtype=np.float64).T


def D_interpolation(x_old: NDArray[np.float64], x_new: NDArray[np.float64]) -> NDArray[np.float64]:
    if not len(x_new):
        return np.array([], dtype=np.float64).reshape(0, len(x_old))
    # scale to [0, 1]
    x_new = (x_new - x_old[0]) / (x_old[-1] - x_old[0])
    x_old = (x_old - x_old[0]) / (x_old[-1] - x_old[0])
    D = []
    for i in range(len(x_old)):
        y = np.zeros_like(x_old)
        y[i] = 1
        poly = scipy.interpolate.lagrange(x_old, y)
        deriv_poly = np.polyder(poly)
        D.append(np.polyval(deriv_poly, x_new))
    return np.array(D, dtype=np.float64).T / (x_old[-1] - x_old[0])


class BatchIndexArray:
    def __init__(self, data: NDArray[np.float64], l_ind: NDArray[np.int32], r_ind: NDArray[np.int32]) -> None:
        super().__init__()
        if not len(l_ind) == len(r_ind):
            raise ValueError("l_ind and r_ind must have the same length")
        self._data = data
        self._l_ind = l_ind
        self._r_ind = r_ind
        self._n = len(l_ind)

    def __getitem__(self, i: int) -> NDArray[np.float64]:
        return self._data[self._l_ind[i]:self._r_ind[i]]

    def __setitem__(self, i: int, value: NDArray[np.float64]) -> None:
        self._data[self._l_ind[i]:self._r_ind[i]] = value

    def __len__(self) -> int:
        return self._n


class Variable:
    def __init__(self, phase: Phase, data: NDArray[np.float64]) -> None:
        self._data = data
        self._l_v = phase.l_v
        self._r_v = phase.r_v
        self._t_c = phase.t_c
        self._t_nc = phase.t_nc
        self._n_x = phase.n_x
        self._n = phase.n
        self._array_state = BatchIndexArray(data, self._l_v[:self._n_x], self._r_v[:self._n_x])
        self._array_control = BatchIndexArray(data, self._l_v[self._n_x:], self._r_v[self._n_x:])

        # for mesh adaption
        self._mesh = phase._mesh
        self._num_point = phase._num_point
        self._N = phase.N
        self._l_c = phase.l_c
        self._r_c = phase.r_c
        self._l_nc = phase.l_nc
        self._r_nc = phase.r_nc

    def _info_interval_c(self, t: NDArray[np.float64]):
        interval_info_c = [[] for _ in range(self._N)]
        n_old = 0
        for t_ in t:
            while self._mesh[n_old + 1] < t_:
                n_old += 1
            interval_info_c[n_old].append(t_)
        return interval_info_c

    def _info_interval_nc(self, t: NDArray[np.float64]):
        interval_info_nc = [[] for _ in range(self._N)]
        n_old = 0
        for i, t_ in enumerate(t):
            while self._mesh[n_old + 1] < t_:
                n_old += 1
            if self._mesh[n_old + 1] == t_ and i > 0 and t[i - 1] == t_ and n_old + 1 < self._N:
                n_old += 1
            interval_info_nc[n_old].append(t_)
        return interval_info_nc

    def _assemble_c(self, V_interval):
        data = []
        row = []
        col = []
        l_r = 0
        for i, (l_c, n) in enumerate(zip(self._l_c, self._num_point)):
            if not np.size(V_interval):
                continue
            data.extend(V_interval[i].flatten())
            l_r_ = V_interval[i].shape[0]
            row.extend(l_r + np.repeat(np.arange(l_r_), n))
            col.extend(l_c + np.tile(np.arange(n), l_r_))
            l_r += l_r_
        L_row = l_r
        L_col = self._r_c[-1]
        M_coo = scipy.sparse.coo_array((data, (row, col)), shape=(L_row, L_col))
        return M_coo.tocsr()

    def _assemble_nc(self, V_interval):
        return scipy.sparse.block_diag(V_interval, format='csr')

    def _guard_t(self, t: NDArray[np.float64]):
        for i in range(len(t) - 1):
            if not np.isclose(t[i], t[i + 1]) and t[i] > t[i + 1]:
                raise ValueError("t is not in ascending order")
        if t[0] < self.t_0:
            raise ValueError("t[0] must be equal or greater than t_0")
        if t[-1] > self.t_f:
            raise ValueError("t[-1] must be equal or smaller than t_f")
        return (t - self.t_0) / (self.t_f - self.t_0)

    def V_c(self, t: NDArray[np.float64]):
        t = self._guard_t(t)
        info_interval = self._info_interval_c(t)
        V_interval = [V_interpolation(self._t_c[self._l_c[i]:self._r_c[i]], np.array(t_))
                      for i, t_ in enumerate(info_interval)]
        return self._assemble_c(V_interval)

    def V_nc(self, t: NDArray[np.float64]):
        t = self._guard_t(t)
        info_interval = self._info_interval_nc(t)
        V_interval = [V_interpolation(self._t_nc[self._l_nc[i]:self._r_nc[i]], np.array(t_))
                      for i, t_ in enumerate(info_interval)]
        return self._assemble_nc(V_interval)

    def D_c(self, t: NDArray[np.float64]):
        t = self._guard_t(t)
        info_interval = self._info_interval_c(t)
        V_interval = [D_interpolation(self._t_c[self._l_c[i]:self._r_c[i]], np.array(t_))
                      for i, t_ in enumerate(info_interval)]
        return self._assemble_c(V_interval)

    def D_nc(self, t: NDArray[np.float64]):
        t = self._guard_t(t)
        info_interval = self._info_interval_nc(t)
        V_interval = [D_interpolation(self._t_nc[self._l_nc[i]:self._r_nc[i]], np.array(t_))
                      for i, t_ in enumerate(info_interval)]
        return self._assemble_nc(V_interval)

    def adapt(self, phase: Phase):
        V_c = self.V_c(phase.t_c * (self.t_f - self.t_0) + self.t_0)
        V_nc = self.V_nc(phase.t_nc * (self.t_f - self.t_0) + self.t_0)
        data_new = np.empty(phase.L)
        for n_ in range(phase.n_x):
            if phase.c_x[n_]:
                data_new[phase.l_v[n_]:phase.r_v[n_]] = V_c @ self.x[n_]
            else:
                data_new[phase.l_v[n_]:phase.r_v[n_]] = V_nc @ self.x[n_]
        for n_ in range(phase.n_u):
            if phase.c_u[n_]:
                data_new[phase.l_v[phase.n_x + n_]:phase.r_v[phase.n_x + n_]] = V_c @ self.u[n_]
            else:
                data_new[phase.l_v[phase.n_x + n_]:phase.r_v[phase.n_x + n_]] = V_nc @ self.u[n_]
        data_new[-2] = self._data[-2]
        data_new[-1] = self._data[-1]
        return Variable(phase, data_new)

    @property
    def x(self) -> BatchIndexArray:
        return self._array_state

    @property
    def u(self) -> BatchIndexArray:
        return self._array_control

    @property
    def t_0(self) -> np.float64:
        return self._data[-2]

    @t_0.setter
    def t_0(self, value: np.float64) -> None:
        self._data[-2] = value

    @property
    def t_f(self) -> np.float64:
        return self._data[-1]

    @t_f.setter
    def t_f(self, value: np.float64) -> None:
        self._data[-1] = value

    @property
    def t_c(self) -> NDArray[np.float64]:
        return self._t_c * (self.t_f - self.t_0) + self.t_0

    @property
    def t_nc(self) -> NDArray[np.float64]:
        return self._t_nc * (self.t_f - self.t_0) + self.t_0

    @property
    def data(self) -> NDArray[np.float64]:
        return self._data


def constant_guess(phase: Phase, value: float = 1.) -> Variable:
    if not phase.ok:
        raise ValueError("phase is not fully configured")
    value = float(value)
    v = Variable(phase, np.full(phase.L, value, dtype=np.float64))
    for i in range(phase.n_x):
        if isinstance(phase.bc_0[i], float):
            v.x[i][0] = phase.bc_0[i]
        elif isinstance(phase.bc_f[i], float):
            v.x[i][-1] = phase.bc_f[i]
    if isinstance(phase.t_0, float):
        v.t_0 = phase.t_0
    if isinstance(phase.t_f, float):
        v.t_f = phase.t_f
    return v


def linear_guess(phase: Phase, default: float = 1.) -> Variable:
    if not phase.ok:
        raise ValueError("phase is not fully configured")
    default = float(default)
    v = Variable(phase, np.full(phase.L, default, dtype=np.float64))
    v.t_0 = 0.
    v.t_f = 1.

    for i in range(phase.n_x):
        if isinstance(phase.bc_0[i], float) and isinstance(phase.bc_f[i], float):
            if phase.c_x[i]:
                v.x[i] = v.t_c * (phase.bc_f[i] - phase.bc_0[i]) + phase.bc_0[i]
            else:
                v.x[i] = v.t_nc * (phase.bc_f[i] - phase.bc_0[i]) + phase.bc_0[i]
        elif isinstance(phase.bc_0[i], float):
            v.x[i] = phase.bc_0[i]
        elif isinstance(phase.bc_f[i], float):
            v.x[i] = phase.bc_f[i]

    if isinstance(phase.t_0, float):
        v.t_0 = phase.t_0
    if isinstance(phase.t_f, float):
        v.t_f = phase.t_f
    return v
