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
# from numpy import array, asarray, ma
from numpy import asarray

from scipy._lib.six import callable, string_types
# from scipy._lib._version import NumpyVersion
# from scipy._lib._util import _lazywhere
import scipy.special as special
# from scipy import linalg





# try:
#     # is it python 3.3 or higher?
#     inspect.signature
#
#     # Apparently, yes. Wrap inspect.signature
#
#     ArgSpec = namedtuple('ArgSpec', ['args', 'varargs', 'keywords', 'defaults'])
#
#     def getargspec_no_self(func):
#         """inspect.getargspec replacement using inspect.signature.
#
#         inspect.getargspec is deprecated in python 3. This is a replacement
#         based on the (new in python 3.3) `inspect.signature`.
#
#         Parameters
#         ----------
#         func : callable
#             A callable to inspect
#
#         Returns
#         -------
#         argspec : ArgSpec(args, varargs, varkw, defaults)
#             This is similar to the result of inspect.getargspec(func) under
#             python 2.x.
#             NOTE: if the first argument of `func` is self, it is *not*, I repeat
#             *not* included in argspec.args.
#             This is done for consistency between inspect.getargspec() under
#             python 2.x, and inspect.signature() under python 3.x.
#         """
#         sig = inspect.signature(func)
#         args = [
#             p.name for p in sig.parameters.values()
#             if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
#         ]
#         varargs = [
#             p.name for p in sig.parameters.values()
#             if p.kind == inspect.Parameter.VAR_POSITIONAL
#         ]
#         varargs = varargs[0] if varargs else None
#         varkw = [
#             p.name for p in sig.parameters.values()
#             if p.kind == inspect.Parameter.VAR_KEYWORD
#         ]
#         varkw = varkw[0] if varkw else None
#         defaults = [
#             p.default for p in sig.parameters.values()
#             if (p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD and
#                p.default is not p.empty)
#         ] or None
#         return ArgSpec(args, varargs, varkw, defaults)
#
# except AttributeError:
#     # python 2.x
#     def getargspec_no_self(func):
#         """inspect.getargspec replacement for compatibility with python 3.x.
#
#         inspect.getargspec is deprecated in python 3. This wraps it, and
#         *removes* `self` from the argument list of `func`, if present.
#         This is done for forward compatibility with python 3.
#
#         Parameters
#         ----------
#         func : callable
#             A callable to inspect
#
#         Returns
#         -------
#         argspec : ArgSpec(args, varargs, varkw, defaults)
#             This is similar to the result of inspect.getargspec(func) under
#             python 2.x.
#             NOTE: if the first argument of `func` is self, it is *not*, I repeat
#             *not* included in argspec.args.
#             This is done for consistency between inspect.getargspec() under
#             python 2.x, and inspect.signature() under python 3.x.
#         """
#         argspec = inspect.getargspec(func)
#         if argspec.args[0] == 'self':
#             argspec.args.pop(0)
#         return argspec


