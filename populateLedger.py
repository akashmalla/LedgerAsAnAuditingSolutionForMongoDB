__author__ = 'akashmalla'

import pymongo
import schedule
import time
import datetime
import traceback

def mongodb_conn():
    try:
        maxSevSelDelay=10000
        client = pymongo.MongoClient("13.56.77.24",serverSelectionTimeoutMS=maxSevSelDelay)
        client.server_info()
    except pymongo.errors.ConnectionFailure as err1:
        print("Could not connect to server, connection failure:",err1)
    except pymongo.errors.ServerSelectionTimeoutError as err2:
        print("Could not connect to server, ServerSelectionTimeoutError:",err2)
    return client

def job():
    conn = mongodb_conn()
    #print("connected successfully")
    if conn is None:
        # no connection, exit early
        print("not connected to mongodb!")
        return

    #print("I'm working...")
    try:
        db = conn.data
        input=db.current_op(True)

        for j in input['inprog']:

            if j['active']==True:
                if 'microsecs_running' in j and j['microsecs_running']>50 and j['microsecs_running']<15000:
                        #print(j)
                        newJ=dict()
                        if 'opid' in j:
                            newJ['opid']=j['opid']
                        if 'op' in j:
                            newJ['operation']=j['op']
                        if 'microsecs_running' in j:
                            newJ['microsecs_running']=j['microsecs_running']
                        if 'client' in j:
                            newJ['client']=j['client']
                        if 'ns' in j:
                            newJ['namespace']=j['ns']
                        newJ['time']=datetime.datetime.now()
                        server_status=db.command({"serverStatus":1})
                        newJ['current_connections']=server_status['connections']['current']
                        newJ['available_connections']=server_status['connections']['available']
                        newJ['active_clients']=server_status['globalLock']['activeClients']['total']
                        newJ['current_queue']=server_status['globalLock']['currentQueue']['total']
                        newJ['network_bytesIn']=server_status['network']['bytesIn']
                        newJ['network_bytesOut']=server_status['network']['bytesOut']
                        newJ['network_numRequests']=server_status['network']['numRequests']
                        newJ['opcounters_insert']=server_status['opcounters']['insert']
                        newJ['opcounters_query']=server_status['opcounters']['query']
                        newJ['opcounters_update']=server_status['opcounters']['update']
                        newJ['extra_info_page_faults']=server_status['extra_info']['page_faults']
                        newJ['memory_virtual']=server_status['mem']['virtual']
                        newJ['memory_resident']=server_status['mem']['resident']
                        print(newJ)
                        #print("inside\n")

                        db.ledgerData.insert_one(newJ)

    except:
        traceback.print_exc()
        exit(1)

job()
schedule.every(1).seconds.do(job)
schedule.every().hour.do(job)
schedule.every().day.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)

# java -jar POCDriver.jar -k 20 -i 20 -u 20 -d 600 -t 2 -e -y 10
