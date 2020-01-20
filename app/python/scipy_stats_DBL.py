from __future__ import division, print_function, absolute_import

import warnings
import sys
import math
if sys.version_info.major >= 3 and sys.version_info.minor >= 5:
    from math import gcd
else:
    from fractions import gcd
from collections import namedtuple

import numpy as np
from numpy import asarray

from scipy._lib.six import callable, string_types
import scipy.special as special


def _compute_prob_outside_square(n, h):
    """Compute the proportion of paths that pass outside the two diagonal lines.

    Parameters
    ----------
    n : integer
        n > 0
    h : integer
        0 <= h <= n

    Returns
    -------
    p : float
        The proportion of paths that pass outside the lines x-y = +/-h.

    """
    # Compute Pr(D_{n,n} >= h/n)
    # Prob = 2 * ( binom(2n, n-h) - binom(2n, n-2a) + binom(2n, n-3a) - ... )  / binom(2n, n)
    # This formulation exhibits subtractive cancellation.
    # Instead divide each term by binom(2n, n), then factor common terms
    # and use a Horner-like algorithm
    # P = 2 * A0 * (1 - A1*(1 - A2*(1 - A3*(1 - A4*(...)))))

    P = 0.0
    k = int(np.floor(n / h))
    while k >= 0:
        p1 = 1.0
        # Each of the Ai terms has numerator and denominator with h simple terms.
        for j in range(h):
            p1 = (n - k * h - j) * p1 / (n + k * h + j + 1)
        P = p1 * (1.0 - P)
        k -= 1
    return 2 * P

def _compute_prob_inside_method(m, n, g, h):
    """Count the proportion of paths that stay strictly inside two diagonal lines.

    Parameters
    ----------
    m : integer
        m > 0
    n : integer
        n > 0
    g : integer
        g is greatest common divisor of m and n
    h : integer
        0 <= h <= lcm(m,n)

    Returns
    -------
    p : float
        The proportion of paths that stay inside the two lines.


    Count the integer lattice paths from (0, 0) to (m, n) which satisfy
    |x/m - y/n| < h / lcm(m, n).
    The paths make steps of size +1 in either positive x or positive y directions.

    We generally follow Hodges' treatment of Drion/Gnedenko/Korolyuk.
    Hodges, J.L. Jr.,
    "The Significance Probability of the Smirnov Two-Sample Test,"
    Arkiv fiur Matematik, 3, No. 43 (1958), 469-86.
    """
    # Probability is symmetrical in m, n.  Computation below uses m >= n.
    if m < n:
        m, n = n, m
    mg = m // g
    ng = n // g

    # Count the integer lattice paths from (0, 0) to (m, n) which satisfy
    # |nx/g - my/g| < h.
    # Compute matrix A such that:
    #  A(x, 0) = A(0, y) = 1
    #  A(x, y) = A(x, y-1) + A(x-1, y), for x,y>=1, except that
    #  A(x, y) = 0 if |x/m - y/n|>= h
    # Probability is A(m, n)/binom(m+n, n)
    # Optimizations exist for m==n, m==n*p.
    # Only need to preserve a single column of A, and only a sliding window of it.
    # minj keeps track of the slide.
    minj, maxj = 0, min(int(np.ceil(h / mg)), n + 1)
    curlen = maxj - minj
    # Make a vector long enough to hold maximum window needed.
    lenA = min(2 * maxj + 2, n + 1)
    # This is an integer calculation, but the entries are essentially
    # binomial coefficients, hence grow quickly.
    # Scaling after each column is computed avoids dividing by a
    # large binomial coefficent at the end. Instead it is incorporated
    # one factor at a time during the computation.
    dtype = np.float64
    A = np.zeros(lenA, dtype=dtype)
    # Initialize the first column
    A[minj:maxj] = 1
    for i in range(1, m + 1):
        # Generate the next column.
        # First calculate the sliding window
        lastminj, lastmaxj, lastlen = minj, maxj, curlen
        minj = max(int(np.floor((ng * i - h) / mg)) + 1, 0)
        minj = min(minj, n)
        maxj = min(int(np.ceil((ng * i + h) / mg)), n + 1)
        if maxj <= minj:
            return 0
        # Now fill in the values
        A[0:maxj - minj] = np.cumsum(A[minj - lastminj:maxj - lastminj])
        curlen = maxj - minj
        if lastlen > curlen:
            # Set some carried-over elements to 0
            A[maxj - minj:maxj - minj + (lastlen - curlen)] = 0
        # Peel off one term from each of top and bottom of the binomial coefficient.
        scaling_factor = i * 1.0 / (n + i)
        A *= scaling_factor
    return A[maxj - minj - 1]

