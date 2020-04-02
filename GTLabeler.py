import json

class Serializable:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)

# {
#   "lists": [
#     {
#       "dataset": "2019-11-07_02-35",
#       "events": [
#         {
#           "eventID": 1,
#           "putback": 0,
#           "observe": {
#             "product": "",
#             "time": "2019-11-07_02-35-28",
#             "position": {
#               "gondola": 2,
#               "shelf": 6,
#               "plates": [
#                 8,
#                 9
#               ]
#             }
#           }
#         },
#         {
#           "eventID": 1,
#           "putback": 0,
#           "observe": {
#             "product": "",
#             "time": "2019-11-07_02-35-28",
#             "position": {
#               "gondola": 2,
#               "shelf": 6,
#               "plates": [
#                 8,
#                 9
#               ]
#             }
#           }
#         }
#       ]
#     }
#   ]
# }

class GroundTruth(Serializable):
