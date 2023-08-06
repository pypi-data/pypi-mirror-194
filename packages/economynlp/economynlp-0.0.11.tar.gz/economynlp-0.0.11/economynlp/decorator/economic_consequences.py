def economic_consequences(consequences):
    """
    ### Example:
    ```
    @economic_consequences("inflation")
    def calculate_price(price, inflation_rate):
        return price * (1 + inflation_rate)

    result = calculate_price(100, 0.02)  # 输出: Economic consequences of inflation: 102.0




    ```
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 执行原始函数并获取结果
            result = func(*args, **kwargs)
            
            # 打印经济后果
            print(f"Economic consequences of {consequences}: {result}")
            
            # 返回原始函数的结果
            return result
        return wrapper
    return decorator
