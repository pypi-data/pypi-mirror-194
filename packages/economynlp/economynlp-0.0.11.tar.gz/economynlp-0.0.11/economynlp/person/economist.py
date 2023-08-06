from economynlp.person.consumer import *

class Economist(Consumer):
    """
Economists are professionals who study the production, consumption, and distribution of goods and services, and the behavior of individuals, firms, and governments in the economy. Economists are characterized by the following features:

Knowledge of economic theory: Economists possess knowledge of economic theory, including microeconomics and macroeconomics, as well as specialized areas of study such as international trade, development economics, and behavioral economics.
Analytical skills: Economists possess analytical skills, including the ability to use quantitative methods and statistical analysis to study economic phenomena and test economic theories.
Data analysis: Economists are skilled in collecting, analyzing, and interpreting data relevant to economic questions and problems.
Policy expertise: Economists possess expertise in economic policy, including the design and evaluation of policies related to taxation, regulation, monetary policy, and international trade.
Communication skills: Economists possess strong communication skills, including the ability to communicate complex economic concepts and analyses to a wide range of audiences, including policymakers, business leaders, and the general public.    
    """
    def __init__(self, name, age, wealth,utility_function,area_of_expertise, analytical_skills, data_analysis_skills, policy_expertise, communication_skills):
        super().__init__(name, age, wealth,utility_function)
        self.area_of_expertise = area_of_expertise
        self.analytical_skills = analytical_skills
        self.data_analysis_skills = data_analysis_skills
        self.policy_expertise = policy_expertise
        self.communication_skills = communication_skills

    def impact(self):
        # Compute the impact of the economist
        # This is just a simple example calculation
        impact = (self.analytical_skills + self.data_analysis_skills +
                  self.policy_expertise + self.communication_skills) / 100
        return impact
