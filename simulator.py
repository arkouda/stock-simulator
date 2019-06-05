import random
import pylab

initialStockPrice = 2000

startingCapitalS = 20000

startingCapitalNS = 200000

limitBuyLowerBound = 0.88

limitSellLowerBound = 0.93

simulationLengthDays = 360

numberOfTraders = 1000

numberOfSimulations = 1

lblBias = random.uniform(0.00, 0.06)

lslBias = random.uniform(0.00, 0.07)

class Stock(object):
    def __init__(self, price):
        self.price = price   # >0
        self.marketBias = 0  # [-1, 1]
        self.buyOrders = {}   # {price:[(id,quantity)]}
        self.sellOrders = {}  # {price:[(id,quantity)]}
        self.orderHistory = []  # [(buyerID, sellerID, executedPrice, quantity, timeStamp, price)]
        self.d1 = 0
        self.d2 = 0
        self.d3 = 0
        self.d4 = 0
        self.d5 = 0
        self.d6 = 0
        self.d7 = 0

    def __setPrice(self, price):
        self.price = price

    def __setMarketBias(self, marketBias):
        self.marketBias = marketBias

    def getPrice(self):
        return self.price

    def alterPriceAndMarketBias(self):
        sellDict = {}
        buyDict = {}
        sellVolume = list(map(lambda x: sum(map(lambda y: y[1], x)), self.sellOrders.values()))
        buyVolume = list(map(lambda x: sum(map(lambda y: y[1], x)), self.buyOrders.values()))
        j=0
        for i in self.sellOrders:
            sellDict[i] = sellVolume[j]
            j += 1
        j = 0
        for i in self.buyOrders:
            buyDict[i] = buyVolume[j]
            j += 1
        if (not buyDict) and (not sellDict):
            newPrice = self.getPrice()
        elif not buyDict:
            newPrice = max(sellDict, key=sellDict.get)
        elif not sellDict:
            newPrice = max(buyDict, key=buyDict.get)
        else:
            newPrice = int((max(buyDict, key=buyDict.get) + max(sellDict, key=sellDict.get)) / 2)
        last50trades = list(map(lambda x: x[2], self.orderHistory[-100:]))
        prevLast50trades = list(map(lambda x: x[2], self.orderHistory[-200:-100]))
        if not prevLast50trades:
            newMarketBias = self.marketBias
        else:
            last50Mean = sum(last50trades) / len(last50trades)
            prevLast50Mean = sum(prevLast50trades) / len(prevLast50trades)
            newMarketBias = (last50Mean - prevLast50Mean) / prevLast50Mean
        self.__setPrice(newPrice)
        self.__setMarketBias(newMarketBias)


'''        if self.getPrice() > newPrice:
            newMarketBias = self.marketBias - (newPrice / self.getPrice())
        elif self.getPrice() < newPrice:
            newMarketBias = self.marketBias + (newPrice / self.getPrice())
        else:
            newMarketBias = self.marketBias

                for i in range(len(sellVolume)):
            sellVolume[i] *= sellPriceList[i]
        for i in range(len(buyVolume)):
            buyVolume[i] *= buyPriceList[i]
        sellVolume = sum(sellVolume)
        buyVolume = sum(buyVolume)
        buyPriceList.sort()
        sellPriceList.sort()
        volumeBias = (buyVolume - sellVolume) / buyVolume
        newPrice = (0.1 * (1 + volumeBias) + 0.45 * (buyPriceList[-1] + sellPriceList [-1])) * self.getPrice()
        newMarketBias = self.marketBias + ((newPrice - self.getPrice())/self.getPrice())

        buyPriceList = list(self.buyOrders.keys()).sort()
        sellPriceList = list(self.sellOrders.keys()).sort()

        '''

