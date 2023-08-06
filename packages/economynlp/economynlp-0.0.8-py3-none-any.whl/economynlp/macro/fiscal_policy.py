class FiscalPolicy:
    def __init__(self, implementation, impact, funding, timing,budget, taxation, borrowing):
        self.implementation = implementation
        self.impact = impact
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