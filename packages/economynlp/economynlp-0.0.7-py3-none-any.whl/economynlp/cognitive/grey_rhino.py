class GreyRhino:
    """
    In economics, a "grey rhino" refers to a highly probable, high-impact yet neglected threat that is often ignored or downplayed due to its seemingly obvious nature. The characteristics of a grey rhino include:

    High probability: Unlike a black swan event, a grey rhino is a predictable and probable threat. It is not a matter of if it will happen, but when.
    High impact: Grey rhinos have the potential to cause significant damage to the economy and society as a whole. They can be large-scale problems that can result in global crises.
    Neglected or downplayed: Despite their high probability and impact, grey rhinos often go unrecognized or are ignored due to their seemingly obvious nature. People tend to believe that these risks are easily manageable and not worth addressing.
    Complex and interconnected: Grey rhinos are often complex, systemic problems that are deeply interconnected with other issues. They can be difficult to solve without addressing the underlying causes and related issues.
    Often require urgent action: Once a grey rhino has been identified, it usually requires immediate attention and action to avoid its impact.
    In economics, the concept of a grey rhino was introduced by Michele Wucker to emphasize the importance of recognizing and addressing obvious but neglected risks before they become crises.
    """
    def __init__(self):
        self.high_probability = True
        self.high_impact = True
        self.neglected_or_downplayed = True
        self.complex_and_interconnected = True
        self.often_require_urgent_action = True

    def address_threat(self, threat):
        # 判断是否是高概率的高影响威胁
        if threat.is_high_probability() and threat.is_high_impact():
            # 判断是否被忽视或低估
            if threat.is_neglected_or_downplayed():
                # 判断是否复杂且相互关联
                if threat.is_complex_and_interconnected():
                    # 灰犀牛事件通常需要紧急处理
                    threat.take_urgent_action()
