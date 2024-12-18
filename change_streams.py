from pymongo import MongoClient
from datetime import datetime, timedelta
import sys

def test():
    aggCmdRes = db.command({
      "aggregate": "changestream",
      "pipeline": [{ "$changeStream": {} }],
      "cursor": {},
    })
    startTime = datetime.now()
    results ={}

    while datetime.now() - startTime < duration:
        getMoreCmdRes = db.command({
          "getMore": aggCmdRes['cursor']['id'],
          "collection": "people",
          "maxTimeMS" : 1000,
          #"batchSize": 100,
        })
        results[datetime.now()] = getMoreCmdRes['cursor']['nextBatch']

    db.command( { "killCursors": "peope", "cursors": [ aggCmdRes['cursor']['id'] ] } )

    totalLatency = timedelta()
    numEvents = 0

    for getMoreTs in results:
        if len(results[getMoreTs]) > 0:
            getMoreTime = getMoreTs
            for event in results[getMoreTs]:
                totalLatency += getMoreTime - event['wallTime']
                numEvents+=1

    print("Events: {}".format(numEvents))
    avg_latency = (totalLatency / numEvents).microseconds/1000
    print("Avg. Latency: {} ms".format((totalLatency / numEvents).microseconds/1000));

    return avg_latency

# MUST ADD YOUR MONGODB CONNECTION STRING!
#TODO add command line options to initalize the script with the right variables
uri = ""
print(f"Connecting to mongodb at {uri}")
client = MongoClient(uri)
db = client.test
collection = db.changestream
#TODO Add actual connection test using ping or hello
print(f"Connected!")  

if len(sys.argv) > 1:
    loops = int(sys.argv[1])
else:
    loops = 1

if len(sys.argv) > 2:
    duration = timedelta(seconds=int(sys.argv[2]))
else:
    duration = timedelta(seconds=60)

print("Running test {} times and for {} sec each time".format(loops, duration.seconds))

avg_latencies = 0 
for i in range(loops):
    avg_latencies+= test()

print("Average latency overall is {} ms".format(avg_latencies/loops))
