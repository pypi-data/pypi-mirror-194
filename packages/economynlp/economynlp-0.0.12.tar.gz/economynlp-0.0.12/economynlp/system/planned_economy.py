from economynlp.system.economic_system import *

class PlannedEconomy(EconomicSystem):
    def __init__(self, government,ownership, resource_allocation, government_intervention, labor_market):
        """
        Initializes a PlannedEconomy object with the given name and government.

        :param name: A string representing the name of the planned economy.
        :param government: An object representing the government in the planned economy.
        """
        super().__init__(ownership, resource_allocation, government_intervention, labor_market)
        self.government = government

    def get_demand(self, goods):
        """
        Returns the total demand for the specified goods as planned by the government.

        :param goods: A string representing the name of the goods.
        :return: The total demand for the specified goods as planned by the government.
        """
        return self.government.get_demand_plan(goods)

    def get_supply(self, goods):
        """
        Returns the total supply of the specified goods as planned by the government.

        :param goods: A string representing the name of the goods.
        :return: The total supply of the specified goods as planned by the government.
        """
        return self.government.get_supply_plan(goods)

    def set_price(self, goods, price):
        """
        Sets the price for the specified goods as planned by the government.

        :param goods: A string representing the name of the goods.
        :param price: A float representing the price of the goods as planned by the government.
        """
        self.government.set_price_plan(goods, price)
