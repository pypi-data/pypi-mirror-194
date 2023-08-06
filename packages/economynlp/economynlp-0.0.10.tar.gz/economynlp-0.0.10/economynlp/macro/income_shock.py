from economynlp.macro.shock import *

class IncomeShock(Shock):
    def __init__(self, name, impact, duration, income_loss):
        super().__init__(name, impact, duration)
        self.income_loss = income_loss

    def adjust_income_loss(self, new_income_loss):
        self.income_loss = new_income_loss