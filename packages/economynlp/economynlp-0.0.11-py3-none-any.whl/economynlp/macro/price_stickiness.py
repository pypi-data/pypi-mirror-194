class PriceStickiness:
    """
 Price stickiness refers to the tendency of prices to remain fixed or change slowly in response to changes in supply and demand. Price stickiness is characterized by the following features:

 Inertia: Prices tend to remain fixed in the short run due to inertia or a reluctance to adjust prices too frequently. This can be due to factors such as menu costs, which are the costs associated with changing prices, or psychological factors that make price changes difficult.
 Market power: Prices may also be sticky due to market power, which occurs when a firm has the ability to set prices above the competitive level. In this case, the firm may be able to maintain its price even in the face of changes in supply and demand.
 Uncertainty: Prices may also be sticky due to uncertainty about the market, such as uncertainty about future demand or cost changes. Firms may be reluctant to adjust prices until they have a better understanding of the market conditions.
 Economic impact: Price stickiness can have significant economic impacts, including slower adjustments to changes in supply and demand, and potentially leading to market inefficiencies.
    
    """
    def __init__(self, price, market_power):
        self.price = price
        self.market_power = market_power

    def adjust(self, demand, cost):
        # Adjust the price based on changes in demand and cost
        if not self.market_power:
            # If the firm does not have market power, adjust the price
            # based on changes in demand and cost
            new_price = demand - cost
            self.price = max(new_price, 0)
        else:
            # If the firm has market power, maintain the price
            # above the competitive level
            competitive_price = cost
            self.price = max(self.price, competitive_price)

    def impact(self):
        # Compute the economic impact of price stickiness
        # This is just a simple example calculation
        impact = self.price / 10
        return impact