def _count_paths_outside_method(m, n, g, h):
    """Count the number of paths that pass outside the specified diagonal.

    Parameters
    ----------
    m : integer
        m > 0
    n : integer
        n > 0
    g : integer
        g is greatest common divisor of m and n
    h : integer
        0 <= h <= lcm(m,n)

    Returns
    -------
    p : float
        The number of paths that go low.
        The calculation may overflow - check for a finite answer.

    Exceptions
    ----------
    FloatingPointError: Raised if the intermediate computation goes outside
    the range of a float.

    Notes
    -----
    Count the integer lattice paths from (0, 0) to (m, n), which at some
    point (x, y) along the path, satisfy:
      m*y <= n*x - h*g
    The paths make steps of size +1 in either positive x or positive y directions.

    We generally follow Hodges' treatment of Drion/Gnedenko/Korolyuk.
    Hodges, J.L. Jr.,
    "The Significance Probability of the Smirnov Two-Sample Test,"
    Arkiv fiur Matematik, 3, No. 43 (1958), 469-86.
    """
    # Compute #paths which stay lower than x/m-y/n = h/lcm(m,n)
    # B(x, y) = #{paths from (0,0) to (x,y) without previously crossing the boundary}
    #         = binom(x, y) - #{paths which already reached the boundary}
    # Multiply by the number of path extensions going from (x, y) to (m, n)
    # Sum.

    # Probability is symmetrical in m, n.  Computation below assumes m >= n.
    if m < n:
        m, n = n, m
    mg = m // g
    ng = n // g

    #  0 <= x_j <= m is the smallest integer for which n*x_j - m*j < g*h
    xj = [int(np.ceil((h + mg * j)/ng)) for j in range(n+1)]
    xj = [_ for _ in xj if _ <= m]
    lxj = len(xj)
    # B is an array just holding a few values of B(x,y), the ones needed.
    # B[j] == B(x_j, j)
    if lxj == 0:
        return np.round(special.binom(m + n, n))
    B = np.zeros(lxj)
    B[0] = 1
    # Compute the B(x, y) terms
    # The binomial coefficient is an integer, but special.binom() may return a float.
    # Round it to the nearest integer.
    for j in range(1, lxj):
        Bj = np.round(special.binom(xj[j] + j, j))
        if not np.isfinite(Bj):
            raise FloatingPointError()
        for i in range(j):
            bin = np.round(special.binom(xj[j] - xj[i] + j - i, j-i))
            dec = bin * B[i]
            Bj -= dec
        B[j] = Bj
        if not np.isfinite(Bj):
            raise FloatingPointError()
    # Compute the number of path extensions...
    num_paths = 0
    for j in range(lxj):
        bin = np.round(special.binom((m-xj[j]) + (n - j), n-j))
        term = B[j] * bin
        if not np.isfinite(term):
            raise FloatingPointError()
        num_paths += term
    return np.round(num_paths)


def ks_2samp(data1, data2, alternative='two-sided'):
    mode = 'exact'
    original_mode = 'exact'
    data1 = np.sort(data1)
    data2 = np.sort(data2)
    n1 = data1.shape[0]
    n2 = data2.shape[0]
    if min(n1, n2) == 0:
        raise ValueError('Data passed to ks_2samp must not be empty')

    data_all = np.concatenate([data1, data2])
    # using searchsorted solves equal data problem
    cdf1 = np.searchsorted(data1, data_all, side='right') / n1
    cdf2 = np.searchsorted(data2, data_all, side='right') / n2
    cddiffs = cdf1 - cdf2
    minS = -np.min(cddiffs)
    maxS = np.max(cddiffs)
    alt2Dvalue = {'less': minS, 'greater': maxS, 'two-sided': max(minS, maxS)}
    d = alt2Dvalue[alternative]
    g = gcd(n1, n2)
    n1g = n1 // g
    n2g = n2 // g
    prob = -np.inf
    # If lcm(n1, n2) is too big, switch from exact to asymp
    if n1g >= np.iinfo(np.int).max / n2g:
        mode = 'asymp'
        warnings.warn(
            "Exact ks_2samp calculation not possible with samples sizes "
            "%d and %d. Switching to 'asymp' " % (n1, n2), RuntimeWarning)

    saw_fp_error = False
    lcm = (n1 // g) * n2
    h = int(np.round(d * lcm))
    d = h * 1.0 / lcm
    if h == 0:
        prob = 1.0
    else:
        try:
            if alternative == 'two-sided':
                if n1 == n2:
                    prob = _compute_prob_outside_square(n1, h)
                else:
                    prob = 1 - _compute_prob_inside_method(n1, n2, g, h)
            else:
                if n1 == n2:
                    # prob = binom(2n, n-h) / binom(2n, n)
                    # Evaluating in that form incurs roundoff errors
                    # from special.binom. Instead calculate directly
                    prob = 1.0
                    for j in range(h):
                        prob = (n1 - j) * prob / (n1 + j + 1)
                else:
                    num_paths = _count_paths_outside_method(n1, n2, g, h)
                    bin = special.binom(n1 + n2, n1)
                    if not np.isfinite(bin) or not np.isfinite(num_paths) or num_paths > bin:
                        raise FloatingPointError()
                    prob = num_paths / bin

        except FloatingPointError:
            # Switch mode
            mode = 'asymp'
            saw_fp_error = True
            # Can't raise warning here, inside the try
        finally:
            if saw_fp_error:
                if original_mode == 'exact':
                    warnings.warn("ks_2samp: Exact calculation overflowed. Switching to mode=%s" % mode, RuntimeWarning)
            else:
                if prob > 1 or prob < 0:
                    mode = 'asymp'
                    if original_mode == 'exact':
                        warnings.warn("ks_2samp: Exact calculation incurred large rounding error. Switching to mode=%s" % mode, RuntimeWarning)

    prob = (0 if prob < 0 else (1 if prob > 1 else prob))
    # return Ks_2sampResult(d, prob)
    return d, prob


if __name__ == "__main__":
    ### single example
    # fg = list(range(0, 40, 2))
    # bg = list(range(1, 100, 2))
    # print(ks_2samp(fg, bg, alternative='two-sided'))

    ### many tests for profiling
    for i in range(1000): # 1k repeated tests
        vals_in_fg = np.random.randint(200, 5000)
        vals_in_bg = np.random.randint(20000)
        fg = np.random.randint(0, 5000000, vals_in_fg) # value between 1 and 5e6 (Lars' scores scaled by 1e6), number of values in fg
        bg = np.random.randint(0, 5000000, vals_in_bg)  # value between 1 and 5e6 (Lars' scores scaled by 1e6), number of values in fg
        ks_2samp(fg, bg, alternative='two-sided')
