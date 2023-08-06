class HumanCapital:
    """
    Human capital in economics refers to the knowledge, skills, and abilities that individuals possess and can use to produce economic value. Some of the characteristics of human capital include:

Investment: Human capital is often acquired through investment in education, training, and work experience.
Productivity: Human capital can increase productivity and economic output.
Non-transferable: Human capital is non-transferable between individuals and can only be owned by the individual who possesses it.
Depreciation: Human capital can depreciate over time if it is not maintained or updated.
    """
    def __init__(self, investment, productivity, non_transferable, depreciation):
        self.investment = investment
        self.productivity = productivity
        self.non_transferable = non_transferable
        self.depreciation = depreciation

    def describe_human_capital(self):
        print("Acquired through investment in education, training, and work experience:", self.investment)
        print("Increases productivity and economic output:", self.productivity)
        print("Non-transferable between individuals:", self.non_transferable)
        print("Can depreciate over time if not maintained or updated:", self.depreciation)
