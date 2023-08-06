def secret_decorator(secret_level):
    """
### Example:
```
@secret_decorator(secret_level=3)
def my_function():
    # 在此执行您的机密操作
    pass
```
    """
    def actual_decorator(function):
        def wrapper(*args, **kwargs):
            if secret_level > 5:
                raise Exception("Access Denied: You do not have the required clearance level.")
            result = function(*args, **kwargs)
            return result
        return wrapper
    return actual_decorator
