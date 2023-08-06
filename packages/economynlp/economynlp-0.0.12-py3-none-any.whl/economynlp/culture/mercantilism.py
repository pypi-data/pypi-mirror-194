class Mercantilism:
    """
    - Favorable balance of trade: Mercantilists believed that a country should maintain a trade surplus, or export more goods than it imported, in order to accumulate wealth and maintain national power.
    - Protectionist policies: Mercantilists advocated for high tariffs, or taxes on imported goods, to protect domestic industries from foreign competition.
    - State intervention in the economy: Mercantilists believed that the state should play an active role in promoting economic growth and development, through measures such as subsidies, monopolies, and regulation.
    Gold and silver reserves: Mercantilists believed that a country's wealth and power were determined by the amount of gold and silver it possessed, and thus advocated for policies that promoted the accumulation of precious metals.
    - Colonization: Mercantilists believed that colonies could provide a source of cheap raw materials and a captive market for manufactured goods, and thus encouraged colonization and the establishment of overseas empires.
    - In summary, mercantilism is characterized by an emphasis on trade surpluses, protectionist policies, state intervention in the economy, the accumulation of gold and silver reserves, and colonization.
    
    ### Example:
    ```
    mercantilism = Mercantilism("England", True, True, True, True, True)
    mercantilism.print_features()
    ```
    
    
    """
    def __init__(self, country, trade_surplus, tariffs, state_intervention, gold_silver_reserves, colonization):
        self.country = country
        self.trade_surplus = trade_surplus
        self.tariffs = tariffs
        self.state_intervention = state_intervention
        self.gold_silver_reserves = gold_silver_reserves
        self.colonization = colonization

    def print_features(self):
        print("Mercantilism is an economic theory and practice that emphasizes the following features:")
        print("- Favorable balance of trade: countries should maintain a trade surplus to accumulate wealth and power.")
        print("- Protectionist policies: high tariffs on imported goods protect domestic industries from foreign competition.")
        print("- State intervention in the economy: the state should play an active role in promoting economic growth and development.")
        print("- Gold and silver reserves: a country's wealth and power is determined by the amount of precious metals it possesses.")
        print("- Colonization: colonies provide a source of cheap raw materials and a captive market for manufactured goods.")