# class rv_generic(object):
#     """Class which encapsulates common functionality between rv_discrete
#     and rv_continuous.
#
#     """
#     def __init__(self, seed=None):
#         super(rv_generic, self).__init__()
#
#         # figure out if _stats signature has 'moments' keyword
#         # sign = _getargspec(self._stats)
#         # self._stats_has_moments = ((sign[2] is not None) or
#         #                            ('moments' in sign[0]))
#         # self._random_state = check_random_state(seed)
#
#     @property
#     def random_state(self):
#         """ Get or set the RandomState object for generating random variates.
#
#         This can be either None or an existing RandomState object.
#
#         If None (or np.random), use the RandomState singleton used by np.random.
#         If already a RandomState instance, use it.
#         If an int, use a new RandomState instance seeded with seed.
#
#         """
#         return self._random_state
#
#     @random_state.setter
#     def random_state(self, seed):
#         self._random_state = check_random_state(seed)
#
#     def __getstate__(self):
#         return self._updated_ctor_param(), self._random_state
#
#     def __setstate__(self, state):
#         ctor_param, r = state
#         self.__init__(**ctor_param)
#         self._random_state = r
#         return self
#
#     def _construct_argparser(
#             self, meths_to_inspect, locscale_in, locscale_out):
#         """Construct the parser for the shape arguments.
#
#         Generates the argument-parsing functions dynamically and attaches
#         them to the instance.
#         Is supposed to be called in __init__ of a class for each distribution.
#
#         If self.shapes is a non-empty string, interprets it as a
#         comma-separated list of shape parameters.
#
#         Otherwise inspects the call signatures of `meths_to_inspect`
#         and constructs the argument-parsing functions from these.
#         In this case also sets `shapes` and `numargs`.
#         """
#
#         if self.shapes:
#             # sanitize the user-supplied shapes
#             if not isinstance(self.shapes, string_types):
#                 raise TypeError('shapes must be a string.')
#
#             shapes = self.shapes.replace(',', ' ').split()
#
#             for field in shapes:
#                 if keyword.iskeyword(field):
#                     raise SyntaxError('keywords cannot be used as shapes.')
#                 if not re.match('^[_a-zA-Z][_a-zA-Z0-9]*$', field):
#                     raise SyntaxError(
#                         'shapes must be valid python identifiers')
#         else:
#             # find out the call signatures (_pdf, _cdf etc), deduce shape
#             # arguments. Generic methods only have 'self, x', any further args
#             # are shapes.
#             shapes_list = []
#             for meth in meths_to_inspect:
#                 shapes_args = _getargspec(meth)   # NB: does not contain self
#                 args = shapes_args.args[1:]       # peel off 'x', too
#
#                 if args:
#                     shapes_list.append(args)
#
#                     # *args or **kwargs are not allowed w/automatic shapes
#                     if shapes_args.varargs is not None:
#                         raise TypeError(
#                             '*args are not allowed w/out explicit shapes')
#                     if shapes_args.keywords is not None:
#                         raise TypeError(
#                             '**kwds are not allowed w/out explicit shapes')
#                     if shapes_args.defaults is not None:
#                         raise TypeError('defaults are not allowed for shapes')
#
#             if shapes_list:
#                 shapes = shapes_list[0]
#
#                 # make sure the signatures are consistent
#                 for item in shapes_list:
#                     if item != shapes:
#                         raise TypeError('Shape arguments are inconsistent.')
#             else:
#                 shapes = []
#
#         # have the arguments, construct the method from template
#         shapes_str = ', '.join(shapes) + ', ' if shapes else ''  # NB: not None
#         dct = dict(shape_arg_str=shapes_str,
#                    locscale_in=locscale_in,
#                    locscale_out=locscale_out,
#                    )
#         ns = {}
#         exec_(parse_arg_template % dct, ns)
#         # NB: attach to the instance, not class
#         for name in ['_parse_args', '_parse_args_stats', '_parse_args_rvs']:
#             setattr(self, name,
#                     instancemethod(ns[name], self, self.__class__)
#                     )
#
#         self.shapes = ', '.join(shapes) if shapes else None
#         if not hasattr(self, 'numargs'):
#             # allows more general subclassing with *args
#             self.numargs = len(shapes)
#
#     def _construct_doc(self, docdict, shapes_vals=None):
#         """Construct the instance docstring with string substitutions."""
#         tempdict = docdict.copy()
#         tempdict['name'] = self.name or 'distname'
#         tempdict['shapes'] = self.shapes or ''
#
#         if shapes_vals is None:
#             shapes_vals = ()
#         vals = ', '.join('%.3g' % val for val in shapes_vals)
#         tempdict['vals'] = vals
#
#         tempdict['shapes_'] = self.shapes or ''
#         if self.shapes and self.numargs == 1:
#             tempdict['shapes_'] += ','
#
#         if self.shapes:
#             tempdict['set_vals_stmt'] = '>>> %s = %s' % (self.shapes, vals)
#         else:
#             tempdict['set_vals_stmt'] = ''
#
#         if self.shapes is None:
#             # remove shapes from call parameters if there are none
#             for item in ['default', 'before_notes']:
#                 tempdict[item] = tempdict[item].replace(
#                     "\n%(shapes)s : array_like\n    shape parameters", "")
#         for i in range(2):
#             if self.shapes is None:
#                 # necessary because we use %(shapes)s in two forms (w w/o ", ")
#                 self.__doc__ = self.__doc__.replace("%(shapes)s, ", "")
#             try:
#                 self.__doc__ = doccer.docformat(self.__doc__, tempdict)
#             except TypeError as e:
#                 raise Exception("Unable to construct docstring for distribution \"%s\": %s" % (self.name, repr(e)))
#
#         # correct for empty shapes
#         self.__doc__ = self.__doc__.replace('(, ', '(').replace(', )', ')')
#
#     def _construct_default_doc(self, longname=None, extradoc=None,
#                                docdict=None, discrete='continuous'):
#         """Construct instance docstring from the default template."""
#         if longname is None:
#             longname = 'A'
#         if extradoc is None:
#             extradoc = ''
#         if extradoc.startswith('\n\n'):
#             extradoc = extradoc[2:]
#         self.__doc__ = ''.join(['%s %s random variable.' % (longname, discrete),
#                                 '\n\n%(before_notes)s\n', docheaders['notes'],
#                                 extradoc, '\n%(example)s'])
#         self._construct_doc(docdict)
#
#     def freeze(self, *args, **kwds):
#         """Freeze the distribution for the given arguments.
#
#         Parameters
#         ----------
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution.  Should include all
#             the non-optional arguments, may include ``loc`` and ``scale``.
#
#         Returns
#         -------
#         rv_frozen : rv_frozen instance
#             The frozen distribution.
#
#         """
#         return rv_frozen(self, *args, **kwds)
#
#     def __call__(self, *args, **kwds):
#         return self.freeze(*args, **kwds)
#     __call__.__doc__ = freeze.__doc__
#
#     # The actual calculation functions (no basic checking need be done)
#     # If these are defined, the others won't be looked at.
#     # Otherwise, the other set can be defined.
#     def _stats(self, *args, **kwds):
#         return None, None, None, None
#
#     #  Central moments
#     def _munp(self, n, *args):
#         # Silence floating point warnings from integration.
#         olderr = np.seterr(all='ignore')
#         vals = self.generic_moment(n, *args)
#         np.seterr(**olderr)
#         return vals
#
#     def _argcheck_rvs(self, *args, **kwargs):
#         # Handle broadcasting and size validation of the rvs method.
#         # Subclasses should not have to override this method.
#         # The rule is that if `size` is not None, then `size` gives the
#         # shape of the result (integer values of `size` are treated as
#         # tuples with length 1; i.e. `size=3` is the same as `size=(3,)`.)
#         #
#         # `args` is expected to contain the shape parameters (if any), the
#         # location and the scale in a flat tuple (e.g. if there are two
#         # shape parameters `a` and `b`, `args` will be `(a, b, loc, scale)`).
#         # The only keyword argument expected is 'size'.
#         size = kwargs.get('size', None)
#         all_bcast = np.broadcast_arrays(*args)
#
#         def squeeze_left(a):
#             while a.ndim > 0 and a.shape[0] == 1:
#                 a = a[0]
#             return a
#
#         # Eliminate trivial leading dimensions.  In the convention
#         # used by numpy's random variate generators, trivial leading
#         # dimensions are effectively ignored.  In other words, when `size`
#         # is given, trivial leading dimensions of the broadcast parameters
#         # in excess of the number of dimensions  in size are ignored, e.g.
#         #   >>> np.random.normal([[1, 3, 5]], [[[[0.01]]]], size=3)
#         #   array([ 1.00104267,  3.00422496,  4.99799278])
#         # If `size` is not given, the exact broadcast shape is preserved:
#         #   >>> np.random.normal([[1, 3, 5]], [[[[0.01]]]])
#         #   array([[[[ 1.00862899,  3.00061431,  4.99867122]]]])
#         #
#         all_bcast = [squeeze_left(a) for a in all_bcast]
#         bcast_shape = all_bcast[0].shape
#         bcast_ndim = all_bcast[0].ndim
#
#         if size is None:
#             size_ = bcast_shape
#         else:
#             size_ = tuple(np.atleast_1d(size))
#
#         # Check compatibility of size_ with the broadcast shape of all
#         # the parameters.  This check is intended to be consistent with
#         # how the numpy random variate generators (e.g. np.random.normal,
#         # np.random.beta) handle their arguments.   The rule is that, if size
#         # is given, it determines the shape of the output.  Broadcasting
#         # can't change the output size.
#
#         # This is the standard broadcasting convention of extending the
#         # shape with fewer dimensions with enough dimensions of length 1
#         # so that the two shapes have the same number of dimensions.
#         ndiff = bcast_ndim - len(size_)
#         if ndiff < 0:
#             bcast_shape = (1,)*(-ndiff) + bcast_shape
#         elif ndiff > 0:
#             size_ = (1,)*ndiff + size_
#
#         # This compatibility test is not standard.  In "regular" broadcasting,
#         # two shapes are compatible if for each dimension, the lengths are the
#         # same or one of the lengths is 1.  Here, the length of a dimension in
#         # size_ must not be less than the corresponding length in bcast_shape.
#         ok = all([bcdim == 1 or bcdim == szdim
#                   for (bcdim, szdim) in zip(bcast_shape, size_)])
#         if not ok:
#             raise ValueError("size does not match the broadcast shape of "
#                              "the parameters.")
#
#         param_bcast = all_bcast[:-2]
#         loc_bcast = all_bcast[-2]
#         scale_bcast = all_bcast[-1]
#
#         return param_bcast, loc_bcast, scale_bcast, size_
#
#     ## These are the methods you must define (standard form functions)
#     ## NB: generic _pdf, _logpdf, _cdf are different for
#     ## rv_continuous and rv_discrete hence are defined in there
#     def _argcheck(self, *args):
#         """Default check for correct values on args and keywords.
#
#         Returns condition array of 1's where arguments are correct and
#          0's where they are not.
#
#         """
#         cond = 1
#         for arg in args:
#             cond = logical_and(cond, (asarray(arg) > 0))
#         return cond
#
#     def _get_support(self, *args):
#         """Return the support of the (unscaled, unshifted) distribution.
#
#         *Must* be overridden by distributions which have support dependent
#         upon the shape parameters of the distribution.  Any such override
#         *must not* set or change any of the class members, as these members
#         are shared amongst all instances of the distribution.
#
#         Parameters
#         ----------
#         arg1, arg2, ... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information).
#         Returns
#         -------
#         a, b : numeric (float, or int or +/-np.inf)
#             end-points of the distribution's support for the specified
#             shape parameters.
#         """
#         return self.a, self.b
#
#     def _support_mask(self, x, *args):
#         a, b = self._get_support(*args)
#         return (a <= x) & (x <= b)
#
#     def _open_support_mask(self, x, *args):
#         a, b = self._get_support(*args)
#         return (a < x) & (x < b)
#
#     def _rvs(self, *args):
#         # This method must handle self._size being a tuple, and it must
#         # properly broadcast *args and self._size.  self._size might be
#         # an empty tuple, which means a scalar random variate is to be
#         # generated.
#
#         ## Use basic inverse cdf algorithm for RV generation as default.
#         U = self._random_state.random_sample(self._size)
#         Y = self._ppf(U, *args)
#         return Y
#
#     def _logcdf(self, x, *args):
#         return log(self._cdf(x, *args))
#
#     def _sf(self, x, *args):
#         return 1.0-self._cdf(x, *args)
#
#     def _logsf(self, x, *args):
#         return log(self._sf(x, *args))
#
#     def _ppf(self, q, *args):
#         return self._ppfvec(q, *args)
#
#     def _isf(self, q, *args):
#         return self._ppf(1.0-q, *args)  # use correct _ppf for subclasses
#
#     # These are actually called, and should not be overwritten if you
#     # want to keep error checking.
#     def rvs(self, *args, **kwds):
#         """
#         Random variates of given type.
#
#         Parameters
#         ----------
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information).
#         loc : array_like, optional
#             Location parameter (default=0).
#         scale : array_like, optional
#             Scale parameter (default=1).
#         size : int or tuple of ints, optional
#             Defining number of random variates (default is 1).
#         random_state : None or int or ``np.random.RandomState`` instance, optional
#             If int or RandomState, use it for drawing the random variates.
#             If None, rely on ``self.random_state``.
#             Default is None.
#
#         Returns
#         -------
#         rvs : ndarray or scalar
#             Random variates of given `size`.
#
#         """
#         discrete = kwds.pop('discrete', None)
#         rndm = kwds.pop('random_state', None)
#         args, loc, scale, size = self._parse_args_rvs(*args, **kwds)
#         cond = logical_and(self._argcheck(*args), (scale >= 0))
#         if not np.all(cond):
#             raise ValueError("Domain error in arguments.")
#
#         if np.all(scale == 0):
#             return loc*ones(size, 'd')
#
#         # extra gymnastics needed for a custom random_state
#         if rndm is not None:
#             random_state_saved = self._random_state
#             self._random_state = check_random_state(rndm)
#
#         # `size` should just be an argument to _rvs(), but for, um,
#         # historical reasons, it is made an attribute that is read
#         # by _rvs().
#         self._size = size
#         vals = self._rvs(*args)
#
#         vals = vals * scale + loc
#
#         # do not forget to restore the _random_state
#         if rndm is not None:
#             self._random_state = random_state_saved
#
#         # Cast to int if discrete
#         if discrete:
#             if size == ():
#                 vals = int(vals)
#             else:
#                 vals = vals.astype(int)
#
#         return vals
#
#     def stats(self, *args, **kwds):
#         """
#         Some statistics of the given RV.
#
#         Parameters
#         ----------
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional (continuous RVs only)
#             scale parameter (default=1)
#         moments : str, optional
#             composed of letters ['mvsk'] defining which moments to compute:
#             'm' = mean,
#             'v' = variance,
#             's' = (Fisher's) skew,
#             'k' = (Fisher's) kurtosis.
#             (default is 'mv')
#
#         Returns
#         -------
#         stats : sequence
#             of requested moments.
#
#         """
#         args, loc, scale, moments = self._parse_args_stats(*args, **kwds)
#         # scale = 1 by construction for discrete RVs
#         loc, scale = map(asarray, (loc, scale))
#         args = tuple(map(asarray, args))
#         cond = self._argcheck(*args) & (scale > 0) & (loc == loc)
#         output = []
#         default = valarray(shape(cond), self.badvalue)
#
#         # Use only entries that are valid in calculation
#         if np.any(cond):
#             goodargs = argsreduce(cond, *(args+(scale, loc)))
#             scale, loc, goodargs = goodargs[-2], goodargs[-1], goodargs[:-2]
#
#             if self._stats_has_moments:
#                 mu, mu2, g1, g2 = self._stats(*goodargs,
#                                               **{'moments': moments})
#             else:
#                 mu, mu2, g1, g2 = self._stats(*goodargs)
#             if g1 is None:
#                 mu3 = None
#             else:
#                 if mu2 is None:
#                     mu2 = self._munp(2, *goodargs)
#                 if g2 is None:
#                     # (mu2**1.5) breaks down for nan and inf
#                     mu3 = g1 * np.power(mu2, 1.5)
#
#             if 'm' in moments:
#                 if mu is None:
#                     mu = self._munp(1, *goodargs)
#                 out0 = default.copy()
#                 place(out0, cond, mu * scale + loc)
#                 output.append(out0)
#
#             if 'v' in moments:
#                 if mu2 is None:
#                     mu2p = self._munp(2, *goodargs)
#                     if mu is None:
#                         mu = self._munp(1, *goodargs)
#                     mu2 = mu2p - mu * mu
#                     if np.isinf(mu):
#                         # if mean is inf then var is also inf
#                         mu2 = np.inf
#                 out0 = default.copy()
#                 place(out0, cond, mu2 * scale * scale)
#                 output.append(out0)
#
#             if 's' in moments:
#                 if g1 is None:
#                     mu3p = self._munp(3, *goodargs)
#                     if mu is None:
#                         mu = self._munp(1, *goodargs)
#                     if mu2 is None:
#                         mu2p = self._munp(2, *goodargs)
#                         mu2 = mu2p - mu * mu
#                     with np.errstate(invalid='ignore'):
#                         mu3 = (-mu*mu - 3*mu2)*mu + mu3p
#                         g1 = mu3 / np.power(mu2, 1.5)
#                 out0 = default.copy()
#                 place(out0, cond, g1)
#                 output.append(out0)
#
#             if 'k' in moments:
#                 if g2 is None:
#                     mu4p = self._munp(4, *goodargs)
#                     if mu is None:
#                         mu = self._munp(1, *goodargs)
#                     if mu2 is None:
#                         mu2p = self._munp(2, *goodargs)
#                         mu2 = mu2p - mu * mu
#                     if mu3 is None:
#                         mu3p = self._munp(3, *goodargs)
#                         with np.errstate(invalid='ignore'):
#                             mu3 = (-mu * mu - 3 * mu2) * mu + mu3p
#                             mu3 = mu3p - 3 * mu * mu2 - mu**3
#                     with np.errstate(invalid='ignore'):
#                         mu4 = ((-mu**2 - 6*mu2) * mu - 4*mu3)*mu + mu4p
#                         g2 = mu4 / mu2**2.0 - 3.0
#                 out0 = default.copy()
#                 place(out0, cond, g2)
#                 output.append(out0)
#         else:  # no valid args
#             output = [default.copy() for _ in moments]
#
#         if len(output) == 1:
#             return output[0]
#         else:
#             return tuple(output)
#
#     def entropy(self, *args, **kwds):
#         """
#         Differential entropy of the RV.
#
#         Parameters
#         ----------
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information).
#         loc : array_like, optional
#             Location parameter (default=0).
#         scale : array_like, optional  (continuous distributions only).
#             Scale parameter (default=1).
#
#         Notes
#         -----
#         Entropy is defined base `e`:
#
#         >>> drv = rv_discrete(values=((0, 1), (0.5, 0.5)))
#         >>> np.allclose(drv.entropy(), np.log(2.0))
#         True
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwds)
#         # NB: for discrete distributions scale=1 by construction in _parse_args
#         loc, scale = map(asarray, (loc, scale))
#         args = tuple(map(asarray, args))
#         cond0 = self._argcheck(*args) & (scale > 0) & (loc == loc)
#         output = zeros(shape(cond0), 'd')
#         place(output, (1-cond0), self.badvalue)
#         goodargs = argsreduce(cond0, scale, *args)
#         goodscale = goodargs[0]
#         goodargs = goodargs[1:]
#         place(output, cond0, self.vecentropy(*goodargs) + log(goodscale))
#         return output
#
#     def moment(self, n, *args, **kwds):
#         """
#         n-th order non-central moment of distribution.
#
#         Parameters
#         ----------
#         n : int, n >= 1
#             Order of moment.
#         arg1, arg2, arg3,... : float
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information).
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwds)
#         if not (self._argcheck(*args) and (scale > 0)):
#             return nan
#         if (floor(n) != n):
#             raise ValueError("Moment must be an integer.")
#         if (n < 0):
#             raise ValueError("Moment must be positive.")
#         mu, mu2, g1, g2 = None, None, None, None
#         if (n > 0) and (n < 5):
#             if self._stats_has_moments:
#                 mdict = {'moments': {1: 'm', 2: 'v', 3: 'vs', 4: 'vk'}[n]}
#             else:
#                 mdict = {}
#             mu, mu2, g1, g2 = self._stats(*args, **mdict)
#         val = _moment_from_stats(n, mu, mu2, g1, g2, self._munp, args)
#
#         # Convert to transformed  X = L + S*Y
#         # E[X^n] = E[(L+S*Y)^n] = L^n sum(comb(n, k)*(S/L)^k E[Y^k], k=0...n)
#         if loc == 0:
#             return scale**n * val
#         else:
#             result = 0
#             fac = float(scale) / float(loc)
#             for k in range(n):
#                 valk = _moment_from_stats(k, mu, mu2, g1, g2, self._munp, args)
#                 result += comb(n, k, exact=True)*(fac**k) * valk
#             result += fac**n * val
#             return result * loc**n
#
#     def median(self, *args, **kwds):
#         """
#         Median of the distribution.
#
#         Parameters
#         ----------
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             Location parameter, Default is 0.
#         scale : array_like, optional
#             Scale parameter, Default is 1.
#
#         Returns
#         -------
#         median : float
#             The median of the distribution.
#
#         See Also
#         --------
#         rv_discrete.ppf
#             Inverse of the CDF
#
#         """
#         return self.ppf(0.5, *args, **kwds)
#
#     def mean(self, *args, **kwds):
#         """
#         Mean of the distribution.
#
#         Parameters
#         ----------
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         mean : float
#             the mean of the distribution
#
#         """
#         kwds['moments'] = 'm'
#         res = self.stats(*args, **kwds)
#         if isinstance(res, ndarray) and res.ndim == 0:
#             return res[()]
#         return res
#
#     def var(self, *args, **kwds):
#         """
#         Variance of the distribution.
#
#         Parameters
#         ----------
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         var : float
#             the variance of the distribution
#
#         """
#         kwds['moments'] = 'v'
#         res = self.stats(*args, **kwds)
#         if isinstance(res, ndarray) and res.ndim == 0:
#             return res[()]
#         return res
#
#     def std(self, *args, **kwds):
#         """
#         Standard deviation of the distribution.
#
#         Parameters
#         ----------
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         std : float
#             standard deviation of the distribution
#
#         """
#         kwds['moments'] = 'v'
#         res = sqrt(self.stats(*args, **kwds))
#         return res
#
#     def interval(self, alpha, *args, **kwds):
#         """
#         Confidence interval with equal areas around the median.
#
#         Parameters
#         ----------
#         alpha : array_like of float
#             Probability that an rv will be drawn from the returned range.
#             Each value should be in the range [0, 1].
#         arg1, arg2, ... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information).
#         loc : array_like, optional
#             location parameter, Default is 0.
#         scale : array_like, optional
#             scale parameter, Default is 1.
#
#         Returns
#         -------
#         a, b : ndarray of float
#             end-points of range that contain ``100 * alpha %`` of the rv's
#             possible values.
#
#         """
#         alpha = asarray(alpha)
#         if np.any((alpha > 1) | (alpha < 0)):
#             raise ValueError("alpha must be between 0 and 1 inclusive")
#         q1 = (1.0-alpha)/2
#         q2 = (1.0+alpha)/2
#         a = self.ppf(q1, *args, **kwds)
#         b = self.ppf(q2, *args, **kwds)
#         return a, b
#
#     def support(self, *args, **kwargs):
#         """
#         Return the support of the distribution.
#
#         Parameters
#         ----------
#         arg1, arg2, ... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information).
#         loc : array_like, optional
#             location parameter, Default is 0.
#         scale : array_like, optional
#             scale parameter, Default is 1.
#         Returns
#         -------
#         a, b : float
#             end-points of the distribution's support.
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwargs)
#         _a, _b = self._get_support(*args)
#         return _a * scale + loc, _b * scale + loc
#
#
# class rv_continuous(rv_generic):
#     """
#     A generic continuous random variable class meant for subclassing.
#
#     `rv_continuous` is a base class to construct specific distribution classes
#     and instances for continuous random variables. It cannot be used
#     directly as a distribution.
#
#     Parameters
#     ----------
#     momtype : int, optional
#         The type of generic moment calculation to use: 0 for pdf, 1 (default)
#         for ppf.
#     a : float, optional
#         Lower bound of the support of the distribution, default is minus
#         infinity.
#     b : float, optional
#         Upper bound of the support of the distribution, default is plus
#         infinity.
#     xtol : float, optional
#         The tolerance for fixed point calculation for generic ppf.
#     badvalue : float, optional
#         The value in a result arrays that indicates a value that for which
#         some argument restriction is violated, default is np.nan.
#     name : str, optional
#         The name of the instance. This string is used to construct the default
#         example for distributions.
#     longname : str, optional
#         This string is used as part of the first line of the docstring returned
#         when a subclass has no docstring of its own. Note: `longname` exists
#         for backwards compatibility, do not use for new subclasses.
#     shapes : str, optional
#         The shape of the distribution. For example ``"m, n"`` for a
#         distribution that takes two integers as the two shape arguments for all
#         its methods. If not provided, shape parameters will be inferred from
#         the signature of the private methods, ``_pdf`` and ``_cdf`` of the
#         instance.
#     extradoc :  str, optional, deprecated
#         This string is used as the last part of the docstring returned when a
#         subclass has no docstring of its own. Note: `extradoc` exists for
#         backwards compatibility, do not use for new subclasses.
#     seed : None or int or ``numpy.random.RandomState`` instance, optional
#         This parameter defines the RandomState object to use for drawing
#         random variates.
#         If None (or np.random), the global np.random state is used.
#         If integer, it is used to seed the local RandomState instance.
#         Default is None.
#
#     Methods
#     -------
#     rvs
#     pdf
#     logpdf
#     cdf
#     logcdf
#     sf
#     logsf
#     ppf
#     isf
#     moment
#     stats
#     entropy
#     expect
#     median
#     mean
#     std
#     var
#     interval
#     __call__
#     fit
#     fit_loc_scale
#     nnlf
#     support
#
#     Notes
#     -----
#     Public methods of an instance of a distribution class (e.g., ``pdf``,
#     ``cdf``) check their arguments and pass valid arguments to private,
#     computational methods (``_pdf``, ``_cdf``). For ``pdf(x)``, ``x`` is valid
#     if it is within the support of the distribution.
#     Whether a shape parameter is valid is decided by an ``_argcheck`` method
#     (which defaults to checking that its arguments are strictly positive.)
#
#     **Subclassing**
#
#     New random variables can be defined by subclassing the `rv_continuous` class
#     and re-defining at least the ``_pdf`` or the ``_cdf`` method (normalized
#     to location 0 and scale 1).
#
#     If positive argument checking is not correct for your RV
#     then you will also need to re-define the ``_argcheck`` method.
#
#     For most of the scipy.stats distributions, the support interval doesn't
#     depend on the shape parameters. ``x`` being in the support interval is
#     equivalent to ``self.a <= x <= self.b``.  If either of the endpoints of
#     the support do depend on the shape parameters, then
#     i) the distribution must implement the ``_get_support`` method; and
#     ii) those dependent endpoints must be omitted from the distribution's
#     call to the ``rv_continuous`` initializer.
#
#     Correct, but potentially slow defaults exist for the remaining
#     methods but for speed and/or accuracy you can over-ride::
#
#       _logpdf, _cdf, _logcdf, _ppf, _rvs, _isf, _sf, _logsf
#
#     The default method ``_rvs`` relies on the inverse of the cdf, ``_ppf``,
#     applied to a uniform random variate. In order to generate random variates
#     efficiently, either the default ``_ppf`` needs to be overwritten (e.g.
#     if the inverse cdf can expressed in an explicit form) or a sampling
#     method needs to be implemented in a custom ``_rvs`` method.
#
#     If possible, you should override ``_isf``, ``_sf`` or ``_logsf``.
#     The main reason would be to improve numerical accuracy: for example,
#     the survival function ``_sf`` is computed as ``1 - _cdf`` which can
#     result in loss of precision if ``_cdf(x)`` is close to one.
#
#     **Methods that can be overwritten by subclasses**
#     ::
#
#       _rvs
#       _pdf
#       _cdf
#       _sf
#       _ppf
#       _isf
#       _stats
#       _munp
#       _entropy
#       _argcheck
#       _get_support
#
#     There are additional (internal and private) generic methods that can
#     be useful for cross-checking and for debugging, but might work in all
#     cases when directly called.
#
#     A note on ``shapes``: subclasses need not specify them explicitly. In this
#     case, `shapes` will be automatically deduced from the signatures of the
#     overridden methods (`pdf`, `cdf` etc).
#     If, for some reason, you prefer to avoid relying on introspection, you can
#     specify ``shapes`` explicitly as an argument to the instance constructor.
#
#
#     **Frozen Distributions**
#
#     Normally, you must provide shape parameters (and, optionally, location and
#     scale parameters to each call of a method of a distribution.
#
#     Alternatively, the object may be called (as a function) to fix the shape,
#     location, and scale parameters returning a "frozen" continuous RV object:
#
#     rv = generic(<shape(s)>, loc=0, scale=1)
#         `rv_frozen` object with the same methods but holding the given shape,
#         location, and scale fixed
#
#     **Statistics**
#
#     Statistics are computed using numerical integration by default.
#     For speed you can redefine this using ``_stats``:
#
#      - take shape parameters and return mu, mu2, g1, g2
#      - If you can't compute one of these, return it as None
#      - Can also be defined with a keyword argument ``moments``, which is a
#        string composed of "m", "v", "s", and/or "k".
#        Only the components appearing in string should be computed and
#        returned in the order "m", "v", "s", or "k"  with missing values
#        returned as None.
#
#     Alternatively, you can override ``_munp``, which takes ``n`` and shape
#     parameters and returns the n-th non-central moment of the distribution.
#
#     Examples
#     --------
#     To create a new Gaussian distribution, we would do the following:
#
#     >>> from scipy.stats import rv_continuous
#     >>> class gaussian_gen(rv_continuous):
#     ...     "Gaussian distribution"
#     ...     def _pdf(self, x):
#     ...         return np.exp(-x**2 / 2.) / np.sqrt(2.0 * np.pi)
#     >>> gaussian = gaussian_gen(name='gaussian')
#
#     ``scipy.stats`` distributions are *instances*, so here we subclass
#     `rv_continuous` and create an instance. With this, we now have
#     a fully functional distribution with all relevant methods automagically
#     generated by the framework.
#
#     Note that above we defined a standard normal distribution, with zero mean
#     and unit variance. Shifting and scaling of the distribution can be done
#     by using ``loc`` and ``scale`` parameters: ``gaussian.pdf(x, loc, scale)``
#     essentially computes ``y = (x - loc) / scale`` and
#     ``gaussian._pdf(y) / scale``.
#
#     """
#     def __init__(self, momtype=1, a=None, b=None, xtol=1e-14,
#                  badvalue=None, name=None, longname=None,
#                  shapes=None, extradoc=None, seed=None):
#
#         super(rv_continuous, self).__init__(seed)
#
#         # save the ctor parameters, cf generic freeze
#         self._ctor_param = dict(
#             momtype=momtype, a=a, b=b, xtol=xtol,
#             badvalue=badvalue, name=name, longname=longname,
#             shapes=shapes, extradoc=extradoc, seed=seed)
#
#         if badvalue is None:
#             badvalue = nan
#         if name is None:
#             name = 'Distribution'
#         self.badvalue = badvalue
#         self.name = name
#         self.a = a
#         self.b = b
#         if a is None:
#             self.a = -inf
#         if b is None:
#             self.b = inf
#         self.xtol = xtol
#         self.moment_type = momtype
#         self.shapes = shapes
#         self._construct_argparser(meths_to_inspect=[self._pdf, self._cdf],
#                                   locscale_in='loc=0, scale=1',
#                                   locscale_out='loc, scale')
#
#         # nin correction
#         self._ppfvec = vectorize(self._ppf_single, otypes='d')
#         self._ppfvec.nin = self.numargs + 1
#         self.vecentropy = vectorize(self._entropy, otypes='d')
#         self._cdfvec = vectorize(self._cdf_single, otypes='d')
#         self._cdfvec.nin = self.numargs + 1
#
#         self.extradoc = extradoc
#         if momtype == 0:
#             self.generic_moment = vectorize(self._mom0_sc, otypes='d')
#         else:
#             self.generic_moment = vectorize(self._mom1_sc, otypes='d')
#         # Because of the *args argument of _mom0_sc, vectorize cannot count the
#         # number of arguments correctly.
#         self.generic_moment.nin = self.numargs + 1
#
#         if longname is None:
#             if name[0] in ['aeiouAEIOU']:
#                 hstr = "An "
#             else:
#                 hstr = "A "
#             longname = hstr + name
#
#         if sys.flags.optimize < 2:
#             # Skip adding docstrings if interpreter is run with -OO
#             if self.__doc__ is None:
#                 self._construct_default_doc(longname=longname,
#                                             extradoc=extradoc,
#                                             docdict=docdict,
#                                             discrete='continuous')
#             else:
#                 dct = dict(distcont)
#                 self._construct_doc(docdict, dct.get(self.name))
#
#     def _updated_ctor_param(self):
#         """ Return the current version of _ctor_param, possibly updated by user.
#
#             Used by freezing and pickling.
#             Keep this in sync with the signature of __init__.
#         """
#         dct = self._ctor_param.copy()
#         dct['a'] = self.a
#         dct['b'] = self.b
#         dct['xtol'] = self.xtol
#         dct['badvalue'] = self.badvalue
#         dct['name'] = self.name
#         dct['shapes'] = self.shapes
#         dct['extradoc'] = self.extradoc
#         return dct
#
#     def _ppf_to_solve(self, x, q, *args):
#         return self.cdf(*(x, )+args)-q
#
#     def _ppf_single(self, q, *args):
#         left = right = None
#         _a, _b = self._get_support(*args)
#         if _a > -np.inf:
#             left = _a
#         if _b < np.inf:
#             right = _b
#
#         factor = 10.
#         if not left:  # i.e. self.a = -inf
#             left = -1.*factor
#             while self._ppf_to_solve(left, q, *args) > 0.:
#                 right = left
#                 left *= factor
#             # left is now such that cdf(left) < q
#         if not right:  # i.e. self.b = inf
#             right = factor
#             while self._ppf_to_solve(right, q, *args) < 0.:
#                 left = right
#                 right *= factor
#             # right is now such that cdf(right) > q
#
#         return optimize.brentq(self._ppf_to_solve,
#                                left, right, args=(q,)+args, xtol=self.xtol)
#
#     # moment from definition
#     def _mom_integ0(self, x, m, *args):
#         return x**m * self.pdf(x, *args)
#
#     def _mom0_sc(self, m, *args):
#         _a, _b = self._get_support(*args)
#         return integrate.quad(self._mom_integ0, _a, _b,
#                               args=(m,)+args)[0]
#
#     # moment calculated using ppf
#     def _mom_integ1(self, q, m, *args):
#         return (self.ppf(q, *args))**m
#
#     def _mom1_sc(self, m, *args):
#         return integrate.quad(self._mom_integ1, 0, 1, args=(m,)+args)[0]
#
#     def _pdf(self, x, *args):
#         return derivative(self._cdf, x, dx=1e-5, args=args, order=5)
#
#     ## Could also define any of these
#     def _logpdf(self, x, *args):
#         return log(self._pdf(x, *args))
#
#     def _cdf_single(self, x, *args):
#         _a, _b = self._get_support(*args)
#         return integrate.quad(self._pdf, _a, x, args=args)[0]
#
#     def _cdf(self, x, *args):
#         return self._cdfvec(x, *args)
#
#     ## generic _argcheck, _logcdf, _sf, _logsf, _ppf, _isf, _rvs are defined
#     ## in rv_generic
#
#     def pdf(self, x, *args, **kwds):
#         """
#         Probability density function at x of the given RV.
#
#         Parameters
#         ----------
#         x : array_like
#             quantiles
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         pdf : ndarray
#             Probability density function evaluated at x
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwds)
#         x, loc, scale = map(asarray, (x, loc, scale))
#         args = tuple(map(asarray, args))
#         dtyp = np.find_common_type([x.dtype, np.float64], [])
#         x = np.asarray((x - loc)/scale, dtype=dtyp)
#         cond0 = self._argcheck(*args) & (scale > 0)
#         cond1 = self._support_mask(x, *args) & (scale > 0)
#         cond = cond0 & cond1
#         output = zeros(shape(cond), dtyp)
#         putmask(output, (1-cond0)+np.isnan(x), self.badvalue)
#         if np.any(cond):
#             goodargs = argsreduce(cond, *((x,)+args+(scale,)))
#             scale, goodargs = goodargs[-1], goodargs[:-1]
#             place(output, cond, self._pdf(*goodargs) / scale)
#         if output.ndim == 0:
#             return output[()]
#         return output
#
#     def logpdf(self, x, *args, **kwds):
#         """
#         Log of the probability density function at x of the given RV.
#
#         This uses a more numerically accurate calculation if available.
#
#         Parameters
#         ----------
#         x : array_like
#             quantiles
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         logpdf : array_like
#             Log of the probability density function evaluated at x
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwds)
#         x, loc, scale = map(asarray, (x, loc, scale))
#         args = tuple(map(asarray, args))
#         dtyp = np.find_common_type([x.dtype, np.float64], [])
#         x = np.asarray((x - loc)/scale, dtype=dtyp)
#         cond0 = self._argcheck(*args) & (scale > 0)
#         cond1 = self._support_mask(x, *args) & (scale > 0)
#         cond = cond0 & cond1
#         output = empty(shape(cond), dtyp)
#         output.fill(NINF)
#         putmask(output, (1-cond0)+np.isnan(x), self.badvalue)
#         if np.any(cond):
#             goodargs = argsreduce(cond, *((x,)+args+(scale,)))
#             scale, goodargs = goodargs[-1], goodargs[:-1]
#             place(output, cond, self._logpdf(*goodargs) - log(scale))
#         if output.ndim == 0:
#             return output[()]
#         return output
#
#     def cdf(self, x, *args, **kwds):
#         """
#         Cumulative distribution function of the given RV.
#
#         Parameters
#         ----------
#         x : array_like
#             quantiles
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         cdf : ndarray
#             Cumulative distribution function evaluated at `x`
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwds)
#         _a, _b = self._get_support(*args)
#         x, loc, scale = map(asarray, (x, loc, scale))
#         args = tuple(map(asarray, args))
#         dtyp = np.find_common_type([x.dtype, np.float64], [])
#         x = np.asarray((x - loc)/scale, dtype=dtyp)
#         cond0 = self._argcheck(*args) & (scale > 0)
#         cond1 = self._open_support_mask(x, *args) & (scale > 0)
#         cond2 = (x >= _b) & cond0
#         cond = cond0 & cond1
#         output = zeros(shape(cond), dtyp)
#         place(output, (1-cond0)+np.isnan(x), self.badvalue)
#         place(output, cond2, 1.0)
#         if np.any(cond):  # call only if at least 1 entry
#             goodargs = argsreduce(cond, *((x,)+args))
#             place(output, cond, self._cdf(*goodargs))
#         if output.ndim == 0:
#             return output[()]
#         return output
#
#     def logcdf(self, x, *args, **kwds):
#         """
#         Log of the cumulative distribution function at x of the given RV.
#
#         Parameters
#         ----------
#         x : array_like
#             quantiles
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         logcdf : array_like
#             Log of the cumulative distribution function evaluated at x
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwds)
#         _a, _b = self._get_support(*args)
#         x, loc, scale = map(asarray, (x, loc, scale))
#         args = tuple(map(asarray, args))
#         dtyp = np.find_common_type([x.dtype, np.float64], [])
#         x = np.asarray((x - loc)/scale, dtype=dtyp)
#         cond0 = self._argcheck(*args) & (scale > 0)
#         cond1 = self._open_support_mask(x, *args) & (scale > 0)
#         cond2 = (x >= _b) & cond0
#         cond = cond0 & cond1
#         output = empty(shape(cond), dtyp)
#         output.fill(NINF)
#         place(output, (1-cond0)*(cond1 == cond1)+np.isnan(x), self.badvalue)
#         place(output, cond2, 0.0)
#         if np.any(cond):  # call only if at least 1 entry
#             goodargs = argsreduce(cond, *((x,)+args))
#             place(output, cond, self._logcdf(*goodargs))
#         if output.ndim == 0:
#             return output[()]
#         return output
#
#     def sf(self, x, *args, **kwds):
#         """
#         Survival function (1 - `cdf`) at x of the given RV.
#
#         Parameters
#         ----------
#         x : array_like
#             quantiles
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         sf : array_like
#             Survival function evaluated at x
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwds)
#         _a, _b = self._get_support(*args)
#         x, loc, scale = map(asarray, (x, loc, scale))
#         args = tuple(map(asarray, args))
#         dtyp = np.find_common_type([x.dtype, np.float64], [])
#         x = np.asarray((x - loc)/scale, dtype=dtyp)
#         cond0 = self._argcheck(*args) & (scale > 0)
#         cond1 = self._open_support_mask(x, *args) & (scale > 0)
#         cond2 = cond0 & (x <= _a)
#         cond = cond0 & cond1
#         output = zeros(shape(cond), dtyp)
#         place(output, (1-cond0)+np.isnan(x), self.badvalue)
#         place(output, cond2, 1.0)
#         if np.any(cond):
#             goodargs = argsreduce(cond, *((x,)+args))
#             place(output, cond, self._sf(*goodargs))
#         if output.ndim == 0:
#             return output[()]
#         return output
#
#     def logsf(self, x, *args, **kwds):
#         """
#         Log of the survival function of the given RV.
#
#         Returns the log of the "survival function," defined as (1 - `cdf`),
#         evaluated at `x`.
#
#         Parameters
#         ----------
#         x : array_like
#             quantiles
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         logsf : ndarray
#             Log of the survival function evaluated at `x`.
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwds)
#         _a, _b = self._get_support(*args)
#         x, loc, scale = map(asarray, (x, loc, scale))
#         args = tuple(map(asarray, args))
#         dtyp = np.find_common_type([x.dtype, np.float64], [])
#         x = np.asarray((x - loc)/scale, dtype=dtyp)
#         cond0 = self._argcheck(*args) & (scale > 0)
#         cond1 = self._open_support_mask(x, *args) & (scale > 0)
#         cond2 = cond0 & (x <= _a)
#         cond = cond0 & cond1
#         output = empty(shape(cond), dtyp)
#         output.fill(NINF)
#         place(output, (1-cond0)+np.isnan(x), self.badvalue)
#         place(output, cond2, 0.0)
#         if np.any(cond):
#             goodargs = argsreduce(cond, *((x,)+args))
#             place(output, cond, self._logsf(*goodargs))
#         if output.ndim == 0:
#             return output[()]
#         return output
#
#     def ppf(self, q, *args, **kwds):
#         """
#         Percent point function (inverse of `cdf`) at q of the given RV.
#
#         Parameters
#         ----------
#         q : array_like
#             lower tail probability
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         x : array_like
#             quantile corresponding to the lower tail probability q.
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwds)
#         _a, _b = self._get_support(*args)
#         q, loc, scale = map(asarray, (q, loc, scale))
#         args = tuple(map(asarray, args))
#         cond0 = self._argcheck(*args) & (scale > 0) & (loc == loc)
#         cond1 = (0 < q) & (q < 1)
#         cond2 = cond0 & (q == 0)
#         cond3 = cond0 & (q == 1)
#         cond = cond0 & cond1
#         output = valarray(shape(cond), value=self.badvalue)
#
#         lower_bound = _a * scale + loc
#         upper_bound = _b * scale + loc
#         place(output, cond2, argsreduce(cond2, lower_bound)[0])
#         place(output, cond3, argsreduce(cond3, upper_bound)[0])
#
#         if np.any(cond):  # call only if at least 1 entry
#             goodargs = argsreduce(cond, *((q,)+args+(scale, loc)))
#             scale, loc, goodargs = goodargs[-2], goodargs[-1], goodargs[:-2]
#             place(output, cond, self._ppf(*goodargs) * scale + loc)
#         if output.ndim == 0:
#             return output[()]
#         return output
#
#     def isf(self, q, *args, **kwds):
#         """
#         Inverse survival function (inverse of `sf`) at q of the given RV.
#
#         Parameters
#         ----------
#         q : array_like
#             upper tail probability
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information)
#         loc : array_like, optional
#             location parameter (default=0)
#         scale : array_like, optional
#             scale parameter (default=1)
#
#         Returns
#         -------
#         x : ndarray or scalar
#             Quantile corresponding to the upper tail probability q.
#
#         """
#         args, loc, scale = self._parse_args(*args, **kwds)
#         _a, _b = self._get_support(*args)
#         q, loc, scale = map(asarray, (q, loc, scale))
#         args = tuple(map(asarray, args))
#         cond0 = self._argcheck(*args) & (scale > 0) & (loc == loc)
#         cond1 = (0 < q) & (q < 1)
#         cond2 = cond0 & (q == 1)
#         cond3 = cond0 & (q == 0)
#         cond = cond0 & cond1
#         output = valarray(shape(cond), value=self.badvalue)
#
#         lower_bound = _a * scale + loc
#         upper_bound = _b * scale + loc
#         place(output, cond2, argsreduce(cond2, lower_bound)[0])
#         place(output, cond3, argsreduce(cond3, upper_bound)[0])
#
#         if np.any(cond):
#             goodargs = argsreduce(cond, *((q,)+args+(scale, loc)))
#             scale, loc, goodargs = goodargs[-2], goodargs[-1], goodargs[:-2]
#             place(output, cond, self._isf(*goodargs) * scale + loc)
#         if output.ndim == 0:
#             return output[()]
#         return output
#
#     def _nnlf(self, x, *args):
#         return -np.sum(self._logpdf(x, *args), axis=0)
#
#     def _unpack_loc_scale(self, theta):
#         try:
#             loc = theta[-2]
#             scale = theta[-1]
#             args = tuple(theta[:-2])
#         except IndexError:
#             raise ValueError("Not enough input arguments.")
#         return loc, scale, args
#
#     def nnlf(self, theta, x):
#         '''Return negative loglikelihood function.
#
#         Notes
#         -----
#         This is ``-sum(log pdf(x, theta), axis=0)`` where `theta` are the
#         parameters (including loc and scale).
#         '''
#         loc, scale, args = self._unpack_loc_scale(theta)
#         if not self._argcheck(*args) or scale <= 0:
#             return inf
#         x = asarray((x-loc) / scale)
#         n_log_scale = len(x) * log(scale)
#         if np.any(~self._support_mask(x, *args)):
#             return inf
#         return self._nnlf(x, *args) + n_log_scale
#
#     def _nnlf_and_penalty(self, x, args):
#         cond0 = ~self._support_mask(x, *args)
#         n_bad = np.count_nonzero(cond0, axis=0)
#         if n_bad > 0:
#             x = argsreduce(~cond0, x)[0]
#         logpdf = self._logpdf(x, *args)
#         finite_logpdf = np.isfinite(logpdf)
#         n_bad += np.sum(~finite_logpdf, axis=0)
#         if n_bad > 0:
#             penalty = n_bad * log(_XMAX) * 100
#             return -np.sum(logpdf[finite_logpdf], axis=0) + penalty
#         return -np.sum(logpdf, axis=0)
#
#     def _penalized_nnlf(self, theta, x):
#         ''' Return penalized negative loglikelihood function,
#         i.e., - sum (log pdf(x, theta), axis=0) + penalty
#            where theta are the parameters (including loc and scale)
#         '''
#         loc, scale, args = self._unpack_loc_scale(theta)
#         if not self._argcheck(*args) or scale <= 0:
#             return inf
#         x = asarray((x-loc) / scale)
#         n_log_scale = len(x) * log(scale)
#         return self._nnlf_and_penalty(x, args) + n_log_scale
#
#     # return starting point for fit (shape arguments + loc + scale)
#     def _fitstart(self, data, args=None):
#         if args is None:
#             args = (1.0,)*self.numargs
#         loc, scale = self._fit_loc_scale_support(data, *args)
#         return args + (loc, scale)
#
#     # Return the (possibly reduced) function to optimize in order to find MLE
#     #  estimates for the .fit method
#     def _reduce_func(self, args, kwds):
#         # First of all, convert fshapes params to fnum: eg for stats.beta,
#         # shapes='a, b'. To fix `a`, can specify either `f1` or `fa`.
#         # Convert the latter into the former.
#         if self.shapes:
#             shapes = self.shapes.replace(',', ' ').split()
#             for j, s in enumerate(shapes):
#                 val = kwds.pop('f' + s, None) or kwds.pop('fix_' + s, None)
#                 if val is not None:
#                     key = 'f%d' % j
#                     if key in kwds:
#                         raise ValueError("Duplicate entry for %s." % key)
#                     else:
#                         kwds[key] = val
#
#         args = list(args)
#         Nargs = len(args)
#         fixedn = []
#         names = ['f%d' % n for n in range(Nargs - 2)] + ['floc', 'fscale']
#         x0 = []
#         for n, key in enumerate(names):
#             if key in kwds:
#                 fixedn.append(n)
#                 args[n] = kwds.pop(key)
#             else:
#                 x0.append(args[n])
#
#         if len(fixedn) == 0:
#             func = self._penalized_nnlf
#             restore = None
#         else:
#             if len(fixedn) == Nargs:
#                 raise ValueError(
#                     "All parameters fixed. There is nothing to optimize.")
#
#             def restore(args, theta):
#                 # Replace with theta for all numbers not in fixedn
#                 # This allows the non-fixed values to vary, but
#                 #  we still call self.nnlf with all parameters.
#                 i = 0
#                 for n in range(Nargs):
#                     if n not in fixedn:
#                         args[n] = theta[i]
#                         i += 1
#                 return args
#
#             def func(theta, x):
#                 newtheta = restore(args[:], theta)
#                 return self._penalized_nnlf(newtheta, x)
#
#         return x0, func, restore, args
#
#     def fit(self, data, *args, **kwds):
#         """
#         Return MLEs for shape (if applicable), location, and scale
#         parameters from data.
#
#         MLE stands for Maximum Likelihood Estimate.  Starting estimates for
#         the fit are given by input arguments; for any arguments not provided
#         with starting estimates, ``self._fitstart(data)`` is called to generate
#         such.
#
#         One can hold some parameters fixed to specific values by passing in
#         keyword arguments ``f0``, ``f1``, ..., ``fn`` (for shape parameters)
#         and ``floc`` and ``fscale`` (for location and scale parameters,
#         respectively).
#
#         Parameters
#         ----------
#         data : array_like
#             Data to use in calculating the MLEs.
#         args : floats, optional
#             Starting value(s) for any shape-characterizing arguments (those not
#             provided will be determined by a call to ``_fitstart(data)``).
#             No default value.
#         kwds : floats, optional
#             Starting values for the location and scale parameters; no default.
#             Special keyword arguments are recognized as holding certain
#             parameters fixed:
#
#             - f0...fn : hold respective shape parameters fixed.
#               Alternatively, shape parameters to fix can be specified by name.
#               For example, if ``self.shapes == "a, b"``, ``fa``and ``fix_a``
#               are equivalent to ``f0``, and ``fb`` and ``fix_b`` are
#               equivalent to ``f1``.
#
#             - floc : hold location parameter fixed to specified value.
#
#             - fscale : hold scale parameter fixed to specified value.
#
#             - optimizer : The optimizer to use.  The optimizer must take ``func``,
#               and starting position as the first two arguments,
#               plus ``args`` (for extra arguments to pass to the
#               function to be optimized) and ``disp=0`` to suppress
#               output as keyword arguments.
#
#         Returns
#         -------
#         mle_tuple : tuple of floats
#             MLEs for any shape parameters (if applicable), followed by those
#             for location and scale. For most random variables, shape statistics
#             will be returned, but there are exceptions (e.g. ``norm``).
#
#         Notes
#         -----
#         This fit is computed by maximizing a log-likelihood function, with
#         penalty applied for samples outside of range of the distribution. The
#         returned answer is not guaranteed to be the globally optimal MLE, it
#         may only be locally optimal, or the optimization may fail altogether.
#
#         Examples
#         --------
#
#         Generate some data to fit: draw random variates from the `beta`
#         distribution
#
#         >>> from scipy.stats import beta
#         >>> a, b = 1., 2.
#         >>> x = beta.rvs(a, b, size=1000)
#
#         Now we can fit all four parameters (``a``, ``b``, ``loc`` and ``scale``):
#
#         >>> a1, b1, loc1, scale1 = beta.fit(x)
#
#         We can also use some prior knowledge about the dataset: let's keep
#         ``loc`` and ``scale`` fixed:
#
#         >>> a1, b1, loc1, scale1 = beta.fit(x, floc=0, fscale=1)
#         >>> loc1, scale1
#         (0, 1)
#
#         We can also keep shape parameters fixed by using ``f``-keywords. To
#         keep the zero-th shape parameter ``a`` equal 1, use ``f0=1`` or,
#         equivalently, ``fa=1``:
#
#         >>> a1, b1, loc1, scale1 = beta.fit(x, fa=1, floc=0, fscale=1)
#         >>> a1
#         1
#
#         Not all distributions return estimates for the shape parameters.
#         ``norm`` for example just returns estimates for location and scale:
#
#         >>> from scipy.stats import norm
#         >>> x = norm.rvs(a, b, size=1000, random_state=123)
#         >>> loc1, scale1 = norm.fit(x)
#         >>> loc1, scale1
#         (0.92087172783841631, 2.0015750750324668)
#         """
#         Narg = len(args)
#         if Narg > self.numargs:
#             raise TypeError("Too many input arguments.")
#
#         start = [None]*2
#         if (Narg < self.numargs) or not ('loc' in kwds and
#                                          'scale' in kwds):
#             # get distribution specific starting locations
#             start = self._fitstart(data)
#             args += start[Narg:-2]
#         loc = kwds.pop('loc', start[-2])
#         scale = kwds.pop('scale', start[-1])
#         args += (loc, scale)
#         x0, func, restore, args = self._reduce_func(args, kwds)
#
#         optimizer = kwds.pop('optimizer', optimize.fmin)
#         # convert string to function in scipy.optimize
#         if not callable(optimizer) and isinstance(optimizer, string_types):
#             if not optimizer.startswith('fmin_'):
#                 optimizer = "fmin_"+optimizer
#             if optimizer == 'fmin_':
#                 optimizer = 'fmin'
#             try:
#                 optimizer = getattr(optimize, optimizer)
#             except AttributeError:
#                 raise ValueError("%s is not a valid optimizer" % optimizer)
#
#         # by now kwds must be empty, since everybody took what they needed
#         if kwds:
#             raise TypeError("Unknown arguments: %s." % kwds)
#
#         vals = optimizer(func, x0, args=(ravel(data),), disp=0)
#         if restore is not None:
#             vals = restore(args, vals)
#         vals = tuple(vals)
#         return vals
#
#     def _fit_loc_scale_support(self, data, *args):
#         """
#         Estimate loc and scale parameters from data accounting for support.
#
#         Parameters
#         ----------
#         data : array_like
#             Data to fit.
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information).
#
#         Returns
#         -------
#         Lhat : float
#             Estimated location parameter for the data.
#         Shat : float
#             Estimated scale parameter for the data.
#
#         """
#         data = np.asarray(data)
#
#         # Estimate location and scale according to the method of moments.
#         loc_hat, scale_hat = self.fit_loc_scale(data, *args)
#
#         # Compute the support according to the shape parameters.
#         self._argcheck(*args)
#         _a, _b = self._get_support(*args)
#         a, b = _a, _b
#         support_width = b - a
#
#         # If the support is empty then return the moment-based estimates.
#         if support_width <= 0:
#             return loc_hat, scale_hat
#
#         # Compute the proposed support according to the loc and scale
#         # estimates.
#         a_hat = loc_hat + a * scale_hat
#         b_hat = loc_hat + b * scale_hat
#
#         # Use the moment-based estimates if they are compatible with the data.
#         data_a = np.min(data)
#         data_b = np.max(data)
#         if a_hat < data_a and data_b < b_hat:
#             return loc_hat, scale_hat
#
#         # Otherwise find other estimates that are compatible with the data.
#         data_width = data_b - data_a
#         rel_margin = 0.1
#         margin = data_width * rel_margin
#
#         # For a finite interval, both the location and scale
#         # should have interesting values.
#         if support_width < np.inf:
#             loc_hat = (data_a - a) - margin
#             scale_hat = (data_width + 2 * margin) / support_width
#             return loc_hat, scale_hat
#
#         # For a one-sided interval, use only an interesting location parameter.
#         if a > -np.inf:
#             return (data_a - a) - margin, 1
#         elif b < np.inf:
#             return (data_b - b) + margin, 1
#         else:
#             raise RuntimeError
#
#     def fit_loc_scale(self, data, *args):
#         """
#         Estimate loc and scale parameters from data using 1st and 2nd moments.
#
#         Parameters
#         ----------
#         data : array_like
#             Data to fit.
#         arg1, arg2, arg3,... : array_like
#             The shape parameter(s) for the distribution (see docstring of the
#             instance object for more information).
#
#         Returns
#         -------
#         Lhat : float
#             Estimated location parameter for the data.
#         Shat : float
#             Estimated scale parameter for the data.
#
#         """
#         mu, mu2 = self.stats(*args, **{'moments': 'mv'})
#         tmp = asarray(data)
#         muhat = tmp.mean()
#         mu2hat = tmp.var()
#         Shat = sqrt(mu2hat / mu2)
#         Lhat = muhat - Shat*mu
#         if not np.isfinite(Lhat):
#             Lhat = 0
#         if not (np.isfinite(Shat) and (0 < Shat)):
#             Shat = 1
#         return Lhat, Shat
#
#     def _entropy(self, *args):
#         def integ(x):
#             val = self._pdf(x, *args)
#             return entr(val)
#
#         # upper limit is often inf, so suppress warnings when integrating
#         _a, _b = self._get_support(*args)
#         olderr = np.seterr(over='ignore')
#         h = integrate.quad(integ, _a, _b)[0]
#         np.seterr(**olderr)
#
#         if not np.isnan(h):
#             return h
#         else:
#             # try with different limits if integration problems
#             low, upp = self.ppf([1e-10, 1. - 1e-10], *args)
#             if np.isinf(_b):
#                 upper = upp
#             else:
#                 upper = _b
#             if np.isinf(_a):
#                 lower = low
#             else:
#                 lower = _a
#             return integrate.quad(integ, lower, upper)[0]
#
#     def expect(self, func=None, args=(), loc=0, scale=1, lb=None, ub=None,
#                conditional=False, **kwds):
#         """Calculate expected value of a function with respect to the
#         distribution by numerical integration.
#
#         The expected value of a function ``f(x)`` with respect to a
#         distribution ``dist`` is defined as::
#
#                     ub
#             E[f(x)] = Integral(f(x) * dist.pdf(x)),
#                     lb
#
#         where ``ub`` and ``lb`` are arguments and ``x`` has the ``dist.pdf(x)``
#         distribution. If the bounds ``lb`` and ``ub`` correspond to the
#         support of the distribution, e.g. ``[-inf, inf]`` in the default
#         case, then the integral is the unrestricted expectation of ``f(x)``.
#         Also, the function ``f(x)`` may be defined such that ``f(x)`` is ``0``
#         outside a finite interval in which case the expectation is
#         calculated within the finite range ``[lb, ub]``.
#
#         Parameters
#         ----------
#         func : callable, optional
#             Function for which integral is calculated. Takes only one argument.
#             The default is the identity mapping f(x) = x.
#         args : tuple, optional
#             Shape parameters of the distribution.
#         loc : float, optional
#             Location parameter (default=0).
#         scale : float, optional
#             Scale parameter (default=1).
#         lb, ub : scalar, optional
#             Lower and upper bound for integration. Default is set to the
#             support of the distribution.
#         conditional : bool, optional
#             If True, the integral is corrected by the conditional probability
#             of the integration interval.  The return value is the expectation
#             of the function, conditional on being in the given interval.
#             Default is False.
#
#         Additional keyword arguments are passed to the integration routine.
#
#         Returns
#         -------
#         expect : float
#             The calculated expected value.
#
#         Notes
#         -----
#         The integration behavior of this function is inherited from
#         `scipy.integrate.quad`. Neither this function nor
#         `scipy.integrate.quad` can verify whether the integral exists or is
#         finite. For example ``cauchy(0).mean()`` returns ``np.nan`` and
#         ``cauchy(0).expect()`` returns ``0.0``.
#
#         Examples
#         --------
#
#         To understand the effect of the bounds of integration consider
#         >>> from scipy.stats import expon
#         >>> expon(1).expect(lambda x: 1, lb=0.0, ub=2.0)
#         0.6321205588285578
#
#         This is close to
#
#         >>> expon(1).cdf(2.0) - expon(1).cdf(0.0)
#         0.6321205588285577
#
#         If ``conditional=True``
#
#         >>> expon(1).expect(lambda x: 1, lb=0.0, ub=2.0, conditional=True)
#         1.0000000000000002
#
#         The slight deviation from 1 is due to numerical integration.
#         """
#         lockwds = {'loc': loc,
#                    'scale': scale}
#         self._argcheck(*args)
#         _a, _b = self._get_support(*args)
#         if func is None:
#             def fun(x, *args):
#                 return x * self.pdf(x, *args, **lockwds)
#         else:
#             def fun(x, *args):
#                 return func(x) * self.pdf(x, *args, **lockwds)
#         if lb is None:
#             lb = loc + _a * scale
#         if ub is None:
#             ub = loc + _b * scale
#         if conditional:
#             invfac = (self.sf(lb, *args, **lockwds)
#                       - self.sf(ub, *args, **lockwds))
#         else:
#             invfac = 1.0
#         kwds['args'] = args
#         # Silence floating point warnings from integration.
#         olderr = np.seterr(all='ignore')
#         vals = integrate.quad(fun, lb, ub, **kwds)[0] / invfac
#         np.seterr(**olderr)
#         return vals
#
#
# class kstwobign_gen(rv_continuous):
#     r"""Kolmogorov-Smirnov two-sided test for large N.
#
#     This is the asymptotic distribution of the two-sided Kolmogorov-Smirnov
#     statistic :math:`\sqrt{n} D_n` that measures the maximum absolute
#     distance of the theoretical CDF from the empirical CDF (see `kstest`).
#
#     %(before_notes)s
#
#     Notes
#     -----
#     :math:`\sqrt{n} D_n` is given by
#
#     .. math::
#
#         D_n = \text{sup}_x |F_n(x) - F(x)|
#
#     where :math:`F` is a CDF and :math:`F_n` is an empirical CDF. `kstwobign`
#     describes the asymptotic distribution (i.e. the limit of
#     :math:`\sqrt{n} D_n`) under the null hypothesis of the KS test that the
#     empirical CDF corresponds to i.i.d. random variates with CDF :math:`F`.
#
#     %(after_notes)s
#
#     See Also
#     --------
#     ksone, kstest
#
#     References
#     ----------
#     .. [1] Marsaglia, G. et al. "Evaluating Kolmogorov's distribution",
#        Journal of Statistical Software, 8(18), 2003.
#
#     %(example)s
#
#     """
#     def _pdf(self, x):
#         # return -scu._kolmogp(x)
#         return None
#
#     def _cdf(self, x):
#         # return scu._kolmogc(x)
#         return None
#
#     def _sf(self, x):
#         # return sc.kolmogorov(x)
#         return None
#
#     def _ppf(self, q):
#         # return scu._kolmogci(q)
#         return None
#
#     def _isf(self, q):
#         # return sc.kolmogi(q)
#         return None


