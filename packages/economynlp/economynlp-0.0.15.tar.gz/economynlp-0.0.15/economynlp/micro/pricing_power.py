class PricingPower:
    """
 A pricing power, also known as pricing discretion or pricing authority, refers to the ability of a company or individual to set prices for their products or services without being constrained by market competition. Here are some characteristics of pricing power:

It is a form of market power that allows the holder to influence the price of goods or services.
It is often associated with companies that have a strong brand, a unique product or service, or a dominant market position.
It can result in higher profit margins and increased revenue for the holder.
It can be used to maintain price stability in a market or to prevent a race to the bottom in terms of pricing.
It can be a barrier to entry for new competitors, as they may not be able to match the pricing of the holder.
It can be limited by regulation, competition, or changes in market conditions.
   
    """
    def __init__(self, company, product, market_position, brand_strength):
        self.company = company
        self.product = product
        self.market_position = market_position
        self.brand_strength = brand_strength
        
    def has_pricing_power(self):
        if self.market_position == "dominant" or self.brand_strength == "strong":
            return True
        else:
            return False
        
    def increase_price(self, percentage):
        if self.has_pricing_power():
            self.product.price *= 1 + percentage/100
        else:
            raise ValueError("This company does not have pricing power.")
