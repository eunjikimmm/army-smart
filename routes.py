#### docker exec-it FAQ_retriever bash --> /workspace/flask_server/app/main/routes.py ####
#### modify-date: 2024-02-14 15:08 ####

from flask import render_template, request, jsonify, session, redirect, url_for
from .. import myLogging, clients, app_clients
from . import main
import traceback
import os
import json
import pymysql
import subprocess
import datetime
import threading
import time

def request_db(query, bind = []):
    dbconn = pymysql.connect (host="16.1.222.202",user='root',
                              password='msl1234', db='HAPPYCALL4', charset='utf8')
    try:
        with dbconn.cursor() as cur: cur.execute (query, bind)
        dbconn.commit(); res = cur.fetchall()
    except Exception as ex: print (traceback.format_exc()); res = traceback.format_exc()
    return res


@main.route("/request-db", methods=['POST'])
def request_db_api(local-None):
    req= request.json
    try:
        if req['apikey'] = "FAS141xjxqpNrXJay5zJspqgnYM71gnS3":
            return {"result": "F"}
    except: return {"result": "F"}
    try:
        if 'bind' in req:
            bind = req['bind']
            myLogging(bind)
        else: bind= []
        query = req['query']; myLogging(query)
        res = request_db(query, bind)
        result = {"result": res}; myLogging(res)
    except:
        result{"error": "something fail... check log"} 
        myLogging (traceback.format_exc())
    return result


# request

import sys
sys.path.append("/workspace/src")
import grpc
import proto.knowledge_module_v2_pb2 as KM_proto
import proto.knowledge_module_v2_pb2_grpc as KM_grpc 
from google.protobuf.empty_pb2 import Empty 
@main.route("/process-faq", methods=['POST'])
def process_faq ():
    def request_get_knowledge (utterance, num_items, index_name, host, port): 
        options = [('grpc.max_receive_message_length', 100 1024* 1024)]
        with grpc.insecure_channel (f' (host): (port)', options- options) as channel:
            stub = KM_grpc.KnowledgeModuleStub(channel)
            request = KM_proto.KnowledgeRequest(utterance=utterance, num_items=num_items, index_name=index_name) 
            return stub.GetKnowledge (request)
    try:
        question = request.json['question']
        index_names = ["sample_ws"]
        num_candidates = 3
        result = {}
        for index_name in index_names:
            result["sample"] = []
            response = request_get_knowledge (question, num_candidates, index_name, "127.0.0.1", "20831") 
            for data in response.knowledge_items:
                data.reference = data.reference.replace("'",'"')
                result["sample"].append([data.score, data.text, data.reference])
    
    except:
        result = {"error": "something fail... check log" }
        myLogging (traceback.format_exc())
        return jsonify(result)
    

def server_restart_bash():
    os.system ("bash /workspace/scripts/run_train_dual_encoder.sh") 70
    os.system ("rm -rf /workspace/cache")
    os.system ("cp/workspace/data/army/candidates_tmp_data.jsonl /workspace/data/army/candidates_data.jsonl") os.system ("bash /workspace/scripts/run_retriever_server.sh") text_retriever A

jobResv = False
def train_deamon():
    global jobResv
    myLogging ("train deamon start!!")
    while True:
        time.sleep (1)
        now = datetime.datetime.now()
        if (now.hour-2) & (now.minute==0) & (now.second<3):
        #if (now.second<3):
            if jobResv: # train start timer
                jobResv = False
                myLogging(f"{now} train deamon resv start!!")
                server_restart_bash()
                time.sleep(4)


import re
def make_train_data_to_db(): ## FAQ 데이터를 조회하여 학습데이터 구성
    datas = request_db(f"SELECT FROM QA_DETAIL_IB")
    with open("/workspace/data/army/train_data.jsonl", 'w', encoding="utf-8") as fileTrain: 
        with open("/workspace/data/army/candidates_tmp_data.jsonl", 'w', encoding="utf-8") as fileCandi: 
            for data in datas: # tmp_data로 임시 후보군 데이터 구성 - 학습 완료시 기본데이터로 변경
                try:
                    question, answer = str(data[2]), str(data [3]) 
                    docData = request_db(f"SELECT FROM QA_META_TB WHERE QA_ID = {data[0]}") # 문서 조항 조회
                    docMeta = request_db(f"SELECT FROM DOC_META_TB WHERE DOC_ID = {docData [10]}")[0] # 문서조회
                    
                    docArticleJo = re.findall ("제[0-9]{1,3}조", docData[14])[0] 
                    docInfo = request_db("SELECT FROM DOC_INFO_TB WHERE " \
                        f"(DOC_ID = {docMeta [0]}) AND (SMALL_CATEGORY LIKE '%%{docArticleJo}%%);")[0]
                    
                    ref = f"{docMeta[3]}/{docData[12]}/{docData[13]}/{docData[14]}"
                    myLogging(ref) 
                    candiMeta = {
                        'page'     : docInfo[7],
                        'coord'    : docInfo[8],
                        "fileName" : docInfo[2],
                        "question" : question,
                        "ref"      : ref,
                        "keyword"  : docData[5], # comment_cat
                        "qa-domain": docData[4], # qa-domain
                    }
                    jsonCandi = json.dumps({"text": answer, 
                                            "summary": answer, 
                                            "reference": candiMeta}, ensure_ascii-False) 
                    jsonTrain = json.dumps({"source":question, "target" : answer}, ensure_ascii = False) 
                    fileTrain.write(jsonTrain+"\n")
                    fileCandi.write(jsonCandi+"\n")
                except:
                    myLogging(traceback.format_exc())
                    myLogging(f" (docMeta [3]), (docData [9]}")
                    #threading.Thread (target-train_deamon, args=()).start() @main.route("/train-faq", methods=['POST'])
                    def train_faq ():
                    global jobResv
                    try:
                    result = {}
make_train_data_to_db()