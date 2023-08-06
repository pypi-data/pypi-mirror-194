class SovereignRisk:
    """
The characteristics of sovereign risk are:

Sovereign risk refers to the risk that a government will default on its financial obligations, such as its sovereign debt.
This risk is influenced by a range of factors, including a country's economic and political stability, its debt levels, and its ability to generate revenue.
The credit rating of a country is often used as a measure of its sovereign risk.
Sovereign risk can have significant impacts on the economy of the country and the broader global financial system.    
    """
    def __init__(self, country, credit_rating, debt_to_GDP_ratio, political_stability):
        self.country = country
        self.credit_rating = credit_rating
        self.debt_to_GDP_ratio = debt_to_GDP_ratio
        self.political_stability = political_stability

    def assess_risk(self):
        if self.credit_rating == "AAA" and self.debt_to_GDP_ratio < 60 and self.political_stability == "Stable":
            return "Low risk"
        elif self.credit_rating in ["AA", "A"] and self.debt_to_GDP_ratio < 90 and self.political_stability in ["Stable", "Somewhat stable"]:
            return "Moderate risk"
        elif self.credit_rating in ["BBB", "BB", "B"] and self.debt_to_GDP_ratio < 120 and self.political_stability in ["Stable", "Somewhat stable", "Unstable"]:
            return "High risk"
        else:
            return "Very high risk"
