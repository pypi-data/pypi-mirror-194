from economynlp.policy.economic_policy import *

class FiscalPolicy(EconomicPolicy):
    def __init__(self, goal, tool, trade_off, political_context,implementation, funding, timing,budget, taxation, borrowing):
        super().__init__(goal, tool, trade_off, political_context)
        self.implementation = implementation
        self.funding = funding
        self.timing = timing
        self.budget = budget
        self.taxation = taxation
        self.borrowing = borrowing
    
    def adjust_budget(self, new_budget):
        self.budget = new_budget
        
    def adjust_taxation(self, new_taxation):
        self.taxation = new_taxation
        
    def adjust_borrowing(self, new_borrowing):
        self.borrowing = new_borrowing