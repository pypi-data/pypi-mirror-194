class SupplyCurve:
    """
 Supply curves in economics describe the relationship between the quantity of a good that producers are willing to supply and the price of that good in the market. Some of the characteristics of supply curves include:

Positive slope: Supply curves have a positive slope, indicating that producers are willing to supply more of a good as the price of that good increases.
Law of supply: The law of supply states that there is a direct relationship between price and quantity supplied, meaning that as price increases, quantity supplied also increases.
Shifts in supply: The supply curve can shift to the left or right due to changes in factors such as input costs, technology, and government policies.
Elasticity: The elasticity of supply measures how responsive the quantity supplied is to changes in price.   
    """
    def __init__(self, slope, law_of_supply, shift_factors, elasticity):
        self.slope = slope
        self.law_of_supply = law_of_supply
        self.shift_factors = shift_factors
        self.elasticity = elasticity

    def describe_supply_curve(self):
        print("Positive slope indicating that producers are willing to supply more as price increases:", self.slope)
        print("Law of supply: direct relationship between price and quantity supplied:", self.law_of_supply)
        print("Factors that can shift the supply curve to the left or right:", self.shift_factors)
        print("Elasticity of supply measures the responsiveness of quantity supplied to changes in price:", self.elasticity)
