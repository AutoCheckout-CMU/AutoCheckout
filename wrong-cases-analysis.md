Evaluating database:  BASELINE-2
Capture 4 events in the databse BASELINE-2
==============================================================
Predicted: [613008744120][putback=0] AZ WATERMELON, weight=567g, count=1
Predicted: [613008744120][putback=1] AZ WATERMELON, weight=567g, count=1
Predicted: [071063437553][putback=0] Taco Bell Diablo, weight=103g, count=1
Predicted: [012000286209][putback=0] Pure Leaf Unsweetened Black Tea, weight=592g, count=1
Database: BASELINE-2, Correct Items on Receipts: 2/2, Total GT items: 3
Reason:
A bottle of water is not detected


Evaluating database:  BASELINE-7
Capture 2 events in the databse BASELINE-7
==============================================================
Predicted: [078907916342][putback=0] El Sabroso Hot Spicy Cracklins, weight=52g, count=1
Predicted: [858369006207][putback=0] Soylent Strawberry, weight=467g, count=1
Database: BASELINE-7, Correct Items on Receipts: 2/2, Total GT items: 4
Reason:
the platedata ends so early that the last two events happens in the last window during the sliding,
but sliding window cannot detect events happening at the last window 
(because the mean and variance do not change in one window)
possible solution:
manully add data of one window with stable state value.
