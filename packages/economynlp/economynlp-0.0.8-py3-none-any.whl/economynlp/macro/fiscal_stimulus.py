from economynlp.macro.fiscal_policy import *

class FiscalStimulus(FiscalPolicy):
    """
Fiscal Stimulus（财政刺激）通常指政府采取的一系列财政政策措施，旨在增加政府支出、降低税收和/或提高社会福利开支，以刺激经济增长。以下是一些可能用来描述 Fiscal Stimulus 的特征：

政府支出：Fiscal Stimulus 的一个重要特征是政府增加支出，通常是通过投资基础设施、增加社会福利开支等方式实现的。
减税：Fiscal Stimulus 还可能包括减税措施，例如降低个人所得税、公司所得税和增值税等。
增加社会福利开支：政府可能增加社会福利开支，例如提高医疗保健、失业救济和福利津贴等。
刺激经济增长：Fiscal Stimulus 的最终目标是刺激经济增长。通过增加政府支出和/或降低税收，Fiscal Stimulus 可以刺激消费、投资和出口等方面的经济活动。
    """
    def __init__(self, government_spending, tax_cuts, social_welfare_spending,implementation, impact, funding, timing,budget, taxation, borrowing):
        super().__init__(implementation, impact, funding, timing,budget, taxation, borrowing)

        self.government_spending = government_spending
        self.tax_cuts = tax_cuts
        self.social_welfare_spending = social_welfare_spending
        
    def describe(self):
        print("Fiscal Stimulus is a series of fiscal policy measures taken by the government to increase government spending, reduce taxes, and/or increase social welfare spending to stimulate economic growth.")
        print("One important feature of Fiscal Stimulus is an increase in government spending, which is typically achieved through investing in infrastructure and increasing social welfare spending.")
        print("Fiscal Stimulus may also include tax-cut measures, such as reducing personal income tax, corporate income tax, and value-added tax.")
        print("The ultimate goal of Fiscal Stimulus is to stimulate economic growth. By increasing government spending and/or reducing taxes, Fiscal Stimulus can stimulate economic activities such as consumption, investment, and exports.")
