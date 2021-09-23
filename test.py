import requests

BASE = 'http://127.0.0.1:5000/'

# sample = [{
#   "name": "First Vid",
#   "views": 10,
#   "likes": 4
# }, {
#   "name": "Second Vid",
#   "views": 31,
#   "likes": 400
# }, {
#   "name": "Third Vid",
#   "views": 1000,
#   "likes": 57
# }]

# for i in range(len(sample)):
#   response = requests.post(BASE + "video/" + str(i), sample[i] )
#   print(response.json())

response = requests.patch(BASE + '/video/0', {
  "likes": "450"
})
print(response.json())