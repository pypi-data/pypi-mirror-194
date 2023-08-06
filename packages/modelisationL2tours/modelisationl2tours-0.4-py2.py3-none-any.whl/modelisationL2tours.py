"""Package pour cours de modélisation L2 Tours"""
__version__ = "0.4"
from collections.abc import Iterable
from numbers import Real

import matplotlib.pyplot as plt
import numpy as np


def _recu_sequence(func, x0, times: int) -> list:
    """Return a list of the first `times` values of the recursive sequence
    defined by `func` and `x0`."""
    x = x0
    result = [x]
    for _ in range(times):
        x = func(x)
        result.append(x)
    return result


def recu_sequence(func, x0, times: int) -> list:
    """Return a list of the first `times` values of the recursive sequence
    defined by `func` and `x0`. `x0` can be an iterable or a single value."""
    if isinstance(x0, Iterable):
        return [_recu_sequence(func, x, times) for x in x0]
    else:
        return _recu_sequence(func, x0, times)


def plot_sequence_x0(
    func, x0, times: int, seq_lim=None, line: bool = True, ax = None
) -> plt.Axes:
    """Plot the first `times` values of the recursive sequence defined by `func` and `x0`.
    - `x0` can be an iterable or a single value. If this is an iterable, the function will plot
    the sequence for each value of `x0`.
    - `seq_lim` is the limit of the sequence. If not None, it will be plotted as a blue line.
    """

    sequences = recu_sequence(func, x0, times)

    if isinstance(x0, Real):
        sequences = [sequences]  # make it a list of lists
    if ax is None:
        fig, ax = plt.subplots()
    if seq_lim is not None:
        ax.plot([0, times + 1], [seq_lim, seq_lim], "r-")

    style_seq = "bx-" if line else "bx"
    for seq in sequences:
        ax.plot(seq, style_seq)

    ax.set_xlabel(r"$n$", fontsize=20)
    ax.set_ylabel(r"$u_n$", fontsize=20)
    ax.set_xlim([0, times + 1])
    return ax


def cobweb_plot(func, x0, times: int, valmax=None, ax=None) -> plt.Axes:
    seq = recu_sequence(func, x0, times)
    if valmax is None:
        valmax = 1.1 * max(seq)
    if ax is None:
        fig, ax = plt.subplots()

    doubles = np.repeat(seq, 2)
    X = np.linspace(0, valmax, 100)
    func = np.vectorize(func)
    ax.plot(X, func(X), "r-", label=r"$y=f(x)$")
    ax.plot(X, X, "b-", label=r"$y=x$")
    ax.plot(doubles[0:-1], doubles[1:], "k-", marker="o", markersize=1)

    ax.legend()
    ax.set_title(rf"$x_0 ={x0}$", fontsize=20)
    return ax


def cobweb_plots(func, x0, times: int, valmax=None, ax=None) -> list[plt.Axes]:
    """Plot the cobweb plot for each value of `x0`."""
    if isinstance(x0, Real):
        x0 = [x0]
    if ax is None:
        fig, axes = plt.subplots(x0, 1, figsize=(10, 5 * len(x0)))
    else:
        axes = ax.flatten()
        if not isinstance(axes, Iterable):
            raise ValueError(f"The fig has only one axis, but len(x0) = {len(x0)}")
        if len(axes) != len(x0):
            raise ValueError(f"len(ax) = {len(axes)} != len(x0) = {len(x0)}")

    for x, ax in zip(x0, axes):
        ax = cobweb_plot(func, x, times, valmax, ax)
    return axes


def plot_sequence_and_cobweb(
    func, x0, times: int, seq_lim=None, line: bool = True, valmax=None, AX = None
):
    if not isinstance(x0, Iterable):
        x0 = [x0]
    if AX is None:
        fig, AX = plt.subplots(figsize=(16, 8 * len(x0)), ncols=2, nrows=len(x0))
    if len(AX.flatten()) == 2:  # if AX is a 1D array
        AX = [AX]
    if len(AX) != len(x0):
        raise ValueError(f"len(AX) = {len(AX)} != len(x0) = {len(x0)}")
    for x, ax in zip(x0, AX):
        ax_seq, ax_cob = ax
        ax_seq = plot_sequence_x0(func, x, times, seq_lim, line, ax_seq)
        ax_cob = cobweb_plot(func, x, times, valmax, ax_cob)
        ax_seq.set_xlabel(r"indice $n$", fontsize=20)
        ax_cob.set_xlabel(r"suite $u_n$", fontsize=20)
        ax_cob.set_title("")
    return AX