# kstwobign = kstwobign_gen(a=0.0, name='kstwobign')
#
# def _compute_prob_outside_square(n, h):
#     """Compute the proportion of paths that pass outside the two diagonal lines.
#
#     Parameters
#     ----------
#     n : integer
#         n > 0
#     h : integer
#         0 <= h <= n
#
#     Returns
#     -------
#     p : float
#         The proportion of paths that pass outside the lines x-y = +/-h.
#
#     """
#     # Compute Pr(D_{n,n} >= h/n)
#     # Prob = 2 * ( binom(2n, n-h) - binom(2n, n-2a) + binom(2n, n-3a) - ... )  / binom(2n, n)
#     # This formulation exhibits subtractive cancellation.
#     # Instead divide each term by binom(2n, n), then factor common terms
#     # and use a Horner-like algorithm
#     # P = 2 * A0 * (1 - A1*(1 - A2*(1 - A3*(1 - A4*(...)))))
#
#     P = 0.0
#     k = int(np.floor(n / h))
#     while k >= 0:
#         p1 = 1.0
#         # Each of the Ai terms has numerator and denominator with h simple terms.
#         for j in range(h):
#             p1 = (n - k * h - j) * p1 / (n + k * h + j + 1)
#         P = p1 * (1.0 - P)
#         k -= 1
#     return 2 * P
#
# def _compute_prob_inside_method(m, n, g, h):
#     """Count the proportion of paths that stay strictly inside two diagonal lines.
#
#     Parameters
#     ----------
#     m : integer
#         m > 0
#     n : integer
#         n > 0
#     g : integer
#         g is greatest common divisor of m and n
#     h : integer
#         0 <= h <= lcm(m,n)
#
#     Returns
#     -------
#     p : float
#         The proportion of paths that stay inside the two lines.
#
#
#     Count the integer lattice paths from (0, 0) to (m, n) which satisfy
#     |x/m - y/n| < h / lcm(m, n).
#     The paths make steps of size +1 in either positive x or positive y directions.
#
#     We generally follow Hodges' treatment of Drion/Gnedenko/Korolyuk.
#     Hodges, J.L. Jr.,
#     "The Significance Probability of the Smirnov Two-Sample Test,"
#     Arkiv fiur Matematik, 3, No. 43 (1958), 469-86.
#     """
#     # Probability is symmetrical in m, n.  Computation below uses m >= n.
#     if m < n:
#         m, n = n, m
#     mg = m // g
#     ng = n // g
#
#     # Count the integer lattice paths from (0, 0) to (m, n) which satisfy
#     # |nx/g - my/g| < h.
#     # Compute matrix A such that:
#     #  A(x, 0) = A(0, y) = 1
#     #  A(x, y) = A(x, y-1) + A(x-1, y), for x,y>=1, except that
#     #  A(x, y) = 0 if |x/m - y/n|>= h
#     # Probability is A(m, n)/binom(m+n, n)
#     # Optimizations exist for m==n, m==n*p.
#     # Only need to preserve a single column of A, and only a sliding window of it.
#     # minj keeps track of the slide.
#     minj, maxj = 0, min(int(np.ceil(h / mg)), n + 1)
#     curlen = maxj - minj
#     # Make a vector long enough to hold maximum window needed.
#     lenA = min(2 * maxj + 2, n + 1)
#     # This is an integer calculation, but the entries are essentially
#     # binomial coefficients, hence grow quickly.
#     # Scaling after each column is computed avoids dividing by a
#     # large binomial coefficent at the end. Instead it is incorporated
#     # one factor at a time during the computation.
#     dtype = np.float64
#     A = np.zeros(lenA, dtype=dtype)
#     # Initialize the first column
#     A[minj:maxj] = 1
#     for i in range(1, m + 1):
#         # Generate the next column.
#         # First calculate the sliding window
#         lastminj, lastmaxj, lastlen = minj, maxj, curlen
#         minj = max(int(np.floor((ng * i - h) / mg)) + 1, 0)
#         minj = min(minj, n)
#         maxj = min(int(np.ceil((ng * i + h) / mg)), n + 1)
#         if maxj <= minj:
#             return 0
#         # Now fill in the values
#         A[0:maxj - minj] = np.cumsum(A[minj - lastminj:maxj - lastminj])
#         curlen = maxj - minj
#         if lastlen > curlen:
#             # Set some carried-over elements to 0
#             A[maxj - minj:maxj - minj + (lastlen - curlen)] = 0
#         # Peel off one term from each of top and bottom of the binomial coefficient.
#         scaling_factor = i * 1.0 / (n + i)
#         A *= scaling_factor
#     return A[maxj - minj - 1]
#
# def _count_paths_outside_method(m, n, g, h):
#     """Count the number of paths that pass outside the specified diagonal.
#
#     Parameters
#     ----------
#     m : integer
#         m > 0
#     n : integer
#         n > 0
#     g : integer
#         g is greatest common divisor of m and n
#     h : integer
#         0 <= h <= lcm(m,n)
#
#     Returns
#     -------
#     p : float
#         The number of paths that go low.
#         The calculation may overflow - check for a finite answer.
#
#     Exceptions
#     ----------
#     FloatingPointError: Raised if the intermediate computation goes outside
#     the range of a float.
#
#     Notes
#     -----
#     Count the integer lattice paths from (0, 0) to (m, n), which at some
#     point (x, y) along the path, satisfy:
#       m*y <= n*x - h*g
#     The paths make steps of size +1 in either positive x or positive y directions.
#
#     We generally follow Hodges' treatment of Drion/Gnedenko/Korolyuk.
#     Hodges, J.L. Jr.,
#     "The Significance Probability of the Smirnov Two-Sample Test,"
#     Arkiv fiur Matematik, 3, No. 43 (1958), 469-86.
#     """
#     # Compute #paths which stay lower than x/m-y/n = h/lcm(m,n)
#     # B(x, y) = #{paths from (0,0) to (x,y) without previously crossing the boundary}
#     #         = binom(x, y) - #{paths which already reached the boundary}
#     # Multiply by the number of path extensions going from (x, y) to (m, n)
#     # Sum.
#
#     # Probability is symmetrical in m, n.  Computation below assumes m >= n.
#     if m < n:
#         m, n = n, m
#     mg = m // g
#     ng = n // g
#
#     #  0 <= x_j <= m is the smallest integer for which n*x_j - m*j < g*h
#     xj = [int(np.ceil((h + mg * j)/ng)) for j in range(n+1)]
#     xj = [_ for _ in xj if _ <= m]
#     lxj = len(xj)
#     # B is an array just holding a few values of B(x,y), the ones needed.
#     # B[j] == B(x_j, j)
#     if lxj == 0:
#         return np.round(special.binom(m + n, n))
#     B = np.zeros(lxj)
#     B[0] = 1
#     # Compute the B(x, y) terms
#     # The binomial coefficient is an integer, but special.binom() may return a float.
#     # Round it to the nearest integer.
#     for j in range(1, lxj):
#         Bj = np.round(special.binom(xj[j] + j, j))
#         if not np.isfinite(Bj):
#             raise FloatingPointError()
#         for i in range(j):
#             bin = np.round(special.binom(xj[j] - xj[i] + j - i, j-i))
#             dec = bin * B[i]
#             Bj -= dec
#         B[j] = Bj
#         if not np.isfinite(Bj):
#             raise FloatingPointError()
#     # Compute the number of path extensions...
#     num_paths = 0
#     for j in range(lxj):
#         bin = np.round(special.binom((m-xj[j]) + (n - j), n-j))
#         term = B[j] * bin
#         if not np.isfinite(term):
#             raise FloatingPointError()
#         num_paths += term
#     return np.round(num_paths)

