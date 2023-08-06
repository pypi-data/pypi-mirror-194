from economynlp.system.market_economy import *

class ChineseSocialistMarketEconomy(MarketEconomy):
    """
Characteristics of the socialist market economy with Chinese characteristics include:

Combination of public ownership and market mechanism: The Chinese socialist market economy combines public ownership of key industries and resources with market mechanism. This means that while the state maintains ownership of key industries such as energy, telecommunications, and finance, market forces are allowed to allocate resources and determine prices.
State intervention and guidance: The government plays an active role in guiding economic development through various policies and regulations. This includes industrial planning, investment in infrastructure, and support for strategic industries.
Emphasis on social welfare: The Chinese socialist market economy places a strong emphasis on social welfare, with the government providing healthcare, education, and social security to its citizens. This is in line with the principle of "people-centered" development.
Openness to the world: China has actively pursued opening up to the world and integrating into the global economy. This includes participating in international trade and investment, as well as promoting cross-border flows of goods, services, and capital.


    """
    def __init__(self, public_ownership, market_mechanism,state_intervention, social_welfare, openness,supply,demand,citizens, businesses,ownership, resource_allocation, government_intervention, labor_market):
        super().__init__(supply,demand,citizens, businesses,ownership, resource_allocation, government_intervention, labor_market)
        self.public_ownership = public_ownership
        self.market_mechanism = market_mechanism
        self.state_intervention = state_intervention
        self.social_welfare = social_welfare
        self.openness = openness
    
    def allocate_resources(self):
        if self.market_mechanism:
            return "Resources are allocated based on market forces."
        else:
            return "Resources are allocated based on government planning."
    
    def provide_social_welfare(self):
        if self.social_welfare:
            return "The government provides healthcare, education, and social security."
        else:
            return "Social welfare is not a priority."
    
    def promote_openness(self):
        if self.openness:
            return "China is actively integrating into the global economy."
        else:
            return "China is closed off from the world."
