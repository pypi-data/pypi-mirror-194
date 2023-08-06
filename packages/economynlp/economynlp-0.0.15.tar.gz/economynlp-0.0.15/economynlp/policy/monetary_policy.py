from economynlp.policy.economic_policy import *

class MonetaryPolicy(EconomicPolicy):
    """
 "Monetary Policy" 是指中央银行利用货币政策工具来影响货币供应和利率水平，从而达到控制经济发展和通货膨胀的目的。以下是一些可能用来描述 Monetary Policy 的特征：

货币供应：货币政策通过控制货币供应量来影响经济的发展和通货膨胀水平。
利率水平：货币政策还可以通过调整利率水平来影响经济的发展和通货膨胀水平。
货币政策工具：中央银行使用的货币政策工具包括公开市场操作、政策利率、准备金要求等。
目标：货币政策的目标通常包括保持通货稳定、促进经济增长和最大化就业等。
   
    """
    def __init__(self, money_supply, interest_rate, targets,goal, tool, trade_off, political_context):
        super().__init__(goal, tool, trade_off, political_context)
        self.money_supply = money_supply
        self.interest_rate = interest_rate
        self.targets = targets
