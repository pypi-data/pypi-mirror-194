from economynlp.market.market import *

class MarketAccess(Market):
    """
Market access refers to the ability of a country or group of countries to enter and participate in the markets of other countries. Market access is characterized by the following features:

Trade barriers: Market access can be hindered by various trade barriers, including tariffs, quotas, and regulatory restrictions that limit or prohibit foreign market entry.
Reciprocity: Market access is often subject to the principle of reciprocity, which means that a country will only grant access to its own markets if it receives equivalent access to the markets of other countries.
Negotiation: Market access is typically negotiated through trade agreements and treaties, which aim to reduce trade barriers and promote freer and fairer trade.
Economic impact: Market access has significant economic implications, as it can facilitate or hinder trade and investment flows, and affect the competitiveness and growth of domestic industries.    
    """
    def __init__(self,commodity,participants,country, trade_partners):
        super().__init__(commodity,participants)
        self.country = country
        self.trade_partners = trade_partners

    def negotiate(self, trade_partner, concessions):
        # Negotiate market access with a trade partner
        # by offering concessions
        if trade_partner in self.trade_partners:
            self.trade_partners[trade_partner] += concessions

    def impact(self):
        # Compute the economic impact of the country's
        # market access situation
        # This is just a simple example calculation
        total_concessions = sum(self.trade_partners.values())
        impact = total_concessions / 100
        return impact
