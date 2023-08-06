def welfare_effects(effects):
    """
    ### Example:
    ```
    @welfare_effects("consumer surplus")
    def calculate_price(price, demand_curve):
        quantity = demand_curve(price)
        consumer_surplus = 0.5 * (demand_curve(0) - demand_curve(price)) * quantity
        return consumer_surplus
    
    result = calculate_price(10, lambda p: 100 - 2*p)  # 输出: Welfare effects of consumer surplus: 400.0

    ```
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 执行原始函数并获取结果
            result = func(*args, **kwargs)
            
            # 打印福利效果的影响
            print(f"Welfare effects of {effects}: {result}")
            
            # 返回原始函数的结果
            return result
        return wrapper
    return decorator
