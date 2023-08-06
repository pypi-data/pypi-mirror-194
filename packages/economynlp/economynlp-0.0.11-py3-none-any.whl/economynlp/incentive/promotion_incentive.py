from economynlp.incentive.incentive import *

class PromotionIncentive(Incentive):
    def __init__(self, officials,type, amount, recipients):
        super().__init__(type, amount, recipients)
        self.officials = officials
        self.performance_criteria = {}  # a dictionary to store performance criteria for each official
        self.promotion_criteria = {}  # a dictionary to store promotion criteria for each official
        self.promotion_results = {}  # a dictionary to store promotion results for each official

    def set_performance_criteria(self, official, criteria):
        self.performance_criteria[official] = criteria

    def set_promotion_criteria(self, official, criteria):
        self.promotion_criteria[official] = criteria

    def evaluate_officials(self):
        for official in self.officials:
            performance_score = self.performance_criteria[official]()
            if performance_score >= self.promotion_criteria[official]:
                self.promotion_results[official] = True
            else:
                self.promotion_results[official] = False

    def promote_officials(self):
        for official in self.officials:
            if self.promotion_results[official]:
                # do something to promote the official, such as increasing salary or giving a new job title
                pass