# def sf(self, x, *args, **kwds):
#     """
#     Survival function (1 - `cdf`) at x of the given RV.
#
#     Parameters
#     ----------
#     x : array_like
#         quantiles
#     arg1, arg2, arg3,... : array_like
#         The shape parameter(s) for the distribution (see docstring of the
#         instance object for more information)
#     loc : array_like, optional
#         location parameter (default=0)
#     scale : array_like, optional
#         scale parameter (default=1)
#
#     Returns
#     -------
#     sf : array_like
#         Survival function evaluated at x
#
#     """
#     args, loc, scale = self._parse_args(*args, **kwds)
#     _a, _b = self._get_support(*args)
#     x, loc, scale = map(asarray, (x, loc, scale))
#     args = tuple(map(asarray, args))
#     dtyp = np.find_common_type([x.dtype, np.float64], [])
#     x = np.asarray((x - loc)/scale, dtype=dtyp)
#     cond0 = self._argcheck(*args) & (scale > 0)
#     cond1 = self._open_support_mask(x, *args) & (scale > 0)
#     cond2 = cond0 & (x <= _a)
#     cond = cond0 & cond1
#     output = zeros(shape(cond), dtyp)
#     place(output, (1-cond0)+np.isnan(x), self.badvalue)
#     place(output, cond2, 1.0)
#     if np.any(cond):
#         goodargs = argsreduce(cond, *((x,)+args))
#         place(output, cond, self._sf(*goodargs))
#     if output.ndim == 0:
#         return output[()]
#     return output



