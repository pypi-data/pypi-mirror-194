class MinimumWage:
    """
    Minimum wage in economics refers to the legal minimum amount that employers must pay their employees for their labor services. Some of the characteristics of minimum wage include:

Legal requirement: Minimum wage is a legal requirement that sets a floor on wages.
Price floor: Minimum wage creates a price floor for wages, which can lead to unemployment or reduced hours for low-skilled workers.
Poverty reduction: Minimum wage can reduce poverty and improve the standard of living for low-wage workers.
Political debate: Minimum wage is often a topic of political debate, with some advocating for higher minimum wages to reduce poverty and others arguing that it can lead to unintended consequences such as job losses.
    """
    def __init__(self, legal_requirement, price_floor, poverty_reduction, political_debate):
        self.legal_requirement = legal_requirement
        self.price_floor = price_floor
        self.poverty_reduction = poverty_reduction
        self.political_debate = political_debate

    def describe_minimum_wage(self):
        print("Legal requirement that sets a floor on wages:", self.legal_requirement)
        print("Creates a price floor for wages, which can lead to unemployment or reduced hours for low-skilled workers:", self.price_floor)
        print("Can reduce poverty and improve the standard of living for low-wage workers:", self.poverty_reduction)
        print("Is often a topic of political debate:", self.political_debate)