class Trader(object):
    def __init__(self, traderID, capital, stocksOwned, avgStockCost, riskTolerance, biasThreshold):
        self.traderID = traderID
        self.capital = capital
        self.stocksOwned = stocksOwned
        self.avgStockCost = avgStockCost
        self.riskTolerance = riskTolerance  # [0, 1] betavariate(3, 7)
        self.biasThreshold = biasThreshold  # [0, 1] betavariate(3, 7)
        self.liveOrders = []  # [(price, quantity, String - 'b' or 's')]
        # No Order Cancellation (for now)

    def setID(self, traderID):
        self.traderID = traderID

    def executeDecision(self, stockObject, intuitionStrength, decision):
        #print(decision)
        if decision == [[1]]:
            sellMarket(self.traderID, random.choice([int(random.betavariate(7, 3) * self.stocksOwned), self.stocksOwned]))
        elif decision == [[2]]:
            sellLimit(self.traderID, random.choice([int(random.betavariate(7, 3) * self.stocksOwned), self.stocksOwned]), getLimitSellPrice(stockObject.getPrice(), intuitionStrength))
        elif decision == [[3]]:
            buyMarket(self.traderID, int(random.uniform(0, self.capital / stockObject.getPrice())))
        else:
            buyLimit(self.traderID, int(random.uniform(0, self.capital / stockObject.getPrice())), getLimitBuyPrice(stockObject.getPrice(), intuitionStrength))

    def makeDecision(self, stockObject):
        tradeFrequency = random.choices([True, False], weights=[1, random.uniform(0, 30)])
        if not tradeFrequency[0]:
            return
        for (p, q, s) in self.liveOrders:
            if stockObject.getPrice() - p < 0.9 * stockObject.getPrice():
                if s is 's':
                    cancelSellOrder(self.traderID, p, q)
                else:
                    cancelBuyOrder(self.traderID, p, q)
        intuitionStrength = random.uniform(0, 1)
        randomSell = random.choices([1, 2], weights=[1 - intuitionStrength, intuitionStrength])
        randomBuy = random.choices([3, 4], weights=[intuitionStrength, 1 - intuitionStrength])
        if self.stocksOwned > 0:                                            # if stocks owned
            if self.avgStockCost >= stockObject.getPrice():                 # when in profit
                if stockObject.marketBias > self.biasThreshold:             # market perception of trader is bullish
                    gso.d1 += 1
                    self.executeDecision(stockObject, intuitionStrength, random.choices([randomBuy, randomSell], weights=[4, 6]))
                    return
                else:                                                       # market perception of trader in stable zone
                    gso.d2 += 1
                    self.executeDecision(stockObject, intuitionStrength, random.choices([randomBuy, randomSell], weights=[6, 4]))
                    return
            else:                                                           # when in loss
                riskPercentage = (stockObject.getPrice() - self.avgStockCost) / stockObject.getPrice()
                if riskPercentage > self.riskTolerance:                     # loss target breached
                    gso.d3 += 1
                    sellMarket(self.traderID, self.stocksOwned)
                    return
                elif stockObject.marketBias < (-1)*self.biasThreshold:      # market perception of trader is bearish
                    gso.d4 += 1
                    self.executeDecision(stockObject, intuitionStrength, random.choices([randomBuy, randomSell], weights=[6, 4]))
                    return
                else:                                                       # market perception of trader in stable zone
                    gso.d5 += 1
                    self.executeDecision(stockObject, intuitionStrength, random.choices([randomBuy, randomSell], weights=[4, 6]))
                    return
        else:                                                               # if stocks not owned
            if random.choices([stockObject.marketBias < (-1) * self.biasThreshold,
                              stockObject.marketBias > self.biasThreshold, True])[0]:
                gso.d6 += 1
                self.executeDecision(stockObject, intuitionStrength, randomBuy)
                return
            else:
                gso.d7 += 1
                return                                                      # hold your horses!!


daynum = -1

def setDay(value):
    global daynum
    daynum = value

def getLimitBuyPrice(price, intuitionStrength):
    iList = [intuitionStrength, 1-intuitionStrength]
    return int(price * (limitBuyLowerBound + lblBias + random.betavariate(max(iList), min(iList))/10))


def getLimitSellPrice(price, intuitionStrength):
    iList = [intuitionStrength, 1-intuitionStrength]
    return int(price * (limitSellLowerBound + lslBias + random.betavariate(max(iList), min(iList))/10))


