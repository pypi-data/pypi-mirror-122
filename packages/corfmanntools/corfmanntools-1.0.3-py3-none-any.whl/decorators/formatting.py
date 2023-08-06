from functools import wraps


def precision(trailing_zeros=False, precision=3):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            rs = fn(*args, **kwargs)
            try:
                rs = "{value:.{precision}f}".format(
                    value=float(rs), precision=precision)
                if not trailing_zeros:
                    rs = rs.rstrip('0').rstrip('.')
                rs = float(rs)
            except (TypeError, ValueError):
                pass
            return rs
        return wrapper
    return decorator


