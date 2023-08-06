def audited(func):
    """

    ### Example:
    ```
    @audited
    def my_function():
        # some code here
        pass

    my_function.audited = True

    ```
    """
    def wrapper(*args, **kwargs):
        if func.__dict__.get('audited'):
            return func(*args, **kwargs)
        else:
            raise Exception(f"{func.__name__} has not been audited.")
    return wrapper
