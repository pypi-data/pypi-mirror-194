def heterogeneous(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, (list, tuple, set)):
            if len(set([type(x) for x in result])) > 1:
                print("The result is heterogeneous.")
        elif isinstance(result, dict):
            if len(set([type(v) for v in result.values()])) > 1:
                print("The result is heterogeneous.")
        else:
            print("The result is not a collection type.")
        return result
    return wrapper
