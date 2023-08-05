import numpy as np
import pytest

from openoc.system import System
from openoc.variable import BatchIndexArray, Variable


def test_batch_index_array():
    data = np.arange(10)
    l_ind = np.array([0, 1, 3, 6])
    r_ind = np.array([1, 3, 6, 10])
    batch_index_array = BatchIndexArray(data, l_ind, r_ind)
    assert np.allclose(batch_index_array[0], [0])
    assert np.allclose(batch_index_array[1], [1, 2])
    assert np.allclose(batch_index_array[2], [3, 4, 5])
    assert np.allclose(batch_index_array[3], [6, 7, 8, 9])
    with pytest.raises(IndexError):
        _ = batch_index_array[4]
    assert len(batch_index_array) == 4


def test_variable_interpolation():
    s = System(0)
    p = s.new_phase(2, 2)
    p.set_dynamics([0, 0]).set_boundary_condition([0, 0], [0, 0], 0, 10) \
        .set_discretization(10, 10, [True, False], [False, True])
    v = Variable(p, np.zeros(p.L))
    v.t_f = 10
    t = np.linspace(0, 10, 101, endpoint=True)

    v.x[0] = np.sin(v.t_c)
    V_c = v.V_c(t)
    assert np.allclose(np.sin(t), V_c @ v.x[0])
    D_c = v.D_c(t)
    assert np.allclose(np.cos(t), D_c @ v.x[0])

    v.x[1] = np.cos(v.t_nc)
    V_nc = v.V_nc(t)
    assert np.allclose(np.cos(t), V_nc @ v.x[1])
    D_nc = v.D_nc(t)
    assert np.allclose(- np.sin(t), D_nc @ v.x[1])
