class Shock:
    """
在宏观经济学中，shock（冲击）通常指不可预测的、非周期性的经济事件，它可以破坏某种经济平衡状态，引起经济体的剧烈变化。以下是一些可能用来描述 shock 的特征：

突发性：shock 是不可预测的，通常突然发生。这使得经济体很难对它们做出反应，因为没有足够的时间来做出计划和准备。
意外性：shock 通常是意外的，而不是根据预期发生的。这意味着经济体的政策制定者可能没有准备好应对这些事件。
多样性：shock 可以是多种类型的，包括财政、货币、政治、自然等方面的。每种类型的 shock 都可能会对经济体产生不同的影响。
影响持久：shock 的影响可能会持续很长时间，这使得经济体必须采取措施来适应新的经济环境。    
    """
    def __init__(self, name, impact, duration):
        self.name = name
        self.impact = impact
        self.duration = duration
        
    def describe(self):
        print(f"{self.name} is an unpredictable event that can disrupt economic equilibrium and cause significant changes in the economy.")
        print(f"Shocks are often sudden and unexpected, making it difficult for the economy to react in time to plan and prepare for them.")
        print(f"Shocks can come in many different forms, including fiscal, monetary, political, natural, and other types.")
        print(f"The impact of shocks can be long-lasting, which requires the economy to take measures to adapt to the new economic environment.")
