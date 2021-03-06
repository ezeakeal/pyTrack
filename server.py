#!/usr/bin/python
from bottle import run, debug, route, template, request, abort, hook, response
from datetime import timedelta, datetime
import json, time
import pymongo

#################################
# GLOBALS
#################################
import hdl_pybus

#################################
# Load up MongoDB
#################################
connection = pymongo.Connection('localhost', 27017)

#################################
# Enable Cross access
#################################
@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = True
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'

#################################
# Handlers for PyBus
#################################
@route('/api/pybus/add', method="POST")
def pyb_add():
  return hdl_pybus.add(connection)
    
# - get_all - Gets all posts within a number of days
@route('/api/pybus/get_all')
@route('/api/pybus/get_all/:numDays')
def pyb_get_all(numDays=7):
  return hdl_pybus.get_all(connection, numDays)

#################################
# MAIN
#################################
run(host='0.0.0.0', debug=True, port=7725, reloader=True)