def buyMarket(traderID, quantity):
    filterOrderLists()
    traderObject = traderDict[traderID]
    priceList = sorted(gso.sellOrders.keys())
    while quantity > 0:
        #print('buyMarket', traderID, quantity)
        if not priceList:
            buyLimit(traderID, quantity, gso.price)
            return
        currentLeastPrice = priceList[0]
        while gso.sellOrders[currentLeastPrice]:
            tid, qt = gso.sellOrders[currentLeastPrice][0]
            traderObject2 = traderDict[tid]
            if quantity > qt:
                gso.sellOrders[currentLeastPrice] = gso.sellOrders[currentLeastPrice][1:]
                quantity -= qt
                traderObject.capital -= qt * currentLeastPrice
                traderObject2.capital += qt * currentLeastPrice   # capital added when order executed
                prevStocksOwned = traderObject.stocksOwned
                traderObject.stocksOwned += qt
                traderObject.avgStockCost = (traderObject.avgStockCost * prevStocksOwned + qt * currentLeastPrice) / traderObject.stocksOwned
                traderObject2.liveOrders.remove((currentLeastPrice, qt, 's'))
                gso.orderHistory.append((traderID, tid, currentLeastPrice, qt, daynum, gso.getPrice()))
                if not gso.sellOrders[currentLeastPrice]:
                    del gso.sellOrders[currentLeastPrice]
                    priceList = priceList[1:]
                if not priceList:
                    buyLimit(traderID, quantity, gso.price)
                    return
                currentLeastPrice = priceList[0]

            else:
                traderObject.capital -= quantity * currentLeastPrice
                traderObject2.capital += quantity * currentLeastPrice
                prevStocksOwned = traderObject.stocksOwned
                traderObject.stocksOwned += quantity
                traderObject.avgStockCost = (traderObject.avgStockCost * prevStocksOwned + quantity * currentLeastPrice)/ traderObject.stocksOwned
                traderObject2.liveOrders.remove((currentLeastPrice, qt, 's'))
                gso.sellOrders[currentLeastPrice].remove((tid, qt))
                if qt - quantity > 0:
                    traderObject2.liveOrders.append((currentLeastPrice, qt - quantity, 's'))
                    gso.sellOrders[currentLeastPrice].append((tid, qt - quantity))
                if not gso.sellOrders[currentLeastPrice]:
                    del gso.sellOrders[currentLeastPrice]
                gso.orderHistory.append((traderID, tid, currentLeastPrice, quantity, daynum, gso.getPrice()))
                quantity = 0
                break
        return


def sellMarket(traderID, quantity):
    filterOrderLists()
    traderObject = traderDict[traderID]
    priceList = sorted(gso.buyOrders.keys(), reverse=True)
    while quantity > 0:
        #print('sellMarket', traderID, quantity)
        if not priceList:
            sellLimit(traderID, quantity, gso.getPrice())
            return
        currentMaxPrice = priceList[0]
        while gso.buyOrders[currentMaxPrice]:
            tid, qt = gso.buyOrders[currentMaxPrice][0]
            traderObject2 = traderDict[tid]
            if quantity > qt:
                gso.buyOrders[currentMaxPrice] = gso.buyOrders[currentMaxPrice][1:]
                quantity -= qt
                traderObject.capital += qt * currentMaxPrice
                traderObject2.avgStockCost = (traderObject2.avgStockCost * traderObject2.stocksOwned + qt * currentMaxPrice) / (traderObject2.stocksOwned + qt)
                traderObject.stocksOwned -= qt
                traderObject2.stocksOwned += qt
                # traderObject2.capital -= qt * currentMaxPrice  # capital deducted at the time of placing limit order
                traderObject2.liveOrders.remove((currentMaxPrice, qt, 'b'))
                gso.orderHistory.append((tid, traderID, currentMaxPrice, qt, daynum, gso.getPrice()))
                if not gso.buyOrders[currentMaxPrice]:
                    del gso.buyOrders[currentMaxPrice]
                    priceList = priceList[1:]
                if not priceList:
                    sellLimit(traderID, quantity, gso.getPrice())
                    return
                currentMaxPrice = priceList[0]
            else:
                traderObject.capital += quantity * currentMaxPrice
                traderObject2.avgStockCost = (traderObject2.avgStockCost * traderObject2.stocksOwned + quantity * currentMaxPrice) / (traderObject2.stocksOwned + quantity)
                traderObject.stocksOwned -= quantity
                traderObject2.stocksOwned += quantity
                traderObject2.liveOrders.remove((currentMaxPrice, qt, 'b'))
                gso.buyOrders[currentMaxPrice].remove((tid, qt))
                if qt - quantity > 0:
                    traderObject2.liveOrders.append((currentMaxPrice, qt - quantity, 'b'))
                    gso.buyOrders[currentMaxPrice].append((tid, qt - quantity))
                if not gso.buyOrders[currentMaxPrice]:
                    del gso.buyOrders[currentMaxPrice]
                gso.orderHistory.append((tid, traderID, currentMaxPrice, quantity, daynum, gso.getPrice()))
                quantity = 0
                break
    return


