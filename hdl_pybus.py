from datetime import timedelta, datetime
from bottle import run, debug, route, template, request, abort
import json, time
import pymongo

#################################
# Handlers to manage requests
#################################
# - add - Adds a deploy record
def add(connection):
  db = connection.dtrack
  postBody = request.body.read()
  if not postBody:
    abort(400, 'No data received')
  entity = json.loads(postBody)
  entity["_id"] = int(round(time.time() * 1000)) # current time in milli
  for k in ["_id", "action", "data"]:
    if not entity.has_key(k):
      abort(400, 'No %s specified' % k)
  try:
    db['pyBus'].save(entity)
    return "saved"
  except Exception, e:
    abort(500, e)

# - get_all - Gets all deploy records within a number of days (default 7), 
#             from an optionally specified user
def get_all(connection):
  try:
    db = connection.dtrack
    postData = request.body.read()
    query = json.loads(postData)
    
    entities = db['pyBus'].find(query)
    if not entities:
      abort(404, 'No documents found')

    returnData = []
    for entity in entities:
      returnData.append(entity)
    return json.dumps(returnData)
  except Exception, e:
    print e