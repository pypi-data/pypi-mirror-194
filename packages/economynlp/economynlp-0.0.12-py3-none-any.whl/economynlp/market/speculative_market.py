from economynlp.market.market import *
class SpeculativeMarket(Market):
    """
"Speculative markets" refer to markets where participants buy or sell assets with the expectation of making a profit based on anticipated price changes, rather than based on the intrinsic value of the assets. Some of the characteristics of speculative markets are:

High volatility: Prices in speculative markets can fluctuate rapidly and dramatically based on investor sentiment, news, and other factors unrelated to the underlying value of the asset.
High risk: Investing in speculative markets carries a high degree of risk because the price of the asset may not be justified by its fundamental value and may be subject to sudden and unpredictable changes.
Lack of liquidity: Assets in speculative markets may be difficult to buy or sell quickly, particularly during times of market stress.    
    """
    def __init__(self, commodity,participants,volatility,risk,liquidity):
        super().__init__(commodity,participants)
        self.volatility=volatility
        self.risk=risk
        self.liquidity=liquidity
    def set_price(self, new_price):
        self.price = new_price

    def get_price(self):
        return self.price