def buyLimit(traderID, quantity, price):
    filterOrderLists()
    #print('buyLimit', traderID, quantity, price)
    traderObject = traderDict[traderID]
    if price in gso.sellOrders:
        while quantity > 0:
            if not gso.sellOrders[price]:
                del gso.sellOrders[price]
                addToBuyOrders(traderID, price, quantity)
                return
            tid, qt = gso.sellOrders[price][0]
            traderObject2 = traderDict[tid]
            if quantity > qt:
                gso.sellOrders[price] = gso.sellOrders[price][1:]
                quantity -= qt
                prevStocksOwned = traderObject.stocksOwned
                traderObject.stocksOwned += qt
                traderObject.capital -= qt * price                                      # Funds Transfer
                traderObject2.capital += qt * price                                     # capital added when order executed
                traderObject.avgStockCost = (traderObject.avgStockCost * prevStocksOwned + qt * price) / traderObject.stocksOwned
                traderObject2.liveOrders.remove((price, qt, 's'))
                gso.orderHistory.append((traderID, tid, price, qt, daynum, gso.getPrice()))
            else:
                traderObject.capital -= quantity * price                                # Funds Transfer
                traderObject2.capital += quantity * price
                prevStocksOwned = traderObject.stocksOwned
                traderObject.stocksOwned += quantity
                traderObject.avgStockCost = (traderObject.avgStockCost * prevStocksOwned + quantity * price) / traderObject.stocksOwned
                traderObject2.liveOrders.remove((price, qt, 's'))
                gso.sellOrders[price].remove((tid, qt))
                if qt - quantity > 0:
                    traderObject2.liveOrders.append((price, qt - quantity, 's'))
                    gso.sellOrders[price].append((tid, qt - quantity))
                if not gso.sellOrders[price]:
                    del gso.sellOrders[price]
                gso.orderHistory.append((traderID, tid, price, quantity, daynum, gso.getPrice()))
                break
    else:
        if quantity > 0:
            addToBuyOrders(traderID, price, quantity)
        return


