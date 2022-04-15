def whenthen(func):
    whenthen_data = []

    def wrapper(*args, **kwargs):
        for cond in whenthen_data:
            if cond[0](*args, **kwargs) is True:
                return cond[1](*args, **kwargs)
        return func(*args, **kwargs)

    def when(whenfunc):
        if (len(whenthen_data) != 0) and (
            len(whenthen_data[-1]) != 2
        ):  # 2 when's in a row
            raise ValueError
        whenthen_data.append([whenfunc])
        return wrapper

    def then(thenfunc):
        if len(whenthen_data[-1]) != 1:  # 2 then's in a row or no when
            raise ValueError
        whenthen_data[-1].append(thenfunc)
        return wrapper

    wrapper.when = when
    wrapper.then = then
    return wrapper
