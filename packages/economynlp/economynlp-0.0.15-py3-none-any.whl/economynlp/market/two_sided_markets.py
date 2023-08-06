from economynlp.market.market import *

class TwoSidedMarkets(Market):
    """
Two-sided markets in economics refer to markets in which two distinct groups of customers interact with each other through a common platform or intermediary. Some of the characteristics of two-sided markets include:

Network effects: The value of the platform or intermediary increases as more users join, creating positive network effects.
Cross-group externalities: The behavior of one group affects the welfare of the other group, creating cross-group externalities.
Pricing strategies: Two-sided markets often involve complex pricing strategies, where one group of customers may be charged differently than the other group.
Multi-homing: Customers may use multiple platforms or intermediaries, creating competition between platforms.
    """
    def __init__(self, commodity,participants,network_effects, cross_group_externalities, pricing_strategies, multi_homing):
        super().__init__(commodity,participants)
        self.network_effects = network_effects
        self.cross_group_externalities = cross_group_externalities
        self.pricing_strategies = pricing_strategies
        self.multi_homing = multi_homing
    def describe_two_sided_markets(self):
        print("Positive network effects as more users join the platform or intermediary:", self.network_effects)
        print("Cross-group externalities where the behavior of one group affects the welfare of the other group:", self.cross_group_externalities)
        print("Complex pricing strategies where one group may be charged differently than the other group:", self.pricing_strategies)
        print("Multi-homing where customers may use multiple platforms or intermediaries:", self.multi_homing)
