class CapitalAccumulation:
    """
 Capital accumulation in economics refers to the process of increasing the stock of capital goods in an economy through investment. Some of the characteristics of capital accumulation include:

 Investment: Capital accumulation is achieved through investment in physical capital goods such as machinery, equipment, and buildings.
 Productivity: Increased capital accumulation can lead to increased productivity and economic growth.
 Diminishing returns: The marginal productivity of capital can decrease as more capital is accumulated, leading to diminishing returns.
 Time horizon: Capital accumulation is a long-term process that requires sustained investment over time.   
    """
    def __init__(self, investment, productivity, diminishing_returns, time_horizon):
        self.investment = investment
        self.productivity = productivity
        self.diminishing_returns = diminishing_returns
        self.time_horizon = time_horizon

    def describe_capital_accumulation(self):
        print("Achieved through investment in physical capital goods:", self.investment)
        print("Increased capital accumulation can lead to increased productivity and economic growth:", self.productivity)
        print("Marginal productivity of capital can decrease as more capital is accumulated, leading to diminishing returns:", self.diminishing_returns)
        print("Capital accumulation is a long-term process that requires sustained investment over time:", self.time_horizon)