def sellLimit(traderID, quantity, price):
    filterOrderLists()
    #print('sellLimit', traderID, quantity, price)
    traderObject = traderDict[traderID]
    if price in gso.buyOrders:
        while quantity > 0:
            if not gso.buyOrders[price]:
                del gso.buyOrders[price]
                addToSellOrders(traderID, price, quantity)
                return
            tid, qt = gso.buyOrders[price][0]
            traderObject2 = traderDict[tid]
            if quantity > qt:
                gso.buyOrders[price] = gso.buyOrders[price][1:]
                quantity -= qt
                traderObject.capital += qt * price
                traderObject2.avgStockCost = (traderObject2.avgStockCost * traderObject2.stocksOwned + qt * price) / (traderObject2.stocksOwned + qt)
                traderObject.stocksOwned -= qt
                traderObject2.stocksOwned += qt
                # traderObject2.capital -= qt * currentMaxPrice  # capital deducted at the time of placing limit order
                traderObject2.liveOrders.remove((price, qt, 'b'))
                gso.orderHistory.append((tid, traderID, price, qt, daynum, gso.getPrice()))
            else:
                traderObject.capital += quantity * price
                traderObject2.liveOrders.remove((price, qt, 'b'))
                traderObject2.avgStockCost = (traderObject2.avgStockCost * traderObject2.stocksOwned + quantity * price) / (traderObject2.stocksOwned + quantity)
                traderObject.stocksOwned -= quantity
                traderObject2.stocksOwned += quantity
                gso.buyOrders[price].remove((tid, qt))
                if qt - quantity > 0:
                    traderObject2.liveOrders.append((price, qt - quantity, 'b'))
                    gso.buyOrders[price].append((tid, qt - quantity))
                if not gso.buyOrders[price]:
                    del gso.buyOrders[price]
                gso.orderHistory.append((tid, traderID, price, quantity, daynum, gso.getPrice()))
                break
    else:
        if quantity > 0:
            addToSellOrders(traderID, price, quantity)
        return


def addToBuyOrders(traderID, price, quantity):
    if price in gso.buyOrders:
        gso.buyOrders[price].append((traderID, quantity))
    else:
        gso.buyOrders[price] = [(traderID, quantity)]
    traderObject = traderDict[traderID]
    traderObject.capital -= price * quantity
    traderObject.liveOrders.append((price, quantity, 'b'))


def addToSellOrders(traderID, price, quantity):
    if price in gso.sellOrders:
        gso.sellOrders[price].append((traderID, quantity))
    else:
        gso.sellOrders[price] = [(traderID, quantity)]
    traderObject = traderDict[traderID]
    traderObject.liveOrders.append((price, quantity, 's'))
    traderObject.stocksOwned -= quantity


def cancelSellOrder(traderID, price, quantity):
    gso.sellOrders[price].remove((traderID, quantity))
    traderObject = traderDict[traderID]
    traderObject.stocksOwned += quantity
    traderObject.liveOrders.remove((price, quantity, 's'))


def cancelBuyOrder(traderID, price, quantity):
    gso.buyOrders[price].remove((traderID, quantity))
    traderObject = traderDict[traderID]
    traderObject.capital += price * quantity
    traderObject.liveOrders.remove((price, quantity, 'b'))


def filterOrderLists():
    for i in list(gso.buyOrders.keys()):
        if not gso.buyOrders[i]:
            del gso.buyOrders[i]
    for i in list(gso.sellOrders.keys()):
        if not gso.sellOrders[i]:
            del gso.sellOrders[i]


def initializeTraders(n):
    traderDict = {}
    for i in range(n):
        startingPrice = initialStockPrice
        if random.choices([True, False], weights=[1, 9])[0]:
            capital = int(startingCapitalNS*random.betavariate(9, 1))
            stocksOwned = 0
            avgStockCost = 0
        else:
            capital = int(startingCapitalS * random.betavariate(3, 7))
            stocksOwned = int(random.betavariate(1, 9) * 100)
            avgStockCost = (0.6 + (0.4 * random.betavariate(1, 1))) * startingPrice
        traderDict[i] = Trader(i, capital, stocksOwned, avgStockCost, random.betavariate(2, 8), random.betavariate(2, 8)/10)
    return traderDict


def getVolume(orderDict):
    return sum(map(lambda xl: sum(list(map(lambda x: x[1], xl))),orderDict.values()))


def getTraderAssets(traderObject):
    totalAssets = traderObject.capital
    totalAssets += gso.getPrice() * traderObject.stocksOwned
    for (p, q, strr) in traderObject.liveOrders:
        if strr == 's':
            totalAssets += q * gso.getPrice()
        else:
            totalAssets += q * p
    return totalAssets


