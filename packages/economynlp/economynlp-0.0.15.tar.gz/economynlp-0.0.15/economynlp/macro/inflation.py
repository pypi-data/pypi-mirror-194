class Inflation:
    """
    Inflation refers to a sustained increase in the general price level of goods and services in an economy over time. Here are some characteristics of inflation:

It is a macroeconomic phenomenon that affects the overall economy and is measured at the national level.
It is often caused by an increase in the supply of money in circulation or a decrease in the supply of goods and services.
It can lead to a decrease in the purchasing power of money and a rise in the cost of living.
It can be classified into different types, such as demand-pull, cost-push, and built-in inflation.
It can be measured using various indicators, such as the consumer price index (CPI) and the producer price index (PPI).
It can have both short-term and long-term effects on individuals and the economy.
    """
    def __init__(self, inflation_rate, type_of_inflation, measurement_indicator):
        self.inflation_rate = inflation_rate
        self.type_of_inflation = type_of_inflation
        self.measurement_indicator = measurement_indicator
        
    def is_high(self):
        if self.inflation_rate > 5:
            return True
        else:
            return False
        
    def is_demand_pull(self):
        if self.type_of_inflation == "demand-pull":
            return True
        else:
            return False
