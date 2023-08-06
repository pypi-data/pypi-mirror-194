class EconomicSystem:
    def __init__(self, ownership, resource_allocation, government_intervention, labor_market):
        self.ownership = ownership
        self.resource_allocation = resource_allocation
        self.government_intervention = government_intervention
        self.labor_market = labor_market

    def resource_distribution(self):
        return "The resource allocation mechanism is " + self.resource_allocation

    def government_role(self):
        return "The degree of government intervention is " + self.government_intervention

    def labor_market_type(self):
        return "The type of labor market is " + self.labor_market