for _ in range(numberOfSimulations):
    history = []
    volume = []
    initialW = []
    finalW = []
    traderDict = initializeTraders(numberOfTraders)
    gso = Stock(initialStockPrice)
    initialAssets = {k: getTraderAssets(v) for k, v in traderDict.items()}
    for i in traderDict:
        initialW.append(getTraderAssets(traderDict[i]))
    for j in range(simulationLengthDays):
        setDay(j + 1)
        for i in traderDict:
            traderDict[i].makeDecision(gso)
        gso.alterPriceAndMarketBias()
        history.append(gso.getPrice())
        volume.append(getVolume(gso.sellOrders) + getVolume(gso.buyOrders))
    for i in traderDict:
        finalW.append(getTraderAssets(traderDict[i]))
    finalAssets = {k: getTraderAssets(v) for k, v in traderDict.items()}
    profitableTradersDict = {}
    lossMakingTradersDict = {}
    for i in initialAssets:
        if initialAssets[i] < finalAssets[i]:
            profitableTradersDict[i] = finalAssets[i] - initialAssets[i]
        else:
            lossMakingTradersDict[i] = initialAssets[i] - finalAssets[i]
    bestTrader = max(profitableTradersDict, key=profitableTradersDict.get)
    bestTraderBuyOrders = []
    bestTraderSellOrders = []
    for i in gso.orderHistory:
        if i[0] == bestTrader:
            bestTraderBuyOrders.append((i[4], i[2], i[3]))
        elif i[1] == bestTrader:
            bestTraderSellOrders.append((i[4], i[2], i[3]))
    pylab.figure(1)
    pylab.title('Closing Price, Sell Orders (Red), Buy Orders (Green)')
    pylab.xlabel('Day')
    pylab.ylabel('Price')
    pylab.plot(history)                          # Blue
    # pylab.plot(volume)                           # Yellow

    pylab.scatter(list(zip(*bestTraderSellOrders))[0], list(zip(*bestTraderSellOrders))[1], c='red', marker='v', s=list(zip(*bestTraderSellOrders))[2])
    pylab.scatter(list(zip(*bestTraderBuyOrders))[0], list(zip(*bestTraderBuyOrders))[1], c='green', marker='^', s=list(zip(*bestTraderBuyOrders))[2])
    pylab.figure(2)
    pylab.title('Starting Wealth (Teal)/ Final Wealth (Red)')
    pylab.ylabel('Frequency')
    pylab.xlabel('Net Value')
    pylab.hist(initialW, bins=40, rwidth=0.4, color='teal', align='left', stacked=True, range=(min(min(initialW), min(finalW)), max(max(initialW), max(finalW))))
    pylab.hist(finalW, bins=40, rwidth=0.4, color='red', align='mid', stacked=True, alpha=0.7, range=(min(min(initialW), min(finalW)), max(max(initialW), max(finalW))))
    pylab.show()



'''
pylab.figure(3)
pylab.title('Final Wealth')
pylab.xlabel('TraderID')
pylab.ylabel('Net Value')

print(vars(traderDict[0]))
print(vars(traderDict[1]))
addToBuyOrders(0,100,2)
sellLimit(1,1,100)
print(vars(traderDict[0]))
print(vars(traderDict[1]))
'''

'''
vol = 0
for i in traderDict:
    vol += traderDict[i].stocksOwned
vol += getVolume(gso.sellOrders)
print(vol)
'''
    #print(gso.price, gso.marketBias, getVolume(gso.buyOrders), getVolume(gso.sellOrders))
#print(gso.d1, gso.d2, gso.d3, gso.d4, gso.d5, gso.d6, gso.d7)
#for i in traderDict:
    #print(vars(traderDict[i]))

#for k in range(30):
#for i in traderDict:
#    print(vars(traderDict[i]))

# gso = GlobalStockObject
# traderDict = {traderID:traderObject} (also Global)

# print(bestTrader)
# print(profitableTradersDict[bestTrader])
# print(len(profitableTradersDict))
# print(len(lossMakingTradersDict))
# print(gso.d1, gso.d2, gso.d3, gso.d4, gso.d5, gso.d6, gso.d7)
# print(gso.orderHistory)
