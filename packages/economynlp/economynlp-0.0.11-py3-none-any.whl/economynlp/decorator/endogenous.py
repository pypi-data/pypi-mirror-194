def endogenous(func):
    """
### Example:
```
@endogenous
def my_function(x, y):
    z = x + y
    return z

result = my_function(3, 4)

```
    """
    def wrapper(*args, **kwargs):
        # 在函数执行前，打印提示信息
        print("The following variable(s) or function(s) are endogenous:")
        print(args)
        print(kwargs)
        # 执行原函数
        return func(*args, **kwargs)
    return wrapper
