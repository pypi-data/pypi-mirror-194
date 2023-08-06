class Inequality:
    """
 Inequality in economics refers to the unequal distribution of resources, income, and wealth among individuals or groups in a society. Some of the characteristics of inequality in economics include:

Unequal distribution: Inequality exists when some individuals or groups have more resources, income, or wealth than others.
Persistence: Inequality can persist over time, even across generations.
Social and economic factors: Inequality can be influenced by social and economic factors such as race, gender, education, and occupation.
Impact on well-being: Inequality can have negative effects on well-being, including physical and mental health, educational outcomes, and social mobility.   
    """
    def __init__(self, distribution, persistence, factors, impact):
        self.distribution = distribution
        self.persistence = persistence
        self.factors = factors
        self.impact = impact

    def describe_inequality(self):
        print("Distribution of resources, income, and wealth:", self.distribution)
        print("Persistence of inequality over time:", self.persistence)
        print("Social and economic factors influencing inequality:", self.factors)
        print("Impact of inequality on well-being:", self.impact)
