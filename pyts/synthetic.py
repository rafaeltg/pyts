import collections
import numpy as np
import pandas as pd
from scipy.integrate import odeint


__all__ = ['mackey_glass', 'lorenz', 'mso']


def mackey_glass(n=1000, tau=17, delta_t=10, seed=None):

    """
    Generate the Mackey-Glass time-series.

    :param n: length of the time-series in timesteps. Default is 1000.
    :param tau: delay of the MG - system. Default is 17.
    :param delta_t: time step size
    :param seed: to seed the random generator, can be used to generate the same timeseries at each invocation.

    :return
    """

    history_len = tau * delta_t
    # Initial conditions for the history of the system
    timeseries = 1.2

    if seed is not None:
        np.random.seed(seed)

    history = collections.deque(1.2 * np.ones(history_len) + 0.2 * (np.random.rand(history_len) - 0.5))
    # Preallocate the array for the time-series
    inp = np.zeros((n, 1))

    for timestep in range(n):
        for _ in range(delta_t):
            xtau = history.popleft()
            history.append(timeseries)
            timeseries = history[-1] + (0.2 * xtau / (1.0 + xtau ** 10) - 0.1 * history[-1]) / delta_t
        inp[timestep] = timeseries

    # Squash time series through tanh
    inp = np.tanh(inp - 1)
    return pd.DataFrame({'Value': np.squeeze(inp)})


def lorenz(n=1000, sigma=10., rho=28., beta=8. / 3., dt=0.01, state0=[-13, -14, 47]):

    """
    Generates a Lorenz time-series of length n,
    with standard parameters sigma, rho and beta.

    Reference:
    Strogatz, S.: Nonlinear dynamics and chaos: with applications to physics, biology, chemistry and engineering
    (Studies in Nonlinearity)

    :param n:
    :param sigma: The sigma parameter. Default: 10.
    :param rho: The rho parameter. Default: 28.
    :param beta: The beta parameter. Default: 8/3.
    :param dt:
    :param state0: A 3-dimensional numeric vector indicating the starting point for the time series.
                   Default: c(0, 0, 0).
    :return
    """

    def f(state, t, sigma, rho, beta):
        """ The Lorenz equations. """
        x, y, z = state
        dx_dt = sigma * (y - x)
        dy_dt = x * (rho - z) - y
        dz_dt = (x * y) - (beta * z)
        return [dx_dt, dy_dt, dz_dt]

    t = np.linspace(0.0, n * dt, n)
    states = odeint(f, state0, t, args=(sigma, rho, beta))
    x, y, z = states.T

    return pd.DataFrame({"X": np.squeeze(x),
                         "Y": np.squeeze(y),
                         "Z": np.squeeze(z)})


def mso(n=1000):

    """
    Generate the Multiple Sinewave Oscillator time-series, a sum of two sines
    with incommensurable periods. Parameters are:
    :param n: length of the time-series in timesteps
    """

    phase = np.random.rand()
    x = np.atleast_2d(np.arange(n)).T
    return np.sin(0.2 * x + phase) + np.sin(0.311 * x + phase)
