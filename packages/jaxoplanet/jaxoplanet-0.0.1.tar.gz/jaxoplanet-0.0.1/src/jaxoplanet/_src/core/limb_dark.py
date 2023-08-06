from functools import partial
from typing import Callable, Tuple

import jax
import jax.numpy as jnp
import numpy as np
from scipy.special import binom, roots_legendre

from jaxoplanet._src.types import Array


@partial(jax.jit, static_argnames=("order",))
def light_curve(u: Array, b: Array, r: Array, *, order: int = 10):
    g = greens_basis_transform(jnp.atleast_1d(u))
    g /= jnp.pi * (g[0] + g[1] / 1.5)
    s = solution_vector(len(g) - 1, order=order)(b, r)
    return s @ g - 1


def solution_vector(
    l_max: int, order: int = 10
) -> Callable[[Array, Array], Array]:
    n_max = l_max + 1

    @partial(jnp.vectorize, signature=f"(),()->({n_max})")
    def impl(b: Array, r: Array) -> Array:
        # TODO: Are all of these conditions necessary?
        b = jnp.abs(b)
        r = jnp.abs(r)
        area, kappa0, kappa1 = kappas(b, r)

        no_occ = jnp.greater_equal(b, 1 + r)
        full_occ = jnp.less_equal(1 + b, r)
        cond = jnp.logical_or(no_occ, full_occ)
        b_ = jnp.where(cond, 1, b)

        b2 = jnp.square(b_)
        r2 = jnp.square(r)

        s0, s2 = s0s2(b_, r, b2, r2, area, kappa0, kappa1)
        s0 = jnp.where(no_occ, jnp.pi, s0)
        s0 = jnp.where(full_occ, 0, s0)
        s2 = jnp.where(cond, 0, s2)

        P = p_integral(order, l_max, b_, r, b2, r2, kappa0)
        P = jnp.where(cond, 0, P)

        s = [s0]
        if l_max >= 1:
            s.append(-P[0] - 2 * (kappa1 - jnp.pi) / 3)
        if l_max >= 2:
            s.append(s2)
        s = jnp.stack(s)
        if l_max >= 3:
            s = jnp.concatenate((s, -P[1:]))
        return s

    return impl


def greens_basis_transform(u: Array) -> Array:
    u = jnp.append(-1, u)
    size = len(u)
    i = np.arange(size)
    arg = binom(i[None, :], i[:, None]) @ u
    p = (-1) ** (i + 1) * arg
    g = [0 for _ in range(size + 2)]
    for n in range(size - 1, 1, -1):
        g[n] = p[n] / (n + 2) + g[n + 2]
    g[1] = p[1] + 3 * g[3]
    g[0] = p[0] + 2 * g[2]
    return jnp.stack(g[:-2])


def kappas(b: Array, r: Array) -> Tuple[Array, Array, Array]:
    b2 = jnp.square(b)
    factor = (r - 1) * (r + 1)
    cond = jnp.logical_and(jnp.greater(b, jnp.abs(1 - r)), jnp.less(b, 1 + r))
    b_ = jnp.where(cond, b, 1)
    area = jnp.where(cond, kite_area(r, b_, 1), 0)
    return area, jnp.arctan2(area, b2 + factor), jnp.arctan2(area, b2 - factor)


def s0s2(
    b: Array,
    r: Array,
    b2: Array,
    r2: Array,
    area: Array,
    kappa0: Array,
    kappa1: Array,
) -> Tuple[Array, Array]:
    bpr = b + r
    onembpr2 = (1 + bpr) * (1 - bpr)
    eta2 = 0.5 * r2 * (r2 + 2 * b2)

    # Large k
    s0_lrg = jnp.pi * (1 - r2)
    s2_lrg = 2 * s0_lrg + 4 * jnp.pi * (eta2 - 0.5)

    # Small k
    Alens = kappa1 + r2 * kappa0 - area * 0.5
    s0_sml = jnp.pi - Alens
    s2_sml = 2 * s0_sml + 2 * (
        -(jnp.pi - kappa1)
        + 2 * eta2 * kappa0
        - 0.25 * area * (1 + 5 * r2 + b2)
    )

    delta = 4 * b * r
    cond = jnp.greater(onembpr2 + delta, delta)
    return jnp.where(cond, s0_lrg, s0_sml), jnp.where(cond, s2_lrg, s2_sml)


def p_integral(
    order: int,
    l_max: int,
    b: Array,
    r: Array,
    b2: Array,
    r2: Array,
    kappa0: Array,
) -> Array:
    # This is a hack for when r -> 0 or b -> 0, so k2 -> inf
    factor = 4 * b * r
    k2_cond = jnp.less(factor, 10 * jnp.finfo(factor.dtype).eps)
    factor = jnp.where(k2_cond, 1, factor)
    k2 = jnp.maximum(0, (1 - r2 - b2 + 2 * b * r) / factor)

    roots, weights = roots_legendre(order)
    rng = 0.5 * kappa0
    phi = rng * roots
    c = jnp.cos(phi + 0.5 * kappa0)
    s = jnp.sin(phi)
    s2 = jnp.square(s)

    arg = []
    if l_max >= 1:
        omz2 = jnp.maximum(0, r2 + b2 - 2 * b * r * c)
        z2 = 1 - omz2
        m = jnp.less(z2, 10 * jnp.finfo(omz2.dtype).eps)
        z2 = jnp.where(m, 1, z2)
        z3 = jnp.where(m, 0, z2 * jnp.sqrt(z2))
        cond = jnp.less(omz2, 10 * jnp.finfo(omz2.dtype).eps)
        omz2 = jnp.where(cond, 1, omz2)
        result = 2 * r * (r - b * c) * (1 - z3) / (3 * omz2)
        arg.append(jnp.where(cond, 0, result[None, :]))
    if l_max >= 3:
        f0 = jnp.maximum(0, jnp.where(k2_cond, 1 - r2, factor * (k2 - s2)))
        n = jnp.arange(3, l_max + 1)
        f = f0[None, :] ** (0.5 * n[:, None])
        f *= 2 * r * (r - b + 2 * b * s2[None, :])
        arg.append(f)

    return rng * jnp.sum(
        jnp.concatenate(arg, axis=0) * weights[None, :], axis=1
    )


def kite_area(a: Array, b: Array, c: Array) -> Array:
    def sort2(a: Array, b: Array) -> Tuple[Array, Array]:
        return jnp.minimum(a, b), jnp.maximum(a, b)

    a, b = sort2(a, b)
    b, c = sort2(b, c)
    a, b = sort2(a, b)

    square_area = (a + (b + c)) * (c - (a - b)) * (c + (a - b)) * (a + (b - c))
    cond = jnp.less(square_area, 10 * jnp.finfo(square_area.dtype).eps)
    square_area = jnp.where(cond, 1, square_area)
    return jnp.where(cond, 0, jnp.sqrt(square_area))
