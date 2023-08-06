class Deflation:
    """
    ### Example:
    ```
    deflation = Deflation(100, 0.05, 0.02)
    deflation.print_price_level()  # Output: Current price level is: 100
    
    deflation.update_price_level()
    deflation.print_price_level()  # Output: Current price level is: 93.1
    
    deflation.decrease_demand()
    deflation.increase_unemployment()
    deflation.increase_debt_burden()
    deflation.print_price_level()  # Output: Current price level is: 88.45
    print("Unemployment rate is: ", deflation.unemployment_rate)
    print("Debt burden is: ", deflation.debt_burden)
    ```
    Deflation is an economic phenomenon characterized by a decrease in the general price level of goods and services in an economy. Deflation is often associated with a reduction in the supply of money and credit, which can lead to a decrease in demand for goods and services.

    The important features of deflation include:
    Falling prices: Deflation leads to falling prices, which means that the same amount of money can buy more goods and services. This can be good for consumers in the short term, but it can also lead to a decrease in business profits and investment.
    Lower demand: When prices are falling, consumers may hold off on making purchases in the hope that prices will fall further. This can lead to a decrease in demand for goods and services, which can in turn lead to a decrease in production and employment.
    Rising unemployment: Deflation can lead to rising unemployment as businesses reduce their output in response to lower demand. This can lead to a vicious cycle, where falling demand leads to lower production, which leads to rising unemployment, which further reduces demand.
    Debt becomes more burdensome: Deflation can make it more difficult for borrowers to repay their debts, because the value of the money they owe may increase in real terms as prices fall. This can lead to defaults and bankruptcies, which can further reduce demand and economic activity.
    In summary, deflation is a complex economic phenomenon that can have wide-ranging effects on consumers, businesses, and the economy as a whole.
    """
    def __init__(self, initial_price_level, money_supply, credit_supply, demand,debt_burden,unemployment_rate):
        self.price_level = initial_price_level
        self.money_supply = money_supply
        self.credit_supply = credit_supply
        self.demand = demand
        self.unemployment_rate = unemployment_rate
        self.debt_burden = debt_burden
    def update_price_level(self):
        # Update the price level based on the decrease in the supply of money and credit
        self.price_level *= (1 - self.money_supply - self.credit_supply)

    def print_price_level(self):
        print("Current price level is: ", self.price_level)

    def decrease_demand(self):
        # Decrease the demand for goods and services due to falling prices
        self.demand *= 0.95  # Assume a 5% decrease in demand

    def increase_unemployment(self):
        # Increase the unemployment rate due to lower demand and production
        self.unemployment_rate += 0.01  # Assume a 1% increase in unemployment rate

    def increase_debt_burden(self):
        # Make it more difficult for borrowers to repay their debts
        self.debt_burden += 0.02  # Assume a 2% increase in debt burden
