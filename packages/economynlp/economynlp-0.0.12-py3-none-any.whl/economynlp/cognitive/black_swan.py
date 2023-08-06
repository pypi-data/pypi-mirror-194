class BlackSwan:
    def __init__(self):
        self.rare = True
        self.impactful = True
        self.post_hoc_explained = True
        self.mind_changing = True

    def evaluate(self, event):
        if event.is_rare() and event.is_impactful():
            # 对经济系统产生深远的影响
            event.affect_economy()
            if not event.is_predicted():
                # 事后容易被解释
                event.explain_post_hoc()
                # 可能会改变我们的信仰和认知
                event.change_mind()
