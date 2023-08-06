def spillover_effect(func):
    """
"溢出效应"和"影响"、"副作用"之间的区别在于，"溢出效应"通常是指市场交易活动中的效应，即一方的行为对其他方的福利产生的影响。而"影响"和"副作用"通常是更广泛的概念，不仅仅限于市场交易活动，还可以涉及到政策、技术等方面的效应和影响。
    """
    def wrapper(*args, **kwargs):
        # Call the original function
        result = func(*args, **kwargs)

        # Compute the spillover effect
        # This is just a simple example calculation
        spillover = result / 100

        # Print the spillover effect
        print(f"This action has a spillover effect of {spillover}")

        return result

    return wrapper
