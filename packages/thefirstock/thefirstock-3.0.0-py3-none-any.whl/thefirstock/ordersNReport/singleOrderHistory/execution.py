class FirstockSingleOrderHistory:
    def __init__(self, orderNumber):
        self.singleOrderHistory = ApiRequests()

        self.orderNumber = orderNumber

    def firstockSingleOrderHistory(self):
        result = self.singleOrderHistory.firstockSingleOrderHistory(self.orderNumber)
        return result
