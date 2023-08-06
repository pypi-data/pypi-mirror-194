class Buyer:
    def buy(self, item, price):
        print("我以", price, "元的价格买了", item)

class Seller:
    def sell(self, item, price):
        print("我以", price, "元的价格卖了", item)

def market(buyer, seller, item, price):
    seller.sell(item, price)
    buyer.buy(item, price)

def trading():
    buyer = Buyer()
    seller = Seller()
    market(buyer, seller, "苹果", 5)
