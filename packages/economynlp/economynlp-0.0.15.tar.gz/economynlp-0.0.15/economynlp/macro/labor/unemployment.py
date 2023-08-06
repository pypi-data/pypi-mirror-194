class Unemployment:
    """
 Unemployment refers to the state of being without a job but actively seeking employment. Here are some characteristics of unemployment:

It is a macroeconomic phenomenon that is measured at the national level.
It is often caused by a lack of demand for labor or changes in the structure of the economy.
It can lead to decreased economic growth and social instability.
It can be classified into different types, such as cyclical, structural, and frictional unemployment.
It can be measured using various indicators, such as the unemployment rate and the labor force participation rate.
It can have both short-term and long-term effects on individuals and the economy.
   
    """
    def __init__(self, unemployment_rate, labor_force_participation_rate, type_of_unemployment):
        self.unemployment_rate = unemployment_rate
        self.labor_force_participation_rate = labor_force_participation_rate
        self.type_of_unemployment = type_of_unemployment
        
    def is_high(self):
        if self.unemployment_rate > 6:
            return True
        else:
            return False
        
    def is_structural(self):
        if self.type_of_unemployment == "structural":
            return True
        else:
            return False
