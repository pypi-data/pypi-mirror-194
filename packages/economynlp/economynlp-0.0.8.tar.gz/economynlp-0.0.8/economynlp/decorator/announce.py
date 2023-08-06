def announce(something):
    """
    ### Example:
    ```
    @announce("We are expanding our product line!")
    def my_function():
        # some code here
        pass
    
    my_function()
    ```
    
       
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            print(f"Company Announcement: {something}")
            result = func(*args, **kwargs)
            print(f"{func.__name__} has been executed.")
            return result
        return inner
    return wrapper
