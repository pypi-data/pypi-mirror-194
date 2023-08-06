from economynlp.system.economic_system import *

class MarketEconomy(EconomicSystem):
    """
 A market economy is an economic system where the production and distribution of goods and services is determined by supply and demand in a free market. The main features of a market economy include:

 - Private property: Individuals and businesses have the right to own property and use it to produce goods and services for sale in the market.
 - Decentralized decision-making: Economic decisions are made by individuals and businesses based on their own self-interest and market signals, rather than being dictated by a central authority.
 - Price system: Prices are determined by supply and demand, which signals to producers and consumers the relative scarcity or abundance of goods and services.
 - Competition: Competition between producers helps to allocate resources efficiently and drive innovation.
 - Profit motive: The desire to earn profits provides an incentive for individuals and businesses to produce goods and services that are in demand in the market.
 - Minimal government intervention: The government's role is generally limited to maintaining the rule of law and protecting property rights, rather than intervening in the market.
These features allow for a dynamic and efficient allocation of resources, with market signals determining the production and distribution of goods and services. However, they can also lead to income inequality and other social problems, which may require government intervention to address.
    """
    def __init__(self,supply,demand,citizens, businesses,ownership, resource_allocation, government_intervention, labor_market):
        """
        Initializes a MarketEconomy object with the given name and citizens and businesses.

        :param name: A string representing the name of the market economy.
        :param citizens: A list of citizens who participate in the economy.
        :param businesses: A list of businesses that participate in the economy.
        """
        super().__init__(ownership, resource_allocation, government_intervention, labor_market)
        self.citizens = citizens
        self.businesses = businesses
        self.supply = supply
        self.demand = demand

    def get_demand(self, goods: str):
        """
        Returns the total demand for the specified goods by the citizens and businesses.

        :param goods: A string representing the name of the goods.
        :return: The total demand for the specified goods.
        """
        total_demand = 0
        for citizen in self.citizens:
            total_demand += citizen.get_demand(goods)
        for business in self.businesses:
            total_demand += business.get_demand(goods)
        return total_demand

    def get_supply(self, goods: str):
        """
        Returns the total supply of the specified goods by the businesses.

        :param goods: A string representing the name of the goods.
        :return: The total supply of the specified goods.
        """
        total_supply = 0
        for business in self.businesses:
            total_supply += business.get_supply(goods)
        return total_supply

    def set_price(self, goods: str, price: float):
        """
        Sets the price for the specified goods.

        :param goods: A string representing the name of the goods.
        :param price: A float representing the price of the goods.
        """
        for business in self.businesses:
            business.set_price(goods, price)
    def price(self):
        return (self.supply + self.demand) / 2

    def resource_allocation(self):
        return {"producer": self.supply, "consumer": self.demand}

    def competition(self):
        return "Competition is the driving force behind the market economy."

    def value_law(self, labor_time):
        return "The value of goods is determined by the labor time required to produce them."