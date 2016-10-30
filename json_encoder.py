import json
import time

# this will get replaced with the actual data
dict = [{"State Name": "Alabama", "Num_Positive_Tweets": 400, "Num_Negative_Tweets": 200}]

# create a new file based on the current date / time
path = 'queries/' + str(int(time.time())) + '.json'
file = open(path, 'w')

file.write(json.dumps(dict))
print(path)

file.close()
