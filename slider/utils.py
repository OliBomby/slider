from functools import lru_cache


class lazyval:
    """Decorator to lazily compute and cache a value.
    """
    def __init__(self, fget):
        self._fget = fget
        self._name = None

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = self._fget(instance)
        vars(instance)[self._name] =  value
        return value

    def __set__(self, instance, value):
        vars(instance)[self._name] = value


class no_default:
    """Sentinel type; this should not be instantiated.

    This type is used so functions can tell the difference between no argument
    passed and an explicit value passed even if ``None`` is a valid value.

    Notes
    -----
    This is implemented as a type to make functions which use this as a default
    argument serializable.
    """
    def __new__(cls):
        raise TypeError('cannot create instances of sentinel type')


memoize = lru_cache(None)


def accuracy(count_300, count_100, count_50, count_miss):
    """Calculate osu! standard accuracy from discrete hit counts.

    Parameters
    ----------
    count_300 : int
        The number of 300's hit.
    count_100 : int
        The number of 100's hit.
    count_50 : int
        The number of 50's hit.
    count_miss : int
        The number of misses

    Returns
    -------
    accuracy : float
        The accuracy in the range [0, 1]
    """
    points_of_hits = count_300 * 300 + count_100 * 100 + count_50 * 50
    total_hits = count_300 + count_100 + count_50 + count_miss
    return points_of_hits / (total_hits * 300)
