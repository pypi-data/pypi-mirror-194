from economynlp.market.market import *

class LaborMarket(Market):
    def __init__(self, commodity,participants,labor_supply, labor_demand, wage_determination, market_imperfections):
        super().__init__(commodity,participants)
        self.labor_supply = labor_supply
        self.labor_demand = labor_demand
        self.wage_determination = wage_determination
        self.market_imperfections = market_imperfections

    def describe_labor_market(self):
        print("Factors affecting labor supply by workers:", self.labor_supply)
        print("Factors affecting labor demand by employers:", self.labor_demand)
        print("Wages determined by the intersection of labor supply and demand curves:", self.wage_determination)
        print("Market imperfections that affect labor markets:", self.market_imperfections)
