class EmploymentStructure:
    """
 Employment structure in economics refers to the distribution of employment across different industries or sectors of the economy. Some of the characteristics of employment structure include:

Sectoral distribution: Employment structure reflects the sectoral distribution of employment across different industries such as manufacturing, services, and agriculture.
Skill level: Employment structure can reflect the skill level of the workforce in different industries.
Structural change: Employment structure can change over time due to shifts in the economy, such as technological advancements or changes in consumer demand.
Policy implications: Employment structure can have policy implications, such as the need for training programs to address skill gaps or support for industries experiencing job losses.   
    """
    def __init__(self, sectoral_distribution, skill_level, structural_change, policy_implications):
        self.sectoral_distribution = sectoral_distribution
        self.skill_level = skill_level
        self.structural_change = structural_change
        self.policy_implications = policy_implications

    def describe_employment_structure(self):
        print("Reflects the sectoral distribution of employment across different industries:", self.sectoral_distribution)
        print("Can reflect the skill level of the workforce in different industries:", self.skill_level)
        print("Can change over time due to shifts in the economy, such as technological advancements or changes in consumer demand:", self.structural_change)
        print("Can have policy implications, such as the need for training programs to address skill gaps or support for industries experiencing job losses:", self.policy_implications)
