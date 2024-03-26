import inspect
import time


def helper(func, name):
    def wrapper(*args, **kwargs):
        print(f"`{name}` started")
        start = time.time_ns()
        result = func(*args, **kwargs)
        end = time.time_ns() - start
        print(f"`{name}` finished in {end / 1000000000}s")
        return result

    return wrapper


def profile(func_or_class):
    is_class = inspect.isclass(func_or_class)
    if is_class:
        for i, _ in inspect.getmembers(func_or_class, predicate=inspect.isfunction):
            setattr(
                func_or_class,
                i,
                helper(getattr(func_or_class, i), f"{func_or_class.__name__}.{i}"),
            )
        return func_or_class
    else:
        return helper(func_or_class, func_or_class.__name__)
