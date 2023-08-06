from economynlp.belief.rational_beliefs import *

class BeliefDistortions(RationalBeliefs):
    """
 Belief distortions refer to deviations from rational beliefs or expectations, which can lead to suboptimal decision-making. 
Belief distortions are characterized by the following features:

 Cognitive biases: Belief distortions can be caused by cognitive biases, which are systematic errors in thinking that can 
lead to inaccurate beliefs or judgments. Examples of cognitive biases include confirmation bias, anchoring bias, and 
overconfidence bias.
 Information asymmetry: Belief distortions can also arise from information asymmetry, where different individuals have 
different levels of information about a situation, leading to different beliefs or expectations.
 Herding behavior: Belief distortions can also be caused by herding behavior, where individuals or groups follow the beliefs 
or actions of others without fully considering the available information.
 Persistence: Belief distortions can persist even in the face of new information or evidence, due to factors such as sunk 
costs or emotional attachment to a belief.
 Economic impact: Belief distortions can have significant economic impacts, affecting decisions related to investments, 
consumption, and production.   
    """
    def __init__(self,initial_belief,objectivity,consistency,adaptability,transparency,economic_impact, cognitive_bias,information_asymmetry):
        super().__init__(initial_belief,objectivity,consistency,adaptability,transparency,economic_impact)
        self.cognitive_bias = cognitive_bias
        self.information_asymmetry=information_asymmetry

    def update(self, new_information):
        # Update the belief based on new information
        if self.cognitive_bias == "confirmation":
            # Confirmation bias - the new information is only accepted if it confirms
            # the existing belief
            if new_information == self.belief:
                self.belief *= 2
        elif self.cognitive_bias == "anchoring":
            # Anchoring bias - the new information is anchored to a previous belief or
            # expectation, leading to a distorted belief
            self.belief = (self.belief + new_information) / 2
        elif self.cognitive_bias == "overconfidence":
            # Overconfidence bias - the new information is overweighed or underweighed
            # due to overconfidence in one's own beliefs or abilities
            self.belief += new_information * 0.1

    def impact(self):
        # Compute the economic impact of the belief distortion
        # This is just a simple example calculation
        impact = self.belief / 100
        return impact
