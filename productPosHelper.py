import BookKeeper

productID = '042238302556'

myBK = BookKeeper.BookKeeper('cps-test-12')
print(productID, myBK.getProductByID(productID).name)
print(myBK.getProductPosAverage(productID))
print(myBK.getProductCoordinates(productID))