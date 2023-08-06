class RationalExpectations:
    """
 Rational expectations refer to expectations that are formed based on all available information, including past experience and knowledge of economic theory, and are consistent with the best available economic models. Rational expectations are characterized by the following features:

 Information efficiency: Rational expectations assume that all available information is efficiently incorporated into expectations, meaning that individuals do not systematically under- or over-react to new information.
 Economic models: Rational expectations are based on economic models that accurately capture the underlying economic relationships and behavior of agents in the economy.
 Consistency: Rational expectations are consistent with economic theory and do not contain internal contradictions or inconsistencies.
 Forward-looking: Rational expectations are forward-looking, meaning that they take into account future events and expectations, as well as current economic conditions.
 Economic impact: Rational expectations can lead to optimal decision-making and efficient market outcomes, with positive economic impacts.    
    """
    def __init__(self, initial_expectation, economic_model,information_efficiency,consistency,forward_looking,economic_impact):
        self.expectation = initial_expectation
        self.economic_model = economic_model
        self.information_efficiency=information_efficiency
        self.consistency=consistency
        self.forward_looking=forward_looking
        self.economic_impact=economic_impact

    def update(self, new_information):
        # Update the expectation based on new information and the economic model
        self.expectation = self.economic_model.predict(new_information)

    def impact(self):
        # Compute the economic impact of the rational expectation
        # This is just a simple example calculation
        impact = self.expectation / 100
        return impact
