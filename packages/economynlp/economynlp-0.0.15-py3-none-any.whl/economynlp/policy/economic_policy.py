class EconomicPolicy:
    """
Economic policy refers to the actions and decisions taken by governments, central banks, and other policymakers to achieve specific economic goals and address economic issues. Economic policy is characterized by the following features:

Goals: Economic policy is designed to achieve specific economic goals, such as price stability, full employment, economic growth, and income redistribution.
Tools: Economic policy relies on a variety of tools and instruments, including monetary policy, fiscal policy, and regulatory policy, to achieve its goals.
Trade-offs: Economic policy involves trade-offs between different economic objectives, as policymakers often need to prioritize some goals over others.
Political context: Economic policy is shaped by the political context in which it is implemented, as policymakers need to take into account the preferences and interests of different stakeholders and interest groups.
Economic impact: Economic policy can have significant economic impacts, both positive and negative, on different segments of the economy and society.
    """
    def __init__(self, goal, tool, trade_off, political_context):
        self.goal = goal
        self.tool = tool
        self.trade_off = trade_off
        self.political_context = political_context

    def impact(self):
        # Compute the economic impact of the policy
        # This is just a simple example calculation
        impact = (self.goal + self.tool + self.trade_off +
                  self.political_context) / 100
        return impact
