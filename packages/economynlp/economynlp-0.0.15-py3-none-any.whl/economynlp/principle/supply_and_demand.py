class SupplyAndDemand:
    """
 The Law of Supply and Demand is a fundamental principle in economics that states that the price of a good or service will tend to adjust to bring the quantity supplied and quantity demanded into balance. Some of the characteristics of the Law of Supply and Demand include:

 Inverse relationship: There is an inverse relationship between the price of a good or service and the quantity demanded. As the price increases, the quantity demanded will decrease, and vice versa.
 Direct relationship: There is a direct relationship between the price of a good or service and the quantity supplied. As the price increases, the quantity supplied will also increase.
 Equilibrium price: The Law of Supply and Demand predicts that there will be an equilibrium price at which the quantity supplied equals the quantity demanded, resulting in a market in balance.
    
    """
    def __init__(self, inverse_relationship, direct_relationship, equilibrium_price):
        self.inverse_relationship = inverse_relationship
        self.direct_relationship = direct_relationship
        self.equilibrium_price = equilibrium_price

    def describe_supply_and_demand(self):
        print("There is an inverse relationship between the price of a good or service and the quantity demanded:", self.inverse_relationship)
        print("There is a direct relationship between the price of a good or service and the quantity supplied:", self.direct_relationship)
        print("The Law of Supply and Demand predicts that there will be an equilibrium price at which the quantity supplied equals the quantity demanded, resulting in a market in balance:", self.equilibrium_price)
