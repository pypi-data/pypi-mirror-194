class Capital:
    """
 Capital in economics refers to the stock of physical goods used to produce other goods and services. Some of the characteristics of capital include:

Physical goods: Capital consists of physical goods such as machinery, equipment, buildings, and infrastructure.
Investment: Capital is acquired through investment in physical goods.
Productivity: Capital can increase productivity and economic output.
Depreciation: Capital goods can depreciate over time and require maintenance or replacement.   
    """
    def __init__(self, physical_goods, investment, productivity, depreciation):
        self.physical_goods = physical_goods
        self.investment = investment
        self.productivity = productivity
        self.depreciation = depreciation

    def describe_capital(self):
        print("Consists of physical goods such as machinery, equipment, buildings, and infrastructure:", self.physical_goods)
        print("Acquired through investment in physical goods:", self.investment)
        print("Can increase productivity and economic output:", self.productivity)
        print("Capital goods can depreciate over time and require maintenance or replacement:", self.depreciation)
