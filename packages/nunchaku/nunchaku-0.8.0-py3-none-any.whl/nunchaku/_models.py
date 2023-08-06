#!/usr/bin/env python3
from sympy import (
    IndexedBase,
    log,
    Sum,
    Indexed,
    lambdify,
    gamma,
    simplify,
    hessian,
    symbols,
    Symbol,
    pi,
    diff,
    exp,
    sqrt,
)


def mc_t():
    """returns functions of the negative log evidence, hessian and jacobian of the y=mx+c model,
    assuming sigma is unknown but constant over x.

    Parameters
    ----------
    intercept : bool
        if False, force c = 0.

    """
    m, N, j, c = symbols("m N j c")
    y = IndexedBase("y")
    x = IndexedBase("x")
    stirling = (
        1 / 2 * log(2 * pi * (N / 2 - 1))
        + (N / 2 - 1) * log(N / 2 - 1)
        - (N / 2 - 1)
        + log(1 + 1 / (12 * (N / 2 - 1)) + 1 / (288 * (N / 2 - 1) ** 2))
    )
    logZ = stirling - log(2) - (N / 2) * log(pi)
    model = m * Indexed(x, j) + c
    theta = (m, c)
    logL = (-N / 2) * log(Sum((Indexed(y, j) - model) ** 2, (j, 0, N - 1)))
    arg_list = (theta, x, y, N)
    neglogL = lambdify(arg_list, -(logL + logZ), modules=["numpy"])
    hess = lambdify(
        arg_list, hessian(-logL, theta), modules=["numpy"]
    )  # No need to add logZ
    # jac = lambdify(arg_list, Matrix([-logL]).jacobian(theta))
    jac = lambdify(arg_list, [diff(-logL, v) for v in theta], modules=["numpy"])
    return neglogL, hess, jac


def mc():
    """returns functions of the negative log evidence of the y=mx+c model assuming known sigma.

    Parameters
    ----------
    intercept : bool
        if False, force c = 0.

    """
    # Define symbols
    x = IndexedBase("x")
    y = IndexedBase("y")
    sig = IndexedBase("\sigma")
    j = Symbol("j")
    N = Symbol("N")
    arg_list = (x, y, sig, N)
    # Define T's
    T1 = Sum(Indexed(y, j) ** 2 / 2 / Indexed(sig, j) ** 2, (j, 0, N - 1))
    T2 = Sum(Indexed(x, j) ** 2 / 2 / Indexed(sig, j) ** 2, (j, 0, N - 1))
    T3 = Sum(1 / 2 / Indexed(sig, j) ** 2, (j, 0, N - 1))
    T4 = Sum(Indexed(y, j) / Indexed(sig, j) ** 2, (j, 0, N - 1))
    T5 = Sum(Indexed(x, j) * Indexed(y, j) / Indexed(sig, j) ** 2, (j, 0, N - 1))
    T6 = Sum(Indexed(x, j) / Indexed(sig, j) ** 2, (j, 0, N - 1))
    # Log likelihood
    logl = (
        (1 - N / 2) * log(2 * pi)
        - Sum(log(Indexed(sig, j)), (j, 0, N - 1))
        - 1 / 2 * (log(4 * T2 * T3 - T6**2))
        + (-T1 + (T2 * T4**2 + T3 * T5**2 - T4 * T5 * T6) / (4 * T2 * T3 - T6**2))
    )
    return lambdify(arg_list, logl, modules=["numpy"])


def mc_entropy():
    x = IndexedBase("x")
    y = IndexedBase("y")
    sig = IndexedBase("\sigma")
    j = Symbol("j")
    N = Symbol("N")
    Z = Symbol("Z")
    arg_list = (x, y, sig, N, Z)
    # Define T's
    T1 = Sum(Indexed(y, j) ** 2 / 2 / Indexed(sig, j) ** 2, (j, 0, N - 1))
    T2 = Sum(Indexed(x, j) ** 2 / 2 / Indexed(sig, j) ** 2, (j, 0, N - 1))
    T3 = Sum(1 / 2 / Indexed(sig, j) ** 2, (j, 0, N - 1))
    T4 = Sum(Indexed(y, j) / Indexed(sig, j) ** 2, (j, 0, N - 1))
    T5 = Sum(Indexed(x, j) * Indexed(y, j) / Indexed(sig, j) ** 2, (j, 0, N - 1))
    T6 = Sum(Indexed(x, j) / Indexed(sig, j) ** 2, (j, 0, N - 1))
    # Z is the evidence
    logA = -Z + (-N / 2) * log(2 * pi) - Sum(log(Indexed(sig, j)), (j, 0, N - 1))
    int_plogp = (
        2
        * pi
        * (
            -16 * T1 * T2**2 * T3**2
            + 8 * T1 * T2 * T3 * T6**2
            - T1 * T6**4
            - 16 * T2**2 * T3**2
            + 4 * T2**2 * T3 * T4**2
            + 4 * T2 * T3**2 * T5**2
            - 4 * T2 * T3 * T4 * T5 * T6
            + 8 * T2 * T3 * T6**2
            - T2 * T4**2 * T6**2
            - T3 * T5**2 * T6**2
            + T4 * T5 * T6**3
            - T6**4
        )
        * exp(
            (
                -4 * T1 * T2 * T3
                + T1 * T6**2
                + T2 * T4**2
                + T3 * T5**2
                - T4 * T5 * T6
            )
            / (4 * T2 * T3 - T6**2)
        )
        / (
            sqrt(T2)
            * sqrt(T3)
            * sqrt((4 * T2 * T3 - T6**2) / (T2 * T3))
            * (16 * T2**2 * T3**2 - 8 * T2 * T3 * T6**2 + T6**4)
        )
    )
    # P = Z * exp
    # P * logP = A * exp * log(A * exp) = A * exp * (logA + log exp)
    # int(P * logP) = logA * int(A * exp) + A * int(exp * log exp)
    entropy = - (logA + exp(logA) * int_plogp)
    return lambdify(arg_list, entropy, modules=["numpy"])
