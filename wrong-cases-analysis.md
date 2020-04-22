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

Evaluating database:  BASELINE-6
Capture 8 events in the databse BASELINE-6
==============================================================
Predicted: [632565000012][putback=0] FIJI WATER .5 LTR, weight=538g, count=2
Predicted: [632565000029][putback=0] FIJI NATURAL WATER 1LTR, weight=1059g, count=1
Predicted: [632565000012][putback=1] FIJI WATER .5 LTR, weight=538g, count=1
Predicted: [632565000012][putback=0] FIJI WATER .5 LTR, weight=538g, count=1
Predicted: [898999010007][putback=0] Vita Coco original 500ml, weight=538g, count=1
Database: BASELINE-6, Correct Items on Receipts: 3/4, Total GT items: 3
Behaviors:
1. Take 1 LTR FIJI Water
2. Put it to .5 LTR FIJI Water shelf
3. Take 2 .5 LTR FIJI Water at the same time
4. Take a coco water, Misplace to another location
5. Take the misplaced coco water away
Reason:
Event is not sorted by time. Put back is wrong.

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

Evaluating database:  BASELINE-8
Capture 7 events in the databse BASELINE-8
==============================================================
Predicted: [042238302556][putback=0] Haribo Gold Bears Gummi Candy, weight=295g, count=1
Predicted: [071142008582][putback=0] ARRWHD SPRNG WTR, weight=621g, count=1
Predicted: [071142643370][putback=0] ARRWHD MTN WTR SPRT BTL, weight=736g, count=1
Predicted: [818780014243][putback=0] Boomchickapop Sea Salt Popcorn, weight=42g, count=1
Predicted: [078907420108][putback=0] El Sabroso Blazing Hot Cheetos, weight=121g, count=1
Predicted: [071063437553][putback=0] Taco Bell Diablo, weight=103g, count=1
Database: BASELINE-8, Correct Items on Receipts: 4/6, Total GT items: 6
Reason:
Association is not correct!

Evaluating database:  BASELINE-10
Capture 2 events in the databse BASELINE-10
==============================================================
Predicted: [818780014229][putback=0] Boomchickapop Sweet & Salty Kettle Corn, weight=71g, count=2
Predicted: [016571953386][putback=0] ICE Ginger Lime, weight=532g, count=2
Database: BASELINE-10, Correct Items on Receipts: 2/4, Total GT items: 6
Reason:
3 TIMES: Take two items at the same time. Different item, same item, different shelf.

Evaluating database:  BASELINE-12
Capture 24 events in the databse BASELINE-12
==============================================================
Predicted: [613008744090][putback=0] AZ MUCHO MANGO, weight=563g, count=1
Predicted: [818780014229][putback=0] Boomchickapop Sweet & Salty Kettle Corn, weight=71g, count=1
Predicted: [818780014243][putback=0] Boomchickapop Sea Salt Popcorn, weight=42g, count=1
Predicted: [891760002560][putback=0] Paqui Tortilla Chips Ghost Pepper, weight=63g, count=4
Predicted: [078907420108][putback=0] El Sabroso Blazing Hot Cheetos, weight=121g, count=1
Predicted: [613008744090][putback=1] AZ MUCHO MANGO, weight=563g, count=1
Predicted: [078907420108][putback=1] El Sabroso Blazing Hot Cheetos, weight=121g, count=1
Predicted: [888109010102][putback=0] Hostess Twinkies, weight=81g, count=2
Predicted: [891760002560][putback=1] Paqui Tortilla Chips Ghost Pepper, weight=63g, count=3
Predicted: [012000286209][putback=0] Pure Leaf Unsweetened Black Tea, weight=592g, count=1
Predicted: [012000286209][putback=0] Pure Leaf Unsweetened Black Tea, weight=592g, count=1
Predicted: [888109010102][putback=1] Hostess Twinkies, weight=81g, count=2
Predicted: [026200471594][putback=0] Andy Capps Hot Fry Bag, weight=92g, count=1
Predicted: [026200471594][putback=0] Andy Capps Hot Fry Bag, weight=92g, count=1
Predicted: [024100204113][putback=0] CheezIt Original, weight=209g, count=1
Predicted: [016000126077][putback=0] Chex Mix Savory Snack Mix Bold Party Blend, weight=111g, count=1
Predicted: [818780014243][putback=1] Boomchickapop Sea Salt Popcorn, weight=42g, count=1
Predicted: [818780014229][putback=1] Boomchickapop Sweet & Salty Kettle Corn, weight=71g, count=1
Database: BASELINE-12, Correct Items on Receipts: 0/7, Total GT items: 2
