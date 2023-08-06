from economynlp.micro.supply_curve import *

class ConvexSupplyCurve(SupplyCurve):
    def __init__(self, increasing_marginal_cost, decreasing_marginal_returns, diminishing_supply_elasticity, nonlinear_relationship,slope, law_of_supply, shift_factors, elasticity):
        super().__init__(slope, law_of_supply, shift_factors, elasticity)
        self.increasing_marginal_cost = increasing_marginal_cost
        self.decreasing_marginal_returns = decreasing_marginal_returns
        self.diminishing_supply_elasticity = diminishing_supply_elasticity
        self.nonlinear_relationship = nonlinear_relationship

    def describe_convex_supply_curve(self):
        print("Increasing marginal cost of producing each additional unit:", self.increasing_marginal_cost)
        print("Decreasing marginal returns as more units are produced:", self.decreasing_marginal_returns)
        print("Diminishing supply elasticity due to diminishing marginal returns:", self.diminishing_supply_elasticity)
        print("Nonlinear relationship between quantity supplied and price with a positive but diminishing slope:", self.nonlinear_relationship)