Ks_2sampResult = namedtuple('Ks_2sampResult', ('statistic', 'pvalue'))


def ks_2samp(data1, data2, alternative='two-sided', mode='auto'):
    """
    Compute the Kolmogorov-Smirnov statistic on 2 samples.

    This is a two-sided test for the null hypothesis that 2 independent samples
    are drawn from the same continuous distribution.  The
    alternative hypothesis can be either 'two-sided' (default), 'less'
    or 'greater'.

    Parameters
    ----------
    data1, data2 : sequence of 1-D ndarrays
        Two arrays of sample observations assumed to be drawn from a continuous
        distribution, sample sizes can be different.
    alternative : {'two-sided', 'less', 'greater'}, optional
        Defines the alternative hypothesis (see explanation above).
        Default is 'two-sided'.
    mode : {'auto', 'exact', 'asymp'}, optional
        Defines the method used for calculating the p-value.
        Default is 'auto'.

        - 'exact' : use approximation to exact distribution of test statistic
        - 'asymp' : use asymptotic distribution of test statistic
        - 'auto' : use 'exact' for small size arrays, 'asymp' for large.

    Returns
    -------
    statistic : float
        KS statistic
    pvalue : float
        two-tailed p-value

    Notes
    -----
    This tests whether 2 samples are drawn from the same distribution. Note
    that, like in the case of the one-sample K-S test, the distribution is
    assumed to be continuous.

    In the one-sided test, the alternative is that the empirical
    cumulative distribution function F(x) of the data1 variable is "less"
    or "greater" than the empirical cumulative distribution function G(x)
    of the data2 variable, ``F(x)<=G(x)``, resp. ``F(x)>=G(x)``.

    If the K-S statistic is small or the p-value is high, then we cannot
    reject the hypothesis that the distributions of the two samples
    are the same.

    If the mode is 'auto', the computation is exact if the sample sizes are
    less than 10000.  For larger sizes, the computation uses the
    Kolmogorov-Smirnov distributions to compute an approximate value.

    We generally follow Hodges' treatment of Drion/Gnedenko/Korolyuk [1]_.

    References
    ----------
    .. [1] Hodges, J.L. Jr.,  "The Significance Probability of the Smirnov
           Two-Sample Test," Arkiv fiur Matematik, 3, No. 43 (1958), 469-86.


    Examples
    --------
    >>> from scipy import stats
    >>> np.random.seed(12345678)  #fix random seed to get the same result
    >>> n1 = 200  # size of first sample
    >>> n2 = 300  # size of second sample

    For a different distribution, we can reject the null hypothesis since the
    pvalue is below 1%:

    >>> rvs1 = stats.norm.rvs(size=n1, loc=0., scale=1)
    >>> rvs2 = stats.norm.rvs(size=n2, loc=0.5, scale=1.5)
    >>> stats.ks_2samp(rvs1, rvs2)
    (0.20833333333333334, 5.129279597781977e-05)

    For a slightly different distribution, we cannot reject the null hypothesis
    at a 10% or lower alpha since the p-value at 0.144 is higher than 10%

    >>> rvs3 = stats.norm.rvs(size=n2, loc=0.01, scale=1.0)
    >>> stats.ks_2samp(rvs1, rvs3)
    (0.10333333333333333, 0.14691437867433876)

    For an identical distribution, we cannot reject the null hypothesis since
    the p-value is high, 41%:

    >>> rvs4 = stats.norm.rvs(size=n2, loc=0.0, scale=1.0)
    >>> stats.ks_2samp(rvs1, rvs4)
    (0.07999999999999996, 0.41126949729859719)

    """
    LARGE_N = 10000  # 'auto' will attempt to be exact if n1,n2 <= LARGE_N
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
    original_mode = mode
    if mode == 'auto':
        if max(n1, n2) <= LARGE_N:
            mode = 'exact'
        else:
            mode = 'asymp'
    elif mode == 'exact':
        # If lcm(n1, n2) is too big, switch from exact to asymp
        if n1g >= np.iinfo(np.int).max / n2g:
            mode = 'asymp'
            warnings.warn(
                "Exact ks_2samp calculation not possible with samples sizes "
                "%d and %d. Switching to 'asymp' " % (n1, n2), RuntimeWarning)

    saw_fp_error = False
    if mode == 'exact':
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
                        warnings.warn(
                            "ks_2samp: Exact calculation overflowed. "
                            "Switching to mode=%s" % mode, RuntimeWarning)
                else:
                    if prob > 1 or prob < 0:
                        mode = 'asymp'
                        if original_mode == 'exact':
                            warnings.warn(
                                "ks_2samp: Exact calculation incurred large"
                                " rounding error. Switching to mode=%s" % mode,
                                RuntimeWarning)

    if mode == 'asymp':
        raise NotImplementedError
        # The product n1*n2 is large.  Use Smirnov's asymptoptic formula.
        # if alternative == 'two-sided':
        #     en = np.sqrt(n1 * n2 / (n1 + n2))
        #     # Switch to using kstwo.sf() when it becomes available.
        #     # kstwo.sf()
        #     # prob = distributions.kstwo.sf(d, int(np.round(en)))
        #
        #     ### previously
        #     # prob = distributions.kstwobign.sf(en * d)
        #     prob = sf(en * d)
        # else:
        #     m, n = max(n1, n2), min(n1, n2)
        #     z = np.sqrt(m*n/(m+n)) * d
        #     # Use Hodges' suggested approximation Eqn 5.3
        #     expt = -2 * z**2 - 2 * z * (m + 2*n)/np.sqrt(m*n*(m+n))/3.0
            prob = np.exp(expt)

    prob = (0 if prob < 0 else (1 if prob > 1 else prob))
    # return Ks_2sampResult(d, prob)
    return d, prob


