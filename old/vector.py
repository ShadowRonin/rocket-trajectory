# Shamelessly stolen from ModSimPy

import pandas as pd
import numpy as np

def underride(d, **options):
    """Add key-value pairs to d only if key is not in d.

    If d is None, create a new dictionary.

    d: dictionary
    options: keyword args to add to d
    """
    if d is None:
        d = {}

    for key, val in options.items():
        d.setdefault(key, val)

    return d

def Vector(x, y, z=None, **options):
    """
    """
    underride(options, name='component')
    if z is None:
        return pd.Series(dict(x=x, y=y), **options)
    else:
        return pd.Series(dict(x=x, y=y, z=z), **options)


## Vector functions (should work with any sequence)

def vector_mag(v):
    """Vector magnitude."""
    return np.sqrt(np.dot(v, v))


def vector_mag2(v):
    """Vector magnitude squared."""
    return np.dot(v, v)


def vector_angle(v):
    """Angle between v and the positive x axis.

    Only works with 2-D vectors.

    returns: angle in radians
    """
    assert len(v) == 2
    x, y = v
    return np.arctan2(y, x)


def vector_polar(v):
    """Vector magnitude and angle.

    returns: (number, angle in radians)
    """
    return vector_mag(v), vector_angle(v)


def vector_hat(v):
    """Unit vector in the direction of v.

    returns: Vector or array
    """
    # check if the magnitude of the Quantity is 0
    mag = vector_mag(v)
    if mag == 0:
        return v
    else:
        return v / mag


def vector_perp(v):
    """Perpendicular Vector (rotated left).

    Only works with 2-D Vectors.

    returns: Vector
    """
    assert len(v) == 2
    x, y = v
    return Vector(-y, x)


def vector_dot(v, w):
    """Dot product of v and w.

    returns: number or Quantity
    """
    return np.dot(v, w)


def vector_cross(v, w):
    """Cross product of v and w.

    returns: number or Quantity for 2-D, Vector for 3-D
    """
    res = np.cross(v, w)

    if len(v) == 3:
        return Vector(*res)
    else:
        return res


def vector_proj(v, w):
    """Projection of v onto w.

    returns: array or Vector with direction of w and units of v.
    """
    w_hat = vector_hat(w)
    return vector_dot(v, w_hat) * w_hat


def scalar_proj(v, w):
    """Returns the scalar projection of v onto w.

    Which is the magnitude of the projection of v onto w.

    returns: scalar with units of v.
    """
    return vector_dot(v, vector_hat(w))


def vector_dist(v, w):
    """Euclidean distance from v to w, with units."""
    if isinstance(v, list):
        v = np.asarray(v)
    return vector_mag(v - w)


def vector_diff_angle(v, w):
    """Angular difference between two vectors, in radians.
    """
    if len(v) == 2:
        return vector_angle(v) - vector_angle(w)
    else:
        # TODO: see http://www.euclideanspace.com/maths/algebra/
        # vectors/angleBetween/
        raise NotImplementedError()