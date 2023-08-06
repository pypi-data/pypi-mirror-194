class TobinTaxes:
    """
Tobin Taxes are a type of financial transaction tax that is designed to discourage short-term speculative trading in financial markets. The tax is named after James Tobin, an economist who proposed the idea in the 1970s.

A Tobin Tax is typically levied on the exchange of one currency for another, and is calculated as a small percentage of the transaction value. The goal of the tax is to reduce the volatility of financial markets and prevent sudden and sharp movements in exchange rates. The tax is also intended to discourage speculative trading, which can destabilize markets and create bubbles.    
    """
    def __init__(self, tax_rate):
        self.tax_rate = tax_rate
        
    def adjust_tax_rate(self, new_tax_rate):
        self.tax_rate = new_tax_rate
        
    def calculate_tax(self, transaction_value):
        # calculate the amount of Tobin Tax on a given transaction
        return transaction_value * self.tax_rate
        
    def apply_tax(self, transaction_value):
        # apply the Tobin Tax to a given transaction
        return transaction_value + self.calculate_tax(transaction_value)
