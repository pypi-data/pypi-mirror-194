from economynlp.macro.inequality.inequality import *

class EarningsInequality(Inequality):
    """
 Earnings inequality refers to the unequal distribution of income among individuals or groups within a society. Here are some characteristics of earnings inequality:

 It is a macroeconomic phenomenon that is measured at the national or global level.
 It is often caused by differences in education, skills, and experience among workers, as well as by differences in the  demand for certain types of labor.
 It can lead to social and economic disparities, such as poverty, social exclusion, and political instability.
 It can be measured using various indicators, such as the Gini coefficient and the ratio of the top 10% to the bottom 10% of earners.
 It can be influenced by government policies, such as progressive taxation and minimum wage laws.
 It can have both short-term and long-term effects on individuals and the economy.   
    """
    def __init__(self, gini_coefficient, top_10_percent_income_ratio, cause_of_inequality,distribution, persistence, factors, impact):
        super().__init__(distribution, persistence, factors, impact)
        self.gini_coefficient = gini_coefficient
        self.top_10_percent_income_ratio = top_10_percent_income_ratio
        self.cause_of_inequality = cause_of_inequality
        
    def is_high(self):
        if self.gini_coefficient > 0.4:
            return True
        else:
            return False
        
    def is_caused_by_education(self):
        if self.cause_of_inequality == "education":
            return True
        else:
            return False
