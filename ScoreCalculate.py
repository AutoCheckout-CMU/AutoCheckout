from BookKeeper import BookKeeper
from WeightTrigger import PickUpEvent
import math_utils

sigmaForEventWeight = 10.0 #gram
sigmaForProductWeight = 10.0 #gram
arrangementContribution = 0.8
weightContribution = 1 - arrangementContribution


class ProductScore:
    arrangementScore: float
    weightScore: float
    barcode: str
    bk: BookKeeper

    def __init__(self, barcode, bk):
        self.barcode = barcode
        self.arrangementScore = 0.
        self.weightScore = 0.
        self.bk = bk
    
    def getTotalScore(self):
        return arrangementContribution*self.arrangementScore+weightContribution*self.weightScore

    def __repr__(self):
        return str(self)

    def __str__(self):
        productExtended = self.bk.getProductByID(self.barcode)
        return "[%s] arrangementScore=%f weightScore=%f totalScore=%f, weight=%f" % (
            self.barcode, 
            self.arrangementScore, 
            self.weightScore, 
            self.getTotalScore(),
            productExtended.weight
        )

class ScoreCalculator:

    # [ProductScore]
    __productScoreRank: list

    # productID -> ProductScore
    __productScoreDict: dict

    __event: PickUpEvent

    __bk: BookKeeper

    def __init__(self, bk, event):
        self.__bk = bk
        self.__productScoreRank = []
        self.__productScoreDict = {}
        self.__event = event
        for productID in self.__bk.productIDsFromProductsTable:
            productScore = ProductScore(productID, bk)
            self.__productScoreRank.append(productScore)
            self.__productScoreDict[productID] = productScore

        self.__calculateArrangementScore()
        self.__calculateWeightScore()
        self.__productScoreRank.sort(key=lambda productScore: productScore.getTotalScore(), reverse=True)

    def getTopK(self, k):
        return self.__productScoreRank[:k]

    def getScoreByProductID(self, productID):
        return self.__productScoreDict[productID]

    # arrangement probability (with different weight sensed on different plate)
    def __calculateArrangementScore(self):
        deltaWeights = self.__event.deltaWeights
        plateProb = 0
        probPerPlate = []
        overallDelta = sum(deltaWeights)

        # a potential bug: what if there are both negatives and positives and their sum is zero?
        if (overallDelta == 0):
            plateProb = 1/len(deltaWeights)
            for i in range(0, len(deltaWeights)):
                probPerPlate.append(plateProb)
        else:
            for deltaWeight in deltaWeights:
                probPerPlate.append(deltaWeight/overallDelta)

        productIDsOnTheShelf = self.__bk.getProductIDsFromPosition(self.__event.gondolaID, self.__event.shelfID)
        for productID in productIDsOnTheShelf:
            positions = self.__bk.getProductPositions(productID)
            for position in positions:
                if position.gondola != self.__event.gondolaID or position.shelf != self.__event.shelfID:
                    continue
                self.__productScoreDict[productID].arrangementScore += probPerPlate[position.plate-1]


    def __calculateWeightScore(self):
        deltaWeightForEvent = abs(self.__event.deltaWeight)
        for productScore in self.__productScoreRank:
            productWeight = self.__bk.getProductByID(productScore.barcode).weight
            productScore.weightScore = math_utils.areaUnderTwoGaussians(deltaWeightForEvent, sigmaForEventWeight, productWeight, sigmaForProductWeight)
